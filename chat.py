from functools import wraps
from flask import Flask, g, request, render_template, make_response, jsonify, abort

from lib import PING_PERIOD, ARCHIVE_PERIOD, IP_BAN_PERIOD, CHAT_FLAGS, get_time
from lib.api import ping, change_state, disconnect, get_online_state
from lib.characters import CHARACTER_DETAILS
from lib.groups import MOD_GROUPS, GROUP_RANKS, MINIMUM_RANKS
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
    if g.user.meta['group'] in MOD_GROUPS:
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
    # Mod options.
    if g.user.meta['group'] in MOD_GROUPS:
        if 'set_group' in request.form and 'counter' in request.form:
            set_group = request.form['set_group']
            set_session_id = g.redis.hget('chat.'+chat+'.counters', request.form['counter']) or abort(400)
            ss_key = 'session.'+set_session_id+'.chat.'+chat
            ss_meta_key = 'session.'+set_session_id+'.meta.'+chat
            current_group = g.redis.hget(ss_meta_key, 'group')
            # You can't promote people to or demote people from a group higher than your own.
            if (
                GROUP_RANKS[current_group]>GROUP_RANKS[g.user.meta['group']]
                or GROUP_RANKS[set_group]>GROUP_RANKS[g.user.meta['group']]
            ):
                return 'ok'
            if current_group!=set_group and set_group in GROUP_RANKS.keys():
                g.redis.hset(ss_meta_key, 'group', set_group)
                set_message = None
                # XXX make a function for fetching name and acronym?
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
                if set_group=='mod':
                    set_message = '%s [%s] gave Tier 1 moderator status to %s [%s].'
                elif set_group=='mod2':
                    set_message = '%s [%s] gave Tier 2 moderator status to %s [%s].'
                elif set_group=='mod3':
                    set_message = '%s [%s] gave Tier 3 moderator status to %s [%s].'
                elif current_group in MOD_GROUPS and set_group not in MOD_GROUPS:
                    set_message = '%s [%s] removed moderator status from %s [%s].'
                if set_message is not None:
                    set_message = set_message % (
                        g.user.character['name'],
                        g.user.character['acronym'],
                        set_session_name,
                        set_session_acronym
                    )
                # Refresh the user's subscriptions.
                g.redis.publish('channel.'+chat+'.refresh', set_session_id+'#'+set_group)
                send_message(g.redis, chat, -1, 'user_change', set_message)
        if 'user_action' in request.form and 'counter' in request.form and request.form['user_action'] in MINIMUM_RANKS:
            # Check if we're high enough to perform this action.
            if GROUP_RANKS[g.user.meta['group']]<MINIMUM_RANKS[request.form['user_action']]:
                return 'ok'
            their_session_id = g.redis.hget('chat.'+chat+'.counters', request.form['counter']) or abort(400)
            their_group = g.redis.hget('session.'+their_session_id+'.meta.'+chat, 'group')
            # Check if we're high enough to affect the other user.
            if GROUP_RANKS[g.user.meta['group']]<GROUP_RANKS[their_group]:
                return 'ok'
            # XXX make a function for fetching name and acronym?
            # Fetch their name and convert to unicode.
            their_chat_key = 'session.'+their_session_id+'.chat.'+chat
            their_character = g.redis.hget(their_chat_key, 'character')
            their_session_name = unicode(
                g.redis.hget(their_chat_key, 'name') or CHARACTER_DETAILS[their_character]['name'],
                encoding='utf8'
            )
            their_session_acronym = unicode(
                g.redis.hget(their_chat_key, 'acronym') or CHARACTER_DETAILS[their_character]['acronym'],
                encoding='utf8'
            )
            if request.form['user_action']=='kick':
                g.redis.publish('channel.'+chat+'.refresh', their_session_id+'#kick')
                disconnect(g.redis, chat, their_session_id, "%s [%s] kicked %s [%s] from the chat." % (
                    g.user.character['name'],
                    g.user.character['acronym'],
                    their_session_name,
                    their_session_acronym
                ))
            # Don't ban people from the oubliette because that'll just put us in an infinite loop.
            elif request.form['user_action']=='ip_ban' and chat!='theoubliette':
                their_ip_address = g.redis.hget('session.'+their_session_id+'.meta', 'last_ip')
                if their_ip_address is not None:
                    g.redis.zadd('ip-bans', chat+'/'+their_ip_address, get_time(IP_BAN_PERIOD))
                g.redis.publish('channel.'+chat+'.refresh', their_session_id+'#ban')
                disconnect(g.redis, chat, their_session_id, "%s [%s] IP banned %s [%s]." % (
                    g.user.character['name'],
                    g.user.character['acronym'],
                    their_session_name,
                    their_session_acronym
                ))
        if 'meta_change' in request.form:
            for flag in CHAT_FLAGS:
                if flag in request.form:
                    if request.form[flag]=='1':
                        g.redis.hset('chat.'+chat+'.meta', flag, '1')
                    else:
                        g.redis.hdel('chat.'+chat+'.meta', flag)
            send_message(g.redis, chat, -1, 'meta_change')
        if 'topic' in request.form:
            if request.form['topic']!='':
                g.redis.hset('chat.'+chat+'.meta', 'topic', request.form['topic'])
                send_message(g.redis, chat, -1, 'meta_change', '%s changed the conversation topic to "%s".' % (
                    g.user.character['name'],
                    request.form['topic']
                ))
            else:
                g.redis.hdel('chat.'+chat+'.meta', 'topic')
                send_message(g.redis, chat, -1, 'meta_change', '%s removed the conversation topic.' % g.user.character['name'])
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
        if silent_users is True and g.user.meta['group'] not in MOD_GROUPS:
            hide_silence(message_dict['online'], message_dict['idle'])
        message_dict['meta'] = g.redis.hgetall('chat.'+chat+'.meta')
        # Newly created matchmaker chats don't know the counter, so we send it here.
        message_dict['counter'] = g.user.meta['counter']
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
                refresh_user, refresh_command = msg['data'].split('#', 1)
                if refresh_user==g.user.session_id:
                    if refresh_command in ['kick', 'ban']:
                        resp = make_response('{"exit":"'+refresh_command+'"}')
                        resp.headers['Content-type'] = 'application/json'
                        return resp
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

