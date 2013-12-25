try:
    import ujson as json
except:
    import json
import datetime, urllib
from flask import Flask, g, request, render_template, redirect, url_for, jsonify, abort
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from time import mktime
from webhelpers import paginate

from lib import SEARCH_PERIOD, ARCHIVE_PERIOD, OUBLIETTE_ID, get_time, validate_chat_url
from lib.archive import archive_chat, get_or_create_log
from lib.characters import CHARACTER_DETAILS, GROUP_DETAILS, SORTED_CHARACTERS, SORTED_GROUPS
from lib.messages import parse_line
from lib.model import Chat, ChatSession, Log, LogPage
from lib.requests import populate_all_chars, connect_redis, connect_mysql, create_normal_session, set_cookie, disconnect_redis, disconnect_mysql
from lib.sessions import CASE_OPTIONS

app = Flask(__name__)

# Pre and post request stuff
app.before_first_request(populate_all_chars)
app.before_request(connect_redis)
app.before_request(connect_mysql)
app.before_request(create_normal_session)
app.after_request(set_cookie)
app.after_request(disconnect_redis)
app.after_request(disconnect_mysql)

# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        replacements=json.loads(g.user.character['replacements']),
        regexes=json.loads(g.user.character['regexes']),
        picky=g.redis.smembers(g.user.prefix+'.picky') or set(),
        picky_groups=g.redis.smembers(g.user.prefix+'.picky-groups') or set(),
        picky_exclude=g.redis.smembers(g.user.prefix+'.picky-exclude') or set(),
        picky_exclude_groups=g.redis.smembers(g.user.prefix+'.picky-exclude-groups') or set(),
        picky_options=g.redis.hgetall(g.user.prefix+'.picky-options') or {},
        case_options=CASE_OPTIONS,
        character_details=CHARACTER_DETAILS,
        group_details=GROUP_DETAILS,
        sorted_characters=SORTED_CHARACTERS,
        sorted_groups=SORTED_GROUPS,
        default_char=g.user.character['character'],
        users_searching=g.redis.zcard('searchers'),
        users_chatting=g.redis.scard('sessions-chatting')
    )

# Chat

@app.route('/chat')
@app.route('/chat/<chat_url>')
def chat(chat_url=None):

    if chat_url is None:
        chat_meta = { 'type': 'unsaved' }
        existing_lines = []
        latest_num = -1
    else:
        if g.redis.zrank('ip-bans', chat_url+'/'+request.environ['HTTP_X_REAL_IP']) is not None:
            chat_url = OUBLIETTE_ID
        # Check if chat exists
        chat_meta = g.redis.hgetall('chat.'+chat_url+'.meta')
        # Convert topic to unicode.
        if 'topic' in chat_meta.keys():
            chat_meta['topic'] = unicode(chat_meta['topic'], encoding='utf8')
        # Try to load the chat from mysql if it doesn't exist in redis.
        if len(chat_meta)==0:
            try:
                mysql_log = g.mysql.query(Log).filter(Log.url==chat_url).one()
                mysql_chat = g.mysql.query(Chat).filter(Chat.log_id==mysql_log.id).one()
                chat_meta = {
                    "type": mysql_chat.type,
                    "counter": mysql_chat.counter,
                }
                if mysql_chat.topic is not None and mysql_chat.topic!="":
                    chat_meta["topic"] = mysql_chat.topic
                g.redis.hmset('chat.'+chat_url+'.meta', chat_meta)
                for mysql_session in g.mysql.query(ChatSession).filter(ChatSession.log_id==mysql_log.id):
                    g.redis.hset('chat.'+chat_url+'.counters', mysql_session.counter, mysql_session.session_id)
                    g.redis.hmset('session.'+mysql_session.session_id+'.meta.'+chat_url, {
                        "counter": mysql_session.counter,
                        "group": mysql_session.group,
                    })
                    g.redis.hmset('session.'+mysql_session.session_id+'.chat.'+chat_url, {
                        "character": mysql_session.character,
                        "name": mysql_session.name,
                        "acronym": mysql_session.acronym,
                        "color": mysql_session.color,
                        "case": mysql_session.case,
                        "replacements": mysql_session.replacements,
                        "regexes": mysql_session.regexes,
                        "quirk_prefix": mysql_session.quirk_prefix,
                        "quirk_suffix": mysql_session.quirk_suffix,
                    })
                    g.redis.sadd('session.'+mysql_session.session_id+'.chats', chat_url)
                    g.redis.zadd('chat-sessions', chat_url+'/'+mysql_session.session_id, mktime(mysql_session.expiry_time.timetuple()))
            except NoResultFound:
                abort(404)
        # Make sure it's in the archive queue.
        if g.redis.zscore('archive-queue', chat_url) is None:
            g.redis.zadd('archive-queue', chat_url, get_time(ARCHIVE_PERIOD))
        # Load chat-based session data.
        g.user.set_chat(chat_url)
        existing_lines = [parse_line(line, 0) for line in g.redis.lrange('chat.'+chat_url, 0, -1)]
        latest_num = len(existing_lines)-1

    return render_template(
        'chat.html',
        user=g.user,
        character_dict=g.user.json_info(),
        case_options=CASE_OPTIONS,
        character_details=CHARACTER_DETAILS,
        sorted_characters=SORTED_CHARACTERS,
        chat=chat_url,
        chat_meta=chat_meta,
        lines=existing_lines,
        latest_num=latest_num
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
        g.user.save_character(request.form)
        g.user.save_pickiness(request.form)
        if 'create' in request.form:
            chat = request.form['chaturl']
            if g.redis.exists('chat.'+chat):
                raise ValueError('chaturl_taken')
            # USE VALIDATE_CHAT_URL
            if not validate_chat_url(chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
            if g.user.meta['group']!='globalmod':
                g.user.set_group('mod')
            g.redis.hset('chat.'+chat+'.meta', 'type', 'group')
            get_or_create_log(g.redis, g.mysql, chat, 'group')
            g.mysql.commit()
            return redirect(url_for('chat', chat_url=chat))
    except ValueError as e:
        return show_homepage(e.args[0])
    return redirect(url_for('chat'))

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
        return redirect('http://www.tumblr.com/new/link?post[one]=Check+out+this+chat+I+just+had+on+MSPARP!&post[two]=http%3A%2F%2Fmsparp.com%2Flogs%2F'+str(log_id)+'&post[source_url]=http%3A%2F%2Fmsparp.com%2F&tags='+url_tags)
    return redirect(url_for('view_log', chat=request.form['chat']))

@app.route('/logs/group/<chat>')
def old_view_log(chat):
    return redirect(url_for('view_log', chat=chat))

@app.route('/logs/<log_id>')
def view_log_by_id(log_id=None):
    log = g.mysql.query(Log).filter(Log.id==log_id).one()
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

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True, host='0.0.0.0')

