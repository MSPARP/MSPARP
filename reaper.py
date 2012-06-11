#!/usr/bin/python

from redis import Redis
import time
from messages import addSystemMessage

STARTTIME = 1302231346
PING_PERIOD = 10
SEARCH_PERIOD = 1

def getTime():
    return time.time() - STARTTIME

def getD(db, session, key, defaultValue=''):
    v = db.hget("session-"+session, key)
    if v is not None:
        return v
    return defaultValue

if __name__=='__main__':

    db = Redis(host='localhost')

    while True:

        for dead in db.zrangebyscore('chats-alive', 0, getTime()-PING_PERIOD*2):
            chat, session = dead.split('/') # FIXME: what if a user fucks this up by sticking a / in their uid?
            db.zrem('chats-alive', dead)
            db.srem(('chat-%s-sessions' % chat), session)
            db.srem('sessions-chatting', session)
            name = getD(db, session, 'name', 'UNKNOWN USER')
            print 'dead', dead, name
            addSystemMessage(db, chat, '%s\'s connection timed out. Please don\'t quit straight away; they could be back.' % (name), True)

        for dead in db.zrangebyscore('searchers', 0, getTime()-SEARCH_PERIOD*2):
            print 'reaping searcher', dead
            db.zrem('searchers', dead)

        time.sleep(1)

