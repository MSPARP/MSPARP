from flask import json, jsonify

def addMessage(db, chatid, color, acronym, text, reload_user_list=False):

    if text is None:
        # Send a blank message. This can be used to reload the userlist without sending anything.
        json_message = { 'messages': [] }
    else:
        message_content = acronym+': '+text if acronym else text

        # generate encoded form
        message = color+'#'+message_content

        # Save to the chat- list. This is the permanent log form
        messagesCount = db.rpush('chat-'+chatid, message)

        json_message = {
            'messages': [
                {
                    'id': messagesCount - 1,
                    'color': color,
                    'line': message_content
                }
            ]
        }

    if reload_user_list==True:
        json_message['online'] = get_user_list(db, chatid)

    # Push to the publication channel to wake up longpolling listeners
    db.publish('channel-'+chatid, json.dumps(json_message))

def addSystemMessage(db, chatid, text, reload_user_list=False):
    addMessage(db, chatid, '000000', '', text, reload_user_list)

def get_user_list(db, chatid):
    user_list = []
    users = db.hgetall('chat-'+chatid+'-sessions')
    for user in users.items():
        if user[1] in ['online', 'away']:
            user_info = db.hgetall('session-'+user[0]+'-'+chatid)
            user_object = {
                'name': user_info['name'],
                'acronym': user_info['acronym'],
                'color': user_info['color'],
                'state': user[1],
                'group': user_info['group'] if user_info['group']!='silent' else 'user'
            }
            user_list.append(user_object)
    user_list.sort(key=lambda _: _['name'].lower())
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

