try:
    import ujson as json
except:
    import json
import datetime, urllib
import requests
from flask import Flask, g, request, render_template, redirect, url_for, jsonify, abort
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from webhelpers import paginate
from socket import inet_aton

from lib import SEARCH_PERIOD, ARCHIVE_PERIOD, get_time, validate_chat_url
from lib.archive import archive_chat, get_or_create_log
from lib.characters import CHARACTER_GROUPS, CHARACTERS, CHARACTER_DETAILS
from lib.messages import parse_line
from lib.model import Log, LogPage
from lib.requests import populate_all_chars, connect_redis, connect_mysql, create_normal_session, set_cookie, disconnect_redis, disconnect_mysql
from lib.sessions import CASE_OPTIONS

from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, 2)

# Pre and post request stuff
app.before_first_request(populate_all_chars)
app.before_request(connect_redis)
app.before_request(connect_mysql)
app.before_request(create_normal_session)
app.after_request(set_cookie)
app.teardown_request(disconnect_redis)
app.teardown_request(disconnect_mysql)

# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        replacements=json.loads(g.user.character['replacements']),
        picky=g.redis.smembers(g.user.prefix+'.picky') or set(),
        picky_options=g.redis.hgetall(g.user.prefix+'.picky-options') or {},
        case_options=CASE_OPTIONS,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character['character'],
        users_searching=g.redis.zcard('searchers'),
        users_chatting=g.redis.scard('sessions-chatting'),
        updates_text=(g.redis.get('updates_text') or "").decode("utf8"),
        welcome_text=(g.redis.get('welcome_text') or "").decode("utf8"),
    )

# Chat

@app.route('/chat')
@app.route('/chat/<chat>')
def chat(chat=None):

    if chat is None:
        chat_meta = { 'type': 'unsaved' }
        existing_lines = []
        latest_num = -1
    else:
        if g.redis.hexists("global-bans", request.headers['CF-Connecting-IP']):
            return redirect("http://erigam.tk/")
        if g.redis.zrank('ip-bans', chat+'/'+request.headers['CF-Connecting-IP']) is not None:
            return redirect("http://help.msparp.com/kb/faq.php?id=21")
        # Check if chat exists
        chat_meta = g.redis.hgetall('chat.'+chat+'.meta')
        # Convert topic to unicode.
        if 'topic' in chat_meta.keys():
            chat_meta['topic'] = unicode(chat_meta['topic'], encoding='utf8')
        if len(chat_meta)==0:
            # XXX CREATE
            abort(404)
        # Load chat-based session data.
        g.user.set_chat(chat)
        existing_lines = [parse_line(line, 0) for line in g.redis.lrange('chat.'+chat, 0, -1)]
        latest_num = len(existing_lines)-1

        # *music* DUCT TAPE...
        if g.user.meta['counter'] == "Redis is loading the dataset in memory":
            abort(500)
    return render_template(
        'chat.html',
        user=g.user,
        character_dict=g.user.json_info(),
        case_options=CASE_OPTIONS,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        chat=chat,
        chat_meta=chat_meta,
        lines=existing_lines,
        latest_num=latest_num,
        chat_links=(g.redis.get('chat_links') or "").decode("utf8"),
    )

# Searching

@app.route('/search', methods=['POST'])
def foundYet():
    target=g.redis.get('session.'+g.user.session_id+'.match')
    if target:
        g.redis.delete('session.'+g.user.session_id+'.match')
        return jsonify(target=target)
    else:
        g.redis.zadd('searchers', g.user.session_id, get_time(SEARCH_PERIOD*2))
        abort(404)

@app.route('/stop_search', methods=['POST'])
def quitSearching():
    g.redis.zrem('searchers', g.user.session_id)
    return 'ok'

# Save

@app.route('/save', methods=['POST'])
def save():
    try:
        if 'character' in request.form:
            g.user.save_character(request.form)
        if 'save_pickiness' in request.form:
            g.user.save_pickiness(request.form)
        if 'create' in request.form:
            chat = request.form['chaturl']
            if g.redis.exists('chat.'+chat+'.meta'):
                raise ValueError('chaturl_taken')
            # USE VALIDATE_CHAT_URL
            if not validate_chat_url(chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
            if g.user.meta['group']!='globalmod':
                g.user.set_group('mod')
            g.redis.hset('chat.'+chat+'.meta', 'type', 'group')
            get_or_create_log(g.redis, g.mysql, chat)
            g.mysql.commit()
            return redirect(url_for('chat', chat=chat))
    except ValueError as e:
        return show_homepage(e.args[0])

    if 'search' in request.form:
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('configure'))

# Logs

@app.route('/logs/save', methods=['POST'])
def save_log():
    if not validate_chat_url(request.form['chat']):
        abort(400)
    chat_type = g.redis.hget('chat.'+request.form['chat']+'.meta', 'type')
    if chat_type not in ['unsaved', 'saved']:
        abort(400)
    log_id = archive_chat(g.redis, g.mysql, request.form['chat'])
    g.redis.hset('chat.'+request.form['chat']+'.meta', 'type', 'saved')
    g.redis.zadd('archive-queue', request.form['chat'], get_time(ARCHIVE_PERIOD))
    if 'tumblr' in request.form:
        # Set the character list as tags.
        tags = g.redis.smembers('chat.'+request.form['chat']+'.characters')
        tags.add('msparp')
        url_tags = urllib.quote_plus(','.join(tags))
        return redirect('http://www.tumblr.com/new/link?post[one]=Check+out+this+chat+I+just+had+on+MSPARP!&post[two]=http%3A%2F%2Funsupported.msparp.com%2Flogs%2F'+str(log_id)+'&post[source_url]=http%3A%2F%2Fmsparp.com%2F&tags='+url_tags)
    return redirect(url_for('view_log', chat=request.form['chat']))

@app.route('/logs/group/<chat>')
def old_view_log(chat):
    return redirect(url_for('view_log', chat=chat))

@app.route('/logs/<log_id>')
def view_log_by_id(log_id=None):
    try:
        log_id = int(log_id)
    except ValueError:
        abort(400)
    try:
        log = g.mysql.query(Log).filter(Log.id==log_id).one()
    except NoResultFound:
        abort(404)
    if log.url is not None:
        return redirect(url_for('view_log', chat=log.url))
    abort(404)

@app.route('/chat/<chat>/log')
def view_log(chat=None):

    # Decide whether or not to put a continue link in.
    continuable = g.redis.hget('chat.'+chat+'.meta', 'type') is not None

    try:
        log = g.mysql.query(Log).filter(Log.url==chat).one()
    except:
        abort(404)

    current_page = request.args.get('page') or log.page_count
    mode = request.args.get('mode') or 'normal'

    try:
        log_page = g.mysql.query(LogPage).filter(and_(LogPage.log_id==log.id, LogPage.number==current_page)).one()
    except NoResultFound:
        abort(404)

    url_generator = paginate.PageURL(url_for('view_log', chat=chat), {'page': current_page})

    # It's only one row per page and we want to fetch them via both log id and
    # page number rather than slicing, so we'll just give it an empty list and
    # override the count.
    paginator = paginate.Page([], page=current_page, items_per_page=1, item_count=log.page_count, url=url_generator)

    # Pages end with a line break, so the last line is blank.
    lines = log_page.content.split('\n')[0:-1]
    lines = map(lambda _: parse_line(_, 0), lines)

    for line in lines:
        line['datetime'] = datetime.datetime.fromtimestamp(line['timestamp'])

    return render_template('log.html',
        chat=chat,
        lines=lines,
        continuable=continuable,
        current_page=current_page,
        mode=mode,
        paginator=paginator
    )

# Globalmod

@app.route('/chat/<chat>/unban', methods=['GET', 'POST'])
def unbanPage(chat=None):
    if chat is None:
        abort(403)

    result = None

    if g.redis.sismember('global-mods', g.user.session_id):
        pass
    else:
        return render_template('admin_denied.html')

    if "ip" in request.form:
        unbanIP = request.form['ip']
        banstring = "%s/%s" % (chat, unbanIP)
        g.redis.hdel("ban-reasons", banstring)
        g.redis.zrem("ip-bans", banstring)
        result = "Unbanned %s!" % (unbanIP)

    banlist = g.redis.zrange("ip-bans", "0", "-1")
    bans = []
    for x in banlist:
        if x.split("/")[0] == chat:
            bans.append(x)

    return render_template('admin_unban.html',
        lines=bans,
        result=result,
        chat=chat,
        page='unban'
    )

@app.route('/chat/<chat>/mods')
def manageMods(chat):
    chat_session = g.redis.hgetall("session."+g.user.session_id+".meta."+chat)
    if "group" not in chat_session or chat_session['group'] != 'globalmod':
        return render_template('admin_denied.html')
    counters = g.redis.hgetall("chat."+chat+".counters")
    mods = []
    if request.args.get('showusers', None) is not None:
        show = ('globalmod', 'mod', 'mod2', 'mod3', 'user')
    else:
        show = ('globalmod', 'mod', 'mod2', 'mod3')
    for counter, session_id in counters.items():
        group = g.redis.hget("session."+session_id+".meta."+chat, 'group')
        if group in show:
            data = g.redis.hgetall("session."+session_id+".chat."+chat)
            name = data.get('name', CHARACTER_DETAILS[data['character']]['name'])
            acronym = data.get('acronym', CHARACTER_DETAILS[data['character']]['acronym'])
            is_you = session_id == g.user.session_id
            #[0] = Counter [1] = Group [2] = Name [3] = Acronym [4] = is_you
            mods.append((counter, group, name, acronym, is_you))
    mods.sort(key=lambda tup: int(tup[0]))
    return render_template(
        'chatmods.html',
        modstatus=mods,
        chat=chat,
        page='mods',
    )

@app.route("/admin/changemessages", methods=['GET', 'POST'])
def change_messages():

    if not g.redis.sismember('global-admins', g.user.session_id):
        return render_template('admin_denied.html')

    if 'welcome_text' in request.form:
        welcome_text = request.form['welcome_text']
        g.redis.set('welcome_text', welcome_text)
        updates_text = request.form['updates_text']
        g.redis.set('updates_text', updates_text)
        chat_links = request.form['chat_links']
        g.redis.set('chat_links', chat_links)

    welcome_text = (g.redis.get('welcome_text') or "").decode("utf8")
    updates_text = (g.redis.get('updates_text') or "").decode("utf8")
    chat_links = (g.redis.get('chat_links') or "").decode("utf8")

    return render_template('admin_changemsg.html',
        welcome_text=welcome_text,
        updates_text=updates_text,
        chat_links=chat_links,
        page="changemsg",
    )

@app.route("/admin/broadcast", methods=['GET', 'POST'])
def global_broadcast():
    result = None

    if not g.redis.sismember('global-admins', g.user.session_id):
        return render_template('admin_denied.html')

    if 'line' in request.form:
        color = request.form.get('color', "000000")
        line = request.form.get('line', None)
        confirm = bool(request.form.get('confirm', False))

        if confirm is True:
            if line in ('\n', '\r\n', '', ' '):
                result = '<div class="alert alert-danger"> <strong> Global cannot be blank! </strong> </div>'
            else:
                pipe = g.redis.pipeline()
                chats = set()
                chat_sessions = g.redis.zrange('chats-alive', 0, -1)
                for chat_session in chat_sessions:
                    chat, user = chat_session.split("/")
                    chats.add(chat)
                message = {
                    "messages": [
                        {
                            "color": color,
                            "timestamp": 0,
                            "counter": -123,
                            "type": "global",
                            "line": line
                        }
                    ]
                }

                for chat in chats:
                    message['messages'][0]['id'] = g.redis.llen("chat."+chat)-1
                    pipe.publish("channel."+chat, json.dumps(message))

                pipe.execute()
                result = '<div class="alert alert-success"> <strong> Global sent! </strong> <br> %s </div>' % (line)
        else:
            result = '<div class="alert alert-danger"> <strong> Confirm checkbox not checked. </strong> </div>'

    return render_template('admin_globalbroadcast.html',
        result=result,
        page="broadcast",
    )


@app.route('/admin/allbans', methods=['GET', 'POST'])
def admin_allbans():
    sort = request.args.get('sort', None)
    result = None

    if g.redis.sismember('global-admins', g.user.session_id):
        pass
    else:
        return render_template('admin_denied.html')

    if "ip" in request.form and "chat" in request.form:
        chat = request.form['chat']
        unbanIP = request.form['ip']
        banstring = "%s/%s" % (chat, unbanIP)
        g.redis.hdel("ban-reasons", banstring)
        g.redis.zrem("ip-bans", banstring)
        result = "Unbanned %s!" % (unbanIP)

    raw_bans = g.redis.zrange("ip-bans", 0, -1, withscores=True)
    ban_reasons = g.redis.hgetall('ban-reasons')

    bans = []
    for chat_ip, expiry in raw_bans:
        chat, ip = chat_ip.split('/')
        bans.append((
            chat, ip,
            datetime.datetime.fromtimestamp(expiry - 2592000),
            ban_reasons.get(chat_ip, '').decode('utf-8'),
        ))

    if sort == 'chat':
        bans.sort(key=lambda tup: tup[0])
        sort = 'chat'
    elif sort == 'ip':
        bans.sort(key=lambda tup: inet_aton(tup[1]))
        sort = 'ip'
    else:
        sort = 'date'

    return render_template('global_allbans.html',
        bans=bans,
        result=result,
        page='allbans',
        sort=sort
    )

@app.route('/admin/globalban', methods=['GET', 'POST'])
def admin_globalban():
    result = None

    if not g.redis.sismember('global-admins', g.user.session_id):
        return render_template('admin_denied.html')

    if "ip" in request.form:
        banIP = request.form['ip']
        banReason = request.form.get("reason", "No reason.")
        action = request.form.get("action", None)

        if action == "ban":
            g.redis.hset("global-bans", banIP, banReason)
            result = "Globally banned %s!" % (banIP)
        elif action == "unban":
            g.redis.hdel("global-bans", banIP)
            result = "Globally unbanned %s!" % (banIP)

    bans = g.redis.hgetall('global-bans')

    return render_template('global_globalban.html',
        bans=bans,
        result=result,
        page="globalban"
    )

@app.route('/admin/panda', methods=['GET', 'POST'])
def admin_panda():
    result = None
    if not g.redis.sismember('global-admins', g.user.session_id):
        return render_template('admin_denied.html')

    if "ip" in request.form:
        ip = request.form['ip']
        action = request.form.get("action", None)
        reason = request.form.get("reason", "No reason.")

        if action == "add":
            g.redis.hset("punish-scene", ip, reason)
            result = "Panda added on %s!" % (ip)
        elif action == "remove":
            g.redis.hdel("punish-scene", ip)
            result = "Panda removed on %s!" % (ip)

    pandas = g.redis.hgetall('punish-scene')

    return render_template('global_globalpanda.html',
        lines=pandas,
        result=result,
        page="panda"
    )


@app.route('/health', methods=['GET'])
def doHealthCheck():
    # should probably actually DO a health check here
    return 'ok'
    
# Redirects 

@app.route("/faq")
def faq():
    return requests.get("http://www.dlh-digital.com/msparpfaq.html").text

@app.route("/bbcode")
def bbcode():
    return requests.get("http://www.dlh-digital.com/bbcode.html").text

@app.route("/userguide")
def userguide():
    return requests.get("http://www.dlh-digital.com/userguide.html").text

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

