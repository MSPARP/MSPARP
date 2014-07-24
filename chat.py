from functools import wraps
from flask import Flask, g, request, render_template, make_response, jsonify, abort

from lib import PING_PERIOD, ARCHIVE_PERIOD, IP_BAN_PERIOD, CHAT_FLAGS, get_time
from lib.api import ping, change_state, disconnect, get_online_state
from lib.characters import CHARACTER_DETAILS
from lib.groups import MOD_GROUPS, GROUP_RANKS, MINIMUM_RANKS
from lib.messages import send_message, get_userlists, parse_messages
from lib.requests import populate_all_chars, connect_redis, create_chat_session, set_cookie, disconnect_redis
from lib.punishments import scenify
from Crypto.Cipher import XOR
import base64
import os
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, 2)


# Pre and post request stuff
app.before_first_request(populate_all_chars)
app.before_request(connect_redis)
app.before_request(create_chat_session)
app.after_request(set_cookie)
app.after_request(disconnect_redis)

# Decorators

def mark_alive(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.joining = ping(g.redis, request.form['chat'], g.user, g.chat_type)
        return f(*args, **kwargs)
    return decorated_function

# Views

@app.route('/post', methods=['POST'])
@mark_alive
def postMessage():
    chat = request.form['chat']
    if 'line' in request.form and g.user.meta['group']!='silent':
        # Remove linebreaks and truncate to 1500 characters.
        line = request.form['line'].replace('\n', ' ')[:1500]

        # Panda checks
        if g.redis.hexists('punish-scene', request.headers['CF-Connecting-IP']):
            if not g.redis.hexists('punish-scene', g.user.session_id):
                g.redis.hset("punish-scene", g.user.session_id, "Adding cookie from IP %s" % (request.headers['CF-Connecting-IP']))
            line = scenify(g.redis, g.user.session_id, chat, line)
        elif g.redis.hexists('punish-scene', g.user.session_id):
            if not g.redis.hexists('punish-scene', request.headers['CF-Connecting-IP']):
                g.redis.hset("punish-scene", request.headers['CF-Connecting-IP'], "Adding IP from cookie %s" % (g.user.session_id))
            line = scenify(g.redis, g.user.session_id, chat, line)

        send_message(g.redis, chat, g.user.meta['counter'], 'message', line, g.user.character['color'], g.user.character['acronym'])
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
                    set_message = '%s [%s] set %s [%s] to Professional Wet Blanket. They can now silence, kick and ban other users.'
                elif set_group=='mod2':
                    set_message = '%s [%s] set %s [%s] to Bum\'s Rusher. They can now silence and kick other users.'
                elif set_group=='mod3':
                    set_message = '%s [%s] set %s [%s] to Amateur Gavel-Slinger. They can now silence other users.'
                elif set_group=='user':
                    if current_group in MOD_GROUPS:
                        set_message = '%s [%s] removed moderator status from %s [%s].'
                    else:
                        set_message = '%s [%s] unsilenced %s [%s].'
                elif set_group=='silent':
                    set_message = '%s [%s] silenced %s [%s].'
                if set_message is not None:
                    set_message = set_message % (
                        g.user.character['name'],
                        g.user.character['acronym'],
                        set_session_name,
                        set_session_acronym
                    )
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
                g.redis.publish('channel.'+chat+'.'+their_session_id, '{"exit":"kick"}')
                disconnect(g.redis, chat, their_session_id, "%s [%s] kicked %s [%s] from the chat." % (
                    g.user.character['name'],
                    g.user.character['acronym'],
                    their_session_name,
                    their_session_acronym
                ))
            # Don't ban people from the oubliette because that'll just put us in an infinite loop.
            elif request.form['user_action']=='ip_ban' and chat!='theoubliette':
                cipher = XOR.new(os.environ['BAN_KEY'])
                their_ip_address = g.redis.hget('session.'+their_session_id+'.meta', 'last_ip')
                ban_id = chat+'/'+their_ip_address
                if their_ip_address is not None:
                    g.redis.zadd('ip-bans', ban_id, get_time(IP_BAN_PERIOD))
                if 'reason' in request.form:
                    g.redis.hset('ban-reasons', ban_id, "[Name: %s; Counter: %s] %s" % (
                        their_session_name,
                        request.form['counter'],
                        request.form['reason'][:1500]
                    ))
                else:
                    g.redis.hset('ban-reasons', ban_id, "[Name: %s; Counter: %s]" % (
                        their_session_name,
                        request.form['counter']
                    ))
                g.redis.publish('channel.'+chat+'.'+their_session_id, '{"exit":"ban"}')
                disconnect(g.redis, chat, their_session_id, "%s [%s] IP banned %s [%s]. ~ %s ~" % (
                    g.user.character['name'],
                    g.user.character['acronym'],
                    their_session_name,
                    their_session_acronym,
                    base64.b64encode(cipher.encrypt(ban_id)),
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
                truncated_topic = request.form['topic'].replace('\n', ' ')[:1500]
                g.redis.hset('chat.'+chat+'.meta', 'topic', truncated_topic)
                send_message(g.redis, chat, -1, 'meta_change', '%s changed the conversation topic to "%s".' % (
                    g.user.character['name'],
                    truncated_topic
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

    # Check for stored messages.
    messages = g.redis.lrange('chat.'+chat, after+1, -1)
    if messages:
        message_dict = {
            'messages': parse_messages(messages, after+1)
        }
    elif g.joining:
        message_dict = {
            'messages': []
        }

    if message_dict:
        message_dict['online'] = get_userlists(g.redis, chat)
        message_dict['meta'] = g.redis.hgetall('chat.'+chat+'.meta')
        # Newly created matchmaker chats don't know the counter, so we send it here.
        message_dict['counter'] = g.user.meta['counter']
        return jsonify(message_dict)

    # Otherwise, listen for a message.
    pubsub = g.redis.pubsub()

    # Main channel.
    pubsub.subscribe('channel.'+chat)

    # Self channel.
    # Right now this is only used by kick/ban and IP lookup, so only subscribe
    # if we're in a group chat or a global mod.
    if g.chat_type=='group' or g.user.meta['group']=='globalmod':
        pubsub.subscribe('channel.'+chat+'.'+g.user.session_id)

    for msg in pubsub.listen():
        if msg['type']=='message':
            # The pubsub channel sends us a JSON string, so we return that instead of using jsonify.
            resp = make_response(msg['data'])
            resp.headers['Content-type'] = 'application/json'
            return resp

@app.route('/quit', methods=['POST'])
def quitChatting():
    disconnect_message = '%s [%s] disconnected.' % (g.user.character['name'], g.user.character['acronym']) if g.user.meta['group']!='silent' else None
    disconnect(g.redis, request.form['chat'], g.user.session_id, disconnect_message)
    return 'ok'

@app.route('/health', methods=['GET'])
def doHealthCheck():
    # should probably actually DO a health check here
    return 'ok'

@app.route('/save', methods=['POST'])
@mark_alive
def save():
    try:
        g.user.save_character(request.form)
    except ValueError as e:
        abort(400)
    return 'ok'

# Globalmod stuff.

@app.route('/ip_lookup', methods=['POST'])
def ip_lookup():
    if g.user.session_id in g.redis.smembers("global-admins"):
        pass
    else:
        return "not a globaladmin. nice try if you're not a globalmod or KB."
    chat = request.form['chat']
    counter = request.form['counter']
    theircookie = g.redis.hget("chat."+chat+".counters", counter)
    ip = g.redis.hget("session."+theircookie+".meta", "last_ip")

    return ip

if __name__ == "__main__":
    app.run(port=9000, debug=True)

