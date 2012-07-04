import itertools, re, time

from functools import wraps
from flask import Flask, g, request, render_template, make_response, redirect, url_for, jsonify, abort
from uuid import uuid4
from collections import defaultdict
from werkzeug.routing import BaseConverter, ValidationError

from lib import get_time, validate_chat_url
from lib.characters import CHARACTER_GROUPS, CHARACTERS
from lib.messages import send_message, get_user_list, parse_line, parse_messages
from lib.requests import connect, set_cookie
from lib.sessions import get_counter


class ChatIDConverter(BaseConverter):

    def __init__(self, url_map):
        super(ChatIDConverter, self).__init__(url_map)

    def to_python(self, value):
        if re.match('^[-a-zA-Z0-9]+$',value):
            return value
        else:
            raise ValidationError()

    def to_url(self, value):
        return value

app = Flask(__name__)
app.url_map.converters['chat'] = ChatIDConverter

# Pre and post request stuff.
app.before_request(connect)
app.after_request(set_cookie)

# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        character_dict=g.user.character_dict(unpack_replacements=True),
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character,
        users_searching=g.db.zcard('searchers'),
        users_chatting=g.db.scard('sessions-chatting')
    )

def get_wanted_channels(channel_main, channel_mod, channel_self):
    wanted_channels = set()
    wanted_channels.add(channel_main)
    if g.user.group=='mod':
        # Moderator messages.
        wanted_channels.add(channel_mod)
    if g.user.group=='silent':
        # Channel for self messages if silent.
        wanted_channels.add(channel_self)
    return wanted_channels

# Decorators

def validate_chat(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'chat' in request.form and validate_chat_url(request.form['chat']):
            return f(*args, **kwargs)
        abort(400)
    return decorated_function

def mark_alive(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        chat = request.form['chat']
        state_key = 'chat.%s.sessions' % chat
        session_state = g.db.hget(state_key, g.user.session)
        if session_state is None:
            # This session has never been in this chat before; we need to add them to the counter.
            g.db.rpush('chat.%s.counter' % chat, g.user.session)
            g.db.sadd('session.%s.chats' % g.user.session, chat)
        if session_state not in ['online', 'away']:
            g.db.hset(state_key, g.user.session, 'online')
            if g.user.group=='silent':
                join_message = None
                g.fake_join_message = True
            else:
                join_message = '%s [%s] joined chat.' % (g.user.name, g.user.acronym)
            send_message(g.db, chat, 'user_change', join_message)
            g.db.sadd('sessions-chatting', g.user.session)
        g.db.zadd('chats-alive', chat+'/'+g.user.session, get_time())
        return f(*args, **kwargs)
    return decorated_function

# Chat

@app.route('/chat')
@app.route('/chat/<chat:chat>')
def chat(chat=None):

    # Delete value from the matchmaker.
    if g.db.get('session.'+g.user.session+'.match'):
        g.db.delete('session.'+g.user.session+'.match')

    if chat is None:
        existing_lines = []
        latest_num = -1
    else:
        existing_lines = [parse_line(line, 0) for line in g.db.lrange('chat.'+chat, 0, -1)]
        latest_num = len(existing_lines)-1
    print "LATEST_NUM"
    print latest_num

    return render_template(
        'chat.html',
        user=g.user,
        character_dict=g.user.character_dict(unpack_replacements=True),
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        chat=chat,
        lines=existing_lines,
        latest_num=latest_num
    )

@app.route('/post', methods=['POST'])
@validate_chat
@mark_alive
def postMessage():
    chat = request.form['chat']
    if 'line' in request.form:
        if g.user.group=='silent':
            send_message(g.db, chat, 'private', request.form['line'], g.user.color, g.user.acronym, g.user.session)
        else:
            send_message(g.db, chat, 'message', request.form['line'], g.user.color, g.user.acronym)
    if 'state' in request.form and request.form['state'] in ['online', 'away']:
        current_state = g.db.hget('chat.%s.sessions' % chat, g.user.session)
        if request.form['state']!=current_state:
            g.db.hset('chat.%s.sessions' % chat, g.user.session, request.form['state'])
            if request.form['state']=='away':
                send_message(g.db, chat, 'user_change')
            else:
                send_message(g.db, chat, 'user_change')
    if 'set_group' in request.form and 'counter' in request.form:
        if g.user.group=='mod':
            set_group = request.form['set_group']
            set_session_id = g.db.lindex('chat.%s.counter' % chat, request.form['counter']) or abort(400)
            set_session_key = 'session.%s.chat.%s' % (set_session_id, chat)
            set_session = g.db.hgetall(set_session_key)
            if set_session['group']!=set_group and set_group in ['user', 'mod', 'silent']:
                g.db.hset(set_session_key, 'group', set_group)
                set_message = None
                # Convert the name and acronym to unicode.
                set_session['name'] = unicode(set_session['name'], encoding='utf8')
                set_session['acronym'] = unicode(set_session['acronym'], encoding='utf8')
                if set_session['group']!='mod' and set_group=='mod':
                    set_message = '%s [%s] gave moderator status to %s [%s].' % (g.user.name, g.user.acronym, set_session['name'], set_session['acronym'])
                elif set_session['group']=='mod' and set_group!='mod':
                    set_message = '%s [%s] removed moderator status from %s [%s].' % (g.user.name, g.user.acronym, set_session['name'], set_session['acronym'])
                # Refresh the user's subscriptions.
                g.db.publish('channel.'+chat+'.refresh', set_session_id+'#'+set_group)
                send_message(g.db, chat, 'user_change', set_message)
        else:
            abort(403)
    return 'ok'

@app.route('/ping', methods=['POST'])
@validate_chat
@mark_alive
def pingServer():
    return 'ok'

@app.route('/messages', methods=['POST'])
@validate_chat
@mark_alive
def getMessages():

    chat = request.form['chat']
    after = int(request.form['after'])

    message_dict = None

    if hasattr(g, 'fake_join_message'):
        message_dict = { 'messages': [ {
            'id': after,
            'color': '000000',
            'line': '%s [%s] joined chat.' % (g.user.name, g.user.acronym)
        } ] }
    else:
        # Check for stored messages.
        messages = g.db.lrange('chat.'+chat, after+1, -1)
        if messages:
            message_dict = {
                'messages': parse_messages(messages, after+1)
            }

    if message_dict:
        message_dict['online'] = get_user_list(g.db, chat, 'mod' if g.user.group=='mod' else 'user')
        if 'fetchCounter' in request.form:
            message_dict['counter'] = get_counter(chat, g.user.session)
        return jsonify(message_dict)

    # Otherwise, listen for a message.

    # Channel names.
    channel_main = 'channel.'+chat
    channel_mod = channel_main+'.mod'
    channel_self = channel_main+'.'+g.user.session
    channel_refresh = channel_main+'.refresh'

    # We subscribe to all four channels then ignore what we don't want because
    # changing subscriptions doesn't happen quickly enough and we end up missing
    # messages.
    g.db.subscribe(channel_main)
    g.db.subscribe(channel_mod)
    g.db.subscribe(channel_self)
    g.db.subscribe(channel_refresh)

    # This gives us a list of all the channels we want to listen to.
    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)

    for msg in g.db.listen():
        if msg['type']=='message':
            if msg['channel']==channel_refresh:
                refresh_user, refresh_group = msg['data'].split('#', 1)
                if refresh_user==g.user.session:
                    # Our group has changed. Alter wanted channels accordingly.
                    g.user.group = refresh_group
                    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)
            elif msg['channel'] in wanted_channels:
                # The pubsub channel sends us a JSON string, so we return that instead of using jsonify.
                resp = make_response(msg['data'])
                resp.headers['Content-type'] = 'application/json'
                return resp

@app.route('/bye', methods=['POST'])
@validate_chat
def quitChatting():
    # Check if they're actually a member of the chat first?
    chatkey = 'chat.%s.sessions' % request.form['chat']
    if g.db.hexists(chatkey, g.user.session):
        g.db.zrem('chats-alive', request.form['chat']+'/'+g.user.session)
        g.db.hset(chatkey, g.user.session, 'offline')
        g.db.srem('sessions-chatting', g.user.session)
        disconnect_message = '%s [%s] disconnected.' % (g.user.name, g.user.acronym) if g.user.group!='silent' else None
        send_message(g.db, request.form['chat'], 'user_change', disconnect_message)
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
            if g.db.exists('chat.'+chat):
                raise ValueError('chaturl_taken')
            if not re.match('^[-a-zA-Z0-9]+$', chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
            g.user.set_group('mod')
            g.db.set('chat.'+chat+'.type', 'group')
            return redirect(url_for('chat', chat=chat))
    except ValueError as e:
        if request.is_xhr:
            abort(400)
        else:
            return show_homepage(e.args[0])

    if request.is_xhr:
        return 'ok'
    elif 'search' in request.form:
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('configure'))

# Searching

@app.route('/search', methods=['POST'])
def foundYet():
    target=g.db.get('session.'+g.user.session+'.match')
    if target:
        return jsonify(target=target)
    else:
        g.db.zadd('searchers', g.user.session, get_time())
        abort(404)

@app.route('/stop_search', methods=['POST'])
def quitSearching():
    g.db.zrem('searchers', g.user.session)
    return 'ok'

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

