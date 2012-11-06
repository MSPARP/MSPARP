#!/usr/bin/python

from redis import Redis
import time
import datetime

from lib import PING_PERIOD, SEARCH_PERIOD, ARCHIVE_PERIOD, get_time
from lib.api import disconnect
from lib.archive import archive_chat, delete_chat
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
            dead_session = PartialSession(redis, session, chat)
            name = dead_session.name
            disconnect_message = None
            if dead_session.group!='silent':
                disconnect_message = '%s\'s connection timed out. Please don\'t quit straight away; they could be back.' % (name)
            disconnect(redis, chat, session, disconnect_message)
            send_message(redis, chat, -1, 'user_change', disconnect_message)
            print 'dead', dead, name

        for dead in redis.zrangebyscore('searchers', 0, get_time()):
            print 'reaping searcher', dead
            redis.zrem('searchers', dead)

        new_time = datetime.datetime.now()

        # Every minute
        if new_time.minute!=current_time.minute:
            # Save chats
            for chat in redis.zrangebyscore('archive-queue', 0, get_time()):
                redis.zrem('archive-queue', chat)
                # If anyone's online, re-add it to the list.
                chat_sessions = redis.hvals('chat.'+chat+'.sessions')
                if 'online' in chat_sessions or 'away' in chat_sessions:
                    print "chat "+chat+" is still active"
                    redis.zadd('archive-queue', chat, get_time(ARCHIVE_PERIOD))
                # Save
                print "saving chat "+chat
                archive_chat(redis, mysql, chat, backlog=50)
                print "saved chat "+chat
            # Delete match chats
            for chat in redis.zrangebyscore('delete-queue', 0, get_time()):
                # Check type, don't delete group chats for now.
                print "deleting chat "+chat
                if redis.get('chat.'+chat+'.type') in ['match', None]:
                    # If it's been saved before, save it again.
                    if redis.llen('chat.'+chat)!=0:
                        print "saving before deletion"
                        archive_chat(redis, mysql, chat, chat_type='match', backlog=0)
                    delete_chat(redis, chat)
                    redis.zrem('delete-queue', chat)
                print "deleted chat "+chat
            pass

        current_time = new_time

        time.sleep(1)

