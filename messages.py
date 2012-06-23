from flask import json, jsonify

def send_message(db, chat, msg_type, text=None, color='000000', acronym='', audience=None):

    # The JavaScript always expects the messages list, so if we don't have any then we need an empty list.
    json_message = { 'messages': [] }

    if text is not None:
        message_content = acronym+': '+text if acronym else text

        # Store the message if it's not private.
        if msg_type!='private':
            message = color+'#'+message_content
            message_count = db.rpush('chat-'+chat, message)
        else:
            # ...or just get message count if it is.
            message_count = db.llen('chat-'+chat)

        # And add it to the pubsub data.
        json_message['messages'].append({
            'id': message_count - 1,
            'color': color,
            'line': message_content
        })

    if msg_type=='user_change':

        # Generate user list.
        user_list, mod_user_list = get_user_list(db, chat, 'both')

        # Send to mods first if they have their own list.
        if mod_user_list is not user_list:
            json_message['online'] = mod_user_list
            db.publish('channel-'+chat+'.mod', json.dumps(json_message))

        json_message['online'] = user_list

    elif msg_type=='private':
        # Just send it to the specified person.
        db.publish('channel-'+chat+'.'+audience, json.dumps(json_message))
        return None

    # Push to the publication channel to wake up longpolling listeners
    db.publish('channel-'+chat, json.dumps(json_message))

def get_user_list(db, chat, audience):

        # Audience can be mod, user or all.
        # If it's mod, we return the full userlist.
        # If it's user, we return the userlist with silent users covered up.
        # If it's all, we return the both lists (or two copies of the same
        # list if they're the same).

        user_list = []
        user_states = db.hgetall('chat-'+chat+'-sessions')
        user_counter = db.lrange('chat-'+chat+'-counter', 0, -1)

        silent_users = False

        for counter, user in enumerate(user_counter):
            if user_states[user] in ['online', 'away']:
                user_info = db.hgetall('session-'+user+'-'+chat)
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

def parseLine(line, id):
    "Parse a chat line like 'FF00FF#Some Text' into a dict"
    parts = line.split('#', 1)
    return {
        'id': id,
        'color': parts[0],
        'line': unicode(parts[1], encoding='utf-8')
    }

def parseMessages(seq, offset):
    return [parseLine(line, i) for (i, line) in enumerate(seq, offset)]

