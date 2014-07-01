from flask import g
try:
    import ujson as json
except:
    import json

from lib import DELETE_UNSAVED_PERIOD, DELETE_SAVED_PERIOD, get_time, LONGPOLL_TIMEOUT_PERIOD
from characters import CHARACTER_DETAILS

FULL_CHARACTER_LENGTH = len(CHARACTER_DETAILS['anonymous/other'])+1

def send_message(redis, chat, counter, msg_type, text=None, color='000000', acronym='', audience=None):

    # Do this here because it's gotta be before userlist generation.
    redis.zadd('longpoll-timeout', chat, get_time(LONGPOLL_TIMEOUT_PERIOD))

    # The JavaScript always expects the messages list, so if we don't have any then we need an empty list.
    json_message = { 'messages': [] }

    if text is not None:
        message_content = acronym+': '+text if acronym else text

        # Store the message if it's not private.
        if msg_type!='private':
            message = ','.join([str(get_time()), str(counter), msg_type, color, message_content])
            message_count = redis.rpush('chat.'+chat, message)
            # Send the chat for archiving early if the chat is getting too long.
            if message_count>=500:
                try:
                    chat_type = g.chat_type
                except RuntimeError:
                    chat_type = redis.hget('chat.'+chat+'.meta', 'type')
                if chat_type!='unsaved':
                    redis.zadd('archive-queue', chat, get_time(-60))
        else:
            # ...or just get message count if it is.
            message_count = redis.llen('chat.'+chat)

        # And add it to the pubsub data.
        json_message['messages'].append({
            'id': message_count - 1,
            'timestamp': get_time(),
            'counter': counter,
            'type': msg_type,
            'color': color,
            'line': message_content
        })

    if msg_type=='user_change':

        # Generate user list.
        json_message['online'] = get_userlists(redis, chat)

        # g doesn't work in the reaper.
        try:
            chat_type = g.chat_type
        except RuntimeError:
            chat_type = redis.hget('chat.'+chat+'.meta', 'type')

        # If the last person just left, clean stuff up.
        if len(json_message['online']) == 0:
            # Mark the chat for deletion.
            if chat_type=='unsaved':
                redis.zadd('delete-queue', chat, get_time(DELETE_UNSAVED_PERIOD))
            else:
                redis.zadd('delete-queue', chat, get_time(DELETE_SAVED_PERIOD))
            # Stop avoiding timeouts.
            redis.zrem('longpoll-timeout', chat)

    elif msg_type=='meta_change':
        json_message['meta'] = redis.hgetall('chat.'+chat+'.meta')

    elif msg_type=='private':
        # Just send it to the specified person.
        redis.publish('channel.'+chat+'.'+audience, json.dumps(json_message))
        return None

    # Push to the publication channel to wake up longpolling listeners
    redis.publish('channel.'+chat, json.dumps(json_message))

def get_userlists(redis, chat):
    sessions_online = redis.smembers('chat.'+chat+'.online')
    online = get_sublist(redis, chat, sessions_online)

    return online

def get_sublist(redis, chat, sessions):
    sublist = []
    for session in sessions:
        session_character = redis.hgetall('session.'+session+'.chat.'+chat)
        try:
            if len(session_character)<FULL_CHARACTER_LENGTH:
                new_session_character = dict(CHARACTER_DETAILS[session_character['character']])
                new_session_character.update(session_character)
                session_character = new_session_character
            session_meta = redis.hgetall('session.'+session+'.meta.'+chat)
            sublist.append({
                'character': session_character,
                'meta': session_meta,
            })
        except KeyError:
            continue
    sublist.sort(key=lambda _: _['character']['name'].lower())
    return sublist

def parse_line(line, id):
    # Lines consist of comma separated fields.
    parts = line.split(',', 4)
    if not isinstance(parts[4], unicode):
        parts[4] = unicode(parts[4], encoding='utf-8')
    return {
        'id': id,
        'timestamp': int(parts[0]),
        'counter': int(parts[1]),
        'type': parts[2],
        'color': parts[3],
        'line': parts[4]
    }

def parse_messages(seq, offset):
    return [parse_line(line, i) for (i, line) in enumerate(seq, offset)]

