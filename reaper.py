#!/usr/bin/python

from redis import Redis
import time

from lib import PING_PERIOD, SEARCH_PERIOD, get_time
from lib.messages import send_message

def get_default(redis, session, chat, key, defaultValue=''):
    v = redis.hget("session."+session+".chat."+chat, key)
    if v is not None:
        return v
    return defaultValue

if __name__=='__main__':

    redis = Redis(host='localhost')

    while True:

        for dead in redis.zrangebyscore('chats-alive', 0, get_time()-PING_PERIOD*2):
            chat, session = dead.split('/') # FIXME: what if a user fucks this up by sticking a / in their uid?
            redis.zrem('chats-alive', dead)
            redis.hset(('chat.%s.sessions' % chat), session, 'offline')
            redis.srem('sessions-chatting', session)
            disconnect_message = None
            if get_default(redis, session, chat, 'group', None)!='silent':
                name = get_default(redis, session, chat, 'name', 'UNKNOWN USER')
                disconnect_message = '%s\'s connection timed out. Please don\'t quit straight away; they could be back.' % (name)
            send_message(redis, chat, 'user_change', disconnect_message)
            print 'dead', dead, name

        for dead in redis.zrangebyscore('searchers', 0, get_time()-SEARCH_PERIOD*2):
            print 'reaping searcher', dead
            redis.zrem('searchers', dead)

        time.sleep(1)

