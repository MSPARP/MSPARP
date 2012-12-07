#!/usr/bin/python

from redis import Redis
import time
import datetime

from lib import ARCHIVE_PERIOD, get_time
from lib.api import disconnect
from lib.archive import archive_chat, delete_chat_session, delete_chat
from lib.characters import CHARACTER_DETAILS
from lib.messages import send_message
from lib.model import sm
from lib.sessions import PartialSession

def get_default(redis, session, chat, key, defaultValue=''):
    v = redis.hget("session."+session+".chat."+chat, key)
    if v is not None:
        return v
    return defaultValue

if __name__=='__main__':

    redis = Redis(unix_socket_path='/tmp/redis.sock')
    mysql = sm()

    current_time = datetime.datetime.now()

    while True:

        for dead in redis.zrangebyscore('chats-alive', 0, get_time()):
            chat, session = dead.split('/')
            disconnect_message = None
            if redis.hget('session.'+session+'.meta.'+chat, 'group')!='silent':
                session_name = redis.hget('session.'+session+'.chat.'+chat, 'name')
                if session_name is None:
                    session_name = CHARACTER_DETAILS[redis.hget('session.'+session+'.chat.'+chat, 'character')]['name']
                disconnect_message = '%s\'s connection timed out. Please don\'t quit straight away; they could be back.' % (session_name)
            disconnect(redis, chat, session, disconnect_message)
            print 'dead', dead

        for dead in redis.zrangebyscore('searchers', 0, get_time()):
            print 'reaping searcher', dead
            redis.zrem('searchers', dead)

        new_time = datetime.datetime.now()

        # Every minute
        if new_time.minute!=current_time.minute:

            # Archive chats.
            for chat in redis.zrangebyscore('archive-queue', 0, get_time()):
                archive_chat(redis, mysql, chat, 50)
                pipe = redis.pipeline()
                pipe.scard('chat.'+chat+'.online')
                pipe.scard('chat.'+chat+'.idle')
                online, idle = pipe.execute()
                # Stop archiving if no-one is online any more.
                if online+idle==0:
                    redis.zrem('archive-queue', chat)
                else:
                    redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))

            # Delete chat-sessions.
            for chat_session in redis.zrangebyscore('chat-sessions', 0, get_time()):
                delete_chat_session(redis, *chat_session.split('/'))

            # Delete chats.
            for chat in redis.zrangebyscore('delete-queue', 0, get_time()):
                delete_chat(redis, mysql, chat)

            # Delete sessions.
            for session_id in redis.zrangebyscore('all-sessions', 0, get_time()):
                delete_session(redis, session_id)

            pass

        current_time = new_time

        time.sleep(1)

