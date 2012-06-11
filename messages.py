from flask import json, jsonify

def addMessage(db, chatid, color, acronym, text):

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

    # Push to the publication channel to wake up longpolling listeners
    db.publish('channel-'+chatid, json.dumps(json_message))

def addSystemMessage(db, chatid, text):
    addMessage(db, chatid, '000000', '', text)

def parseLine(line, id):
    "Parse a chat line like 'FF00FF#Some Text' into a dict"
    parts = line.split('#', 1)
    return {
        'id': id,
        'color': parts[0],
        'line': unicode(parts[1], encoding='utf-8')
    }

def parseMessages(seq, offset):
    return jsonify(messages=[parseLine(line, i) for (i, line) in enumerate(seq, offset)])

