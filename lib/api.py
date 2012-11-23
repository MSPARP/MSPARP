from lib import get_time, ARCHIVE_PERIOD, PING_PERIOD
from lib.messages import send_message

def ping(redis, chat, session):
    online_state = get_online_state(redis, chat, session.session_id)
    fake_join_message = False
    if online_state=='offline':
        # The user isn't online already. Add them to the chat.
        # Remove the chat from the delete queue and add to the archive queue.
        redis.zrem('delete-queue', chat)
        if redis.zscore('archive-queue', chat) is None:
            redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))
        # Set user state.
        redis.sadd('chat.'+chat+'.online', session.session_id)
        if session.meta['group']=='silent':
            join_message = None
            fake_join_message = True
        else:
            join_message = '%s [%s] joined chat.' % (session.character['name'], session.character['acronym'])
        send_message(redis, chat, -1, 'user_change', join_message)
        redis.sadd('sessions-chatting', session.session_id)
        # Add character to chat character list.
        redis.sadd('chat.'+chat+'.characters', session.character['character'])
    redis.zadd('chats-alive', chat+'/'+session.session_id, get_time(PING_PERIOD*2))
    # Return True if the calling function needs to fake a join message.
    return fake_join_message

def change_state(redis, chat, session_id, state):
    current_state = get_online_state(redis, chat, session_id)
    if state!=current_state:
        redis.smove('chat.'+chat+'.'+current_state, 'chat.'+chat+'.'+state, session_id)
        # Update userlist.
        send_message(redis, chat, -1, 'user_change')

def disconnect(redis, chat, session_id, disconnect_message=None):
    online_state = get_online_state(redis, chat, session_id)
    if online_state!='offline':
        redis.srem('chat.'+chat+'.'+online_state, session_id)
        redis.zrem('chats-alive', chat+'/'+session_id)
        redis.srem('sessions-chatting', session_id)
        send_message(redis, chat, -1, 'user_change', disconnect_message)

def get_online_state(redis, chat, session_id):
    pipeline = redis.pipeline()
    pipeline.sismember('chat.'+chat+'.online', session_id)
    pipeline.sismember('chat.'+chat+'.idle', session_id)
    online, idle = pipeline.execute()
    if online:
        return 'online'
    elif idle:
        return 'idle'
    return 'offline'
