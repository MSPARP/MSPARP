from flask import json, jsonify

from lib import DELETE_MATCH_PERIOD, get_time

def send_message(redis, chat, msg_type, text=None, color='000000', acronym='', audience=None):

    # The JavaScript always expects the messages list, so if we don't have any then we need an empty list.
    json_message = { 'messages': [] }

    if text is not None:
        message_content = acronym+': '+text if acronym else text

        # Store the message if it's not private.
        if msg_type!='private':
            message = color+'#'+message_content
            message_count = redis.rpush('chat.'+chat, message)
        else:
            # ...or just get message count if it is.
            message_count = redis.llen('chat.'+chat)

        # And add it to the pubsub data.
        json_message['messages'].append({
            'id': message_count - 1,
            'color': color,
            'line': message_content
        })

    if msg_type=='user_change':

        # Generate user list.
        user_list, mod_user_list = get_user_list(redis, chat, 'both')

        # Send to mods first if they have their own list.
        if mod_user_list is not user_list:
            json_message['online'] = mod_user_list
            redis.publish('channel.'+chat+'.mod', json.dumps(json_message))

        # If the last person just left, mark the chat for archiving.
        if g.chat_type=='match' and len(user_list)==0:
            g.redis.zadd('delete-queue', chat, get_time(DELETE_MATCH_PERIOD))

        json_message['online'] = user_list

    elif msg_type=='private':
        # Just send it to the specified person.
        redis.publish('channel.'+chat+'.'+audience, json.dumps(json_message))
        return None

    # Push to the publication channel to wake up longpolling listeners
    redis.publish('channel.'+chat, json.dumps(json_message))

def get_user_list(redis, chat, audience):

        # Audience can be mod, user or all.
        # If it's mod, we return the full userlist.
        # If it's user, we return the userlist with silent users covered up.
        # If it's all, we return the both lists (or two copies of the same
        # list if they're the same).

        user_list = []
        user_counter = redis.lrange('chat.'+chat+'.counter', 0, -1)
        user_states = redis.hgetall('chat.'+chat+'.sessions')

        silent_users = False

        for counter, user in enumerate(user_counter):
            if user_states[user] in ['online', 'away']:
                user_info = redis.hgetall('session.'+user+'.chat.'+chat)
                user_object = {
                    'name': user_info['name'],
                    'acronym': user_info['acronym'],
                    'color': user_info['color'],
                    'state': user_states[user],
                    # If the audience is user, we cover up the silent users here so we don't have to do a second iteration.
                    'group': user_info['group'] if audience!='user' or user_info['group']!='silent' else 'user',
                    'counter': counter
                }
                # If there's a silent user in the list, remember to do a second iteration covering them up.
                if audience=='both' and user_info['group']=='silent':
                    silent_users = True
                user_list.append(user_object)
        user_list.sort(key=lambda _: _['name'].lower())

        if audience=='both':
            if silent_users:
                covered_user_list = []
                # Iterate through the userlist changing all the silent users to user.
                for user in user_list:
                    if user['group']=='silent':
                        covered_user = dict(user)
                        covered_user['group'] = 'user'
                        covered_user_list.append(covered_user)
                    else:
                        covered_user_list.append(user)
            else:
                covered_user_list = user_list
            return covered_user_list, user_list

        return user_list

def parse_line(line, id):
    "Parse a chat line like 'FF00FF#Some Text' into a dict"
    parts = line.split('#', 1)
    return {
        'id': id,
        'color': parts[0],
        'line': unicode(parts[1], encoding='utf-8')
    }

def parse_messages(seq, offset):
    return [parse_line(line, i) for (i, line) in enumerate(seq, offset)]

