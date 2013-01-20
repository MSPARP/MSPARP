try:
    import ujson as json
except:
    import json
import urllib
from flask import Flask, g, request, render_template, redirect, url_for, jsonify, abort
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from webhelpers import paginate

from lib import SEARCH_PERIOD, ARCHIVE_PERIOD, get_time, validate_chat_url
from lib.archive import archive_chat, get_or_create_log
from lib.characters import CHARACTER_GROUPS, CHARACTERS
from lib.messages import parse_line
from lib.model import Log, LogPage
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
        case_options=CASE_OPTIONS,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character['character'],
        users_searching=g.redis.zcard('searchers'),
        users_chatting=g.redis.scard('sessions-chatting')
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
        if 'character' in request.form:
            g.user.save_character(request.form)
        if 'save_pickiness' in request.form:
            g.user.save_pickiness(request.form)
        if 'create' in request.form:
            chat = request.form['chaturl']
            if g.redis.exists('chat.'+chat):
                raise ValueError('chaturl_taken')
            # USE VALIDATE_CHAT_URL
            if not validate_chat_url(chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
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

    return render_template('log.html',
        chat=chat,
        lines=lines,
        continuable=continuable,
        paginator=paginator
    )

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

