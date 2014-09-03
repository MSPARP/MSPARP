from flask import request, abort
from lib import get_time, ARCHIVE_PERIOD, PING_PERIOD
from lib.messages import send_message

def ping(redis, chat, session, chat_type):
    online_state = get_online_state(redis, chat, session.session_id)
    if online_state=='offline':
        # Don't let the user in if there are more than 30 people online already.
        # XXX SHOW THEM A PROPER ERROR MESSAGE FOR THIS
        if redis.sismember("global-mods", session.session_id) is False and redis.scard('chat.'+chat+'.online')>=30:
            abort(403)
        # Global bans
        if redis.hexists("global-bans", request.headers['CF-Connecting-IP']):
            abort(403)
        # Check for Redis loading.
        if session.meta['counter'] == "Redis is loading the dataset in memory":
            abort(500)
        # Check IP bans.
        if redis.zscore('ip-bans', chat+'/'+request.headers['CF-Connecting-IP']) is not None:
            abort(403)
        # The user isn't online already. Add them to the chat.
        # Remove the chat from the delete queue.
        redis.zrem('delete-queue', chat)
        # Add to the archive queue, but only if it's saved.
        if chat_type!='unsaved' and redis.zscore('archive-queue', chat) is None:
            redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))
        # Log their IP address.
        redis.hset('session.'+session.session_id+'.meta', 'last_ip', request.headers['CF-Connecting-IP'])
        # Set user state.
        redis.sadd('chat.'+chat+'.online', session.session_id)
        if session.meta['group']=='silent':
            join_message = None
        elif session.meta['group']=='globalmod' and redis.hget("session."+session.session_id+".meta", "noglobal") != "1":
            join_message = '%s [%s] joined chat. ~~ %s ~~ [u]MSPARP STAFF[/u]' % (session.character['name'], session.character['acronym'], session.meta['counter'])
        else:
            join_message = '%s [%s] joined chat. ~~ %s ~~' % (session.character['name'], session.character['acronym'], session.meta['counter'])
        send_message(redis, chat, -1, 'user_change', join_message)
        redis.sadd('sessions-chatting', session.session_id)
        # Add character to chat character list.
        redis.sadd('chat.'+chat+'.characters', session.character['character'])
        redis.zadd('chats-alive', chat+'/'+session.session_id, get_time(PING_PERIOD*2))
        return True
    redis.zadd('chats-alive', chat+'/'+session.session_id, get_time(PING_PERIOD*2))
    return False

def change_state(redis, chat, session_id, state):
    current_state = get_online_state(redis, chat, session_id)
    if state!=current_state:
        redis.smove('chat.'+chat+'.'+current_state, 'chat.'+chat+'.'+state, session_id)
        # Update userlist.
        send_message(redis, chat, -1, 'user_change')

def disconnect(redis, chat, session_id, disconnect_message=None):
    online_state = get_online_state(redis, chat, session_id)
    redis.srem('chat.'+chat+'.'+online_state, session_id)
    redis.zrem('chats-alive', chat+'/'+session_id)
    redis.srem('sessions-chatting', session_id)
    if online_state!='offline':
        send_message(redis, chat, -1, 'user_change', disconnect_message)

def get_online_state(redis, chat, session_id):
    online = redis.sismember('chat.'+chat+'.online', session_id)
    if online:
        return 'online'
    return 'offline'
