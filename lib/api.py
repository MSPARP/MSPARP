from lib.messages import send_message

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
