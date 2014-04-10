from redis import Redis
import json
import time
import sys
import os

db = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))

def global_announcement(color, line):
    pipe = db.pipeline()
    chats = set()
    chat_sessions = db.zrange('chats-alive', 0, -1)
    for chat_session in chat_sessions:
        chat, user = chat_session.split("/")
        chats.add(chat)
    message = {
        "messages": [
            {
                "color": color,
                "timestamp": 0,
                "counter": -123,
                "type": "global",
                "line": line
            }
        ]
    }

    for chat in chats:
        message['messages'][0]['id'] = db.llen("chat."+chat)-1
        pipe.publish("channel."+chat, json.dumps(message))

    pipe.execute()

global_announcement(sys.argv[1], sys.argv[2])
# global.py <hex color code> <message>