from functools import wraps
from flask import Flask, g, request, render_template, make_response, jsonify, abort

from lib import PING_PERIOD, ARCHIVE_PERIOD, get_time
from lib.characters import CHARACTER_DETAILS
from lib.messages import send_message, get_user_list, parse_messages
from lib.requests import populate_all_chars, connect_redis, create_chat_session, set_cookie, disconnect_redis
from lib.sessions import get_counter

app = Flask(__name__)

# Pre and post request stuff
app.before_first_request(populate_all_chars)
app.before_request(connect_redis)
app.before_request(create_chat_session)
app.after_request(set_cookie)
app.after_request(disconnect_redis)

# Helper functions

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

def mark_alive(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        chat = request.form['chat']
        state_key = 'chat.%s.sessions' % chat
        session_state = g.redis.hget(state_key, g.user.session)
        if session_state is None:
            # This session has never been in this chat before; we need to add them to the counter.
            g.redis.rpush('chat.%s.counter' % chat, g.user.session)
            g.redis.sadd('session.%s.chats' % g.user.session, chat)
        if session_state not in ['online', 'away']:
            # Remove from the delete queue and add to the archive queue.
            g.redis.zrem('delete-queue', chat)
            if g.redis.zscore('archive-queue', chat) is None:
                g.redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))
            # Set user state.
            g.redis.hset(state_key, g.user.session, 'online')
            if g.user.group=='silent':
                join_message = None
                g.fake_join_message = True
            else:
                join_message = '%s [%s] joined chat.' % (g.user.name, g.user.acronym)
            send_message(g.redis, chat, -1, 'user_change', join_message)
            g.redis.sadd('sessions-chatting', g.user.session)
            # Add character to chat character list.
            g.redis.sadd('chat.'+chat+'.characters', g.user.character)
        g.redis.zadd('chats-alive', chat+'/'+g.user.session, get_time(PING_PERIOD*2))
        return f(*args, **kwargs)
    return decorated_function

# Views

@app.route('/post', methods=['POST'])
@mark_alive
def postMessage():
    chat = request.form['chat']
    if 'line' in request.form:
        # Remove linebreaks and truncate to 1500 characters.
        line = request.form['line'].replace('\n', ' ')[:1500]
        counter = get_counter(chat, g.user.session)
        if g.user.group=='silent':
            send_message(g.redis, chat, counter, 'private', line, g.user.color, g.user.acronym, g.user.session)
        else:
            send_message(g.redis, chat, counter, 'message', line, g.user.color, g.user.acronym)
    if 'state' in request.form and request.form['state'] in ['online', 'away']:
        current_state = g.redis.hget('chat.%s.sessions' % chat, g.user.session)
        if request.form['state']!=current_state:
            g.redis.hset('chat.%s.sessions' % chat, g.user.session, request.form['state'])
            if request.form['state']=='away':
                send_message(g.redis, chat, -1, 'user_change')
            else:
                send_message(g.redis, chat, -1, 'user_change')
    if 'set_group' in request.form and 'counter' in request.form:
        if g.user.group=='mod':
            set_group = request.form['set_group']
            set_session_id = g.redis.lindex('chat.%s.counter' % chat, request.form['counter']) or abort(400)
            set_session_key = 'session.%s.chat.%s' % (set_session_id, chat)
            set_session = g.redis.hgetall(set_session_key)
            if set_session['group']!=set_group and set_group in ['user', 'mod', 'silent']:
                g.redis.hset(set_session_key, 'group', set_group)
                set_message = None
                # Convert the name and acronym to unicode.
                set_session_name = unicode(set_session.get('name') or CHARACTER_DETAILS[set_session['character']]['name'], encoding='utf8')
                set_session_acronym = unicode(set_session.get('acronym') or CHARACTER_DETAILS[set_session['character']]['acronym'], encoding='utf8')
                if set_session['group']!='mod' and set_group=='mod':
                    set_message = '%s [%s] gave moderator status to %s [%s].' % (g.user.name, g.user.acronym, set_session_name, set_session_acronym)
                elif set_session['group']=='mod' and set_group!='mod':
                    set_message = '%s [%s] removed moderator status from %s [%s].' % (g.user.name, g.user.acronym, set_session_name, set_session_acronym)
                # Refresh the user's subscriptions.
                g.redis.publish('channel.'+chat+'.refresh', set_session_id+'#'+set_group)
                send_message(g.redis, chat, -1, 'user_change', set_message)
        else:
            abort(403)
    return 'ok'

@app.route('/ping', methods=['POST'])
@mark_alive
def pingServer():
    return 'ok'

@app.route('/messages', methods=['POST'])
@mark_alive
def getMessages():

    chat = request.form['chat']
    after = int(request.form['after'])

    message_dict = None

    if hasattr(g, 'fake_join_message'):
        message_dict = { 'messages': [ {
            'id': after,
            'timestamp': get_time(),
            'counter': -1,
            'color': '000000',
            'line': '%s [%s] joined chat.' % (g.user.name, g.user.acronym)
        } ] }
    else:
        # Check for stored messages.
        messages = g.redis.lrange('chat.'+chat, after+1, -1)
        if messages:
            message_dict = {
                'messages': parse_messages(messages, after+1)
            }

    if message_dict:
        message_dict['online'] = get_user_list(g.redis, chat, 'mod' if g.user.group=='mod' else 'user')
        if 'fetchCounter' in request.form:
            message_dict['counter'] = get_counter(chat, g.user.session)
        return jsonify(message_dict)

    # Otherwise, listen for a message.

    # Channel names.
    channel_main = 'channel.'+chat
    channel_mod = channel_main+'.mod'
    channel_self = channel_main+'.'+g.user.session
    channel_refresh = channel_main+'.refresh'

    pubsub = g.redis.pubsub()

    # We subscribe to all four channels then ignore what we don't want because
    # changing subscriptions doesn't happen quickly enough and we end up missing
    # messages.
    pubsub.subscribe(channel_main)
    pubsub.subscribe(channel_mod)
    pubsub.subscribe(channel_self)
    pubsub.subscribe(channel_refresh)

    # This gives us a list of all the channels we want to listen to.
    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)

    for msg in pubsub.listen():
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

@app.route('/quit', methods=['POST'])
def quitChatting():
    # Check if they're actually a member of the chat first?
    chatkey = 'chat.%s.sessions' % request.form['chat']
    if g.redis.hexists(chatkey, g.user.session):
        g.redis.zrem('chats-alive', request.form['chat']+'/'+g.user.session)
        g.redis.hset(chatkey, g.user.session, 'offline')
        g.redis.srem('sessions-chatting', g.user.session)
        disconnect_message = '%s [%s] disconnected.' % (g.user.name, g.user.acronym) if g.user.group!='silent' else None
        send_message(g.redis, request.form['chat'], -1, 'user_change', disconnect_message)
        return 'ok'

@app.route('/save', methods=['POST'])
def save():
    try:
        g.user.save_character(request.form)
    except ValueError as e:
        abort(400)
    return 'ok'

if __name__ == "__main__":
    app.run(port=9000, debug=True)

