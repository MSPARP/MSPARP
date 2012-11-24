from functools import wraps
from flask import Flask, g, request, render_template, make_response, jsonify, abort

from lib import PING_PERIOD, ARCHIVE_PERIOD, get_time
from lib.api import ping, change_state, disconnect, get_online_state
from lib.characters import CHARACTER_DETAILS
from lib.messages import send_message, get_userlists, hide_silence, parse_messages
from lib.requests import populate_all_chars, connect_redis, create_chat_session, set_cookie, disconnect_redis

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
    if g.user.meta['group']=='mod':
        # Moderator messages.
        wanted_channels.add(channel_mod)
    if g.user.meta['group']=='silent':
        # Channel for self messages if silent.
        wanted_channels.add(channel_self)
    return wanted_channels

# Decorators

def mark_alive(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if ping(g.redis, request.form['chat'], g.user, g.chat_type):
            g.fake_join_message = True
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
        if g.user.meta['group']=='silent':
            send_message(g.redis, chat, g.user.meta['counter'], 'private', line, g.user.character['color'], g.user.character['acronym'], g.user.session_id)
        else:
            send_message(g.redis, chat, g.user.meta['counter'], 'message', line, g.user.character['color'], g.user.character['acronym'])
    if 'state' in request.form and request.form['state'] in ['online', 'idle']:
        change_state(g.redis, chat, g.user.session_id, request.form['state'])
    if 'set_group' in request.form and 'counter' in request.form:
        if g.user.meta['group']=='mod':
            set_group = request.form['set_group']
            set_session_id = g.redis.hget('chat.'+chat+'.counters', request.form['counter']) or abort(400)
            ss_key = 'session.'+set_session_id+'.chat.'+chat
            ss_meta_key = 'session.'+set_session_id+'.meta.'+chat
            current_group = g.redis.hget(ss_meta_key, 'group')
            if current_group!=set_group and set_group in ['user', 'mod', 'silent']:
                g.redis.hset(ss_meta_key, 'group', set_group)
                set_message = None
                # Convert the name and acronym to unicode.
                ss_character = g.redis.hget(ss_key, 'character')
                set_session_name = unicode(
                    g.redis.hget(ss_key, 'name') or CHARACTER_DETAILS[ss_character]['name'],
                    encoding='utf8'
                )
                set_session_acronym = unicode(
                    g.redis.hget(ss_key, 'acronym') or CHARACTER_DETAILS[ss_character]['acronym'],
                    encoding='utf8'
                )
                if current_group!='mod' and set_group=='mod':
                    set_message = '%s [%s] gave moderator status to %s [%s].' % (
                        g.user.character['name'],
                        g.user.character['acronym'],
                        set_session_name,
                        set_session_acronym
                    )
                elif current_group=='mod' and set_group!='mod':
                    set_message = '%s [%s] removed moderator status from %s [%s].' % (
                        g.user.character['name'],
                        g.user.character['acronym'],
                        set_session_name,
                        set_session_acronym
                    )
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
            'line': '%s [%s] joined chat.' % (g.user.character['name'], g.user.character['acronym'])
        } ] }
    else:
        # Check for stored messages.
        messages = g.redis.lrange('chat.'+chat, after+1, -1)
        if messages:
            message_dict = {
                'messages': parse_messages(messages, after+1)
            }

    if message_dict:
        message_dict['online'], message_dict['idle'], silent_users = get_userlists(g.redis, chat)
        if silent_users is True and g.user.meta['group']!='mod':
            hide_silence(message_dict['online'], message_dict['idle'])
        return jsonify(message_dict)

    # Otherwise, listen for a message.

    # Channel names.
    channel_main = 'channel.'+chat
    channel_mod = channel_main+'.mod'
    channel_self = channel_main+'.'+g.user.session_id
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
                if refresh_user==g.user.session_id:
                    # Our group has changed. Alter wanted channels accordingly.
                    g.user.meta['group'] = refresh_group
                    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)
            elif msg['channel'] in wanted_channels:
                # The pubsub channel sends us a JSON string, so we return that instead of using jsonify.
                resp = make_response(msg['data'])
                resp.headers['Content-type'] = 'application/json'
                return resp

@app.route('/quit', methods=['POST'])
def quitChatting():
    disconnect_message = '%s [%s] disconnected.' % (g.user.character['name'], g.user.character['acronym']) if g.user.meta['group']!='silent' else None
    disconnect(g.redis, request.form['chat'], g.user.session_id, disconnect_message)
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

