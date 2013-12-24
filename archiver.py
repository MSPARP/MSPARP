#!/usr/bin/python

from redis import Redis
import sys
import time
import datetime

from lib import ARCHIVE_PERIOD, get_time
from lib.api import disconnect
from lib.archive import archive_chat, delete_chat_session, delete_chat, delete_session
from lib.characters import CHARACTER_DETAILS
from lib.messages import send_message
from lib.model import sm
from lib.sessions import PartialSession
import os

if __name__=='__main__':

    print "Archiving script started."

    redis = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))

    current_time = datetime.datetime.now()

    while True:

        new_time = datetime.datetime.now()

        # Every minute
        if new_time.minute!=current_time.minute:
            print "running archiving"
            mysql = sm()

            # Send blank messages to avoid socket timeouts.
            for chat in redis.zrangebyscore('longpoll-timeout', 0, get_time()):
                send_message(redis, chat, -1, "message")

            # Expire IP bans.
            redis.zremrangebyscore('ip-bans', 0, get_time())

            # Archive chats.
            for chat in redis.zrangebyscore('archive-queue', 0, get_time()):
                print "archiving chat: ",chat
                archive_chat(redis, mysql, chat)
                pipe = redis.pipeline()
                pipe.scard('chat.'+chat+'.online')
                pipe.scard('chat.'+chat+'.idle')
                online, idle = pipe.execute()
                # Delete if no-one is online any more.
                if online+idle==0:
                    delete_chat(redis, mysql, chat)
                    redis.zrem('archive-queue', chat)
                else:
                    redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))

            # Delete chat-sessions.
            for chat_session in redis.zrangebyscore('chat-sessions', 0, get_time()):
                print "deleting chat session: ", chat_session
                delete_chat_session(redis, *chat_session.split('/'))

            # Delete chats.
            for chat in redis.zrangebyscore('delete-queue', 0, get_time()):
                myLength = redis.llen('chat.'+chat)
                if myLength < 10:
                    print "deleting unsaved chat: ", chat, "(lines:", redis.llen('chat.'+chat), ")"
                    delete_chat(redis, mysql, chat)
                    redis.zrem('delete-queue', chat)
                else:
                    print "found chat over 10 lines, fixing save status!", chat, "(lines:", redis.llen('chat.'+chat), ")"
                    redis.hset('chat.'+chat+'.meta', 'type', 'saved')
                    redis.zadd('archive-queue', chat, get_time(-60))
            # Delete sessions.
            for session_id in redis.zrangebyscore('all-sessions', 0, get_time()):
                print "deleting session: ", session_id
                delete_session(redis, session_id)

            mysql.close()
            del mysql

        current_time = new_time

        time.sleep(1)
        sys.stdout.write('.'),
        sys.stdout.flush()
