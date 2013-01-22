#!/usr/bin/python

import sys
from redis import Redis

db = Redis()

session_id = sys.argv[2]

if sys.argv[1]=='add':
    db.sadd('global-mods', session_id)
    print 'Added to global mods list.'
    for chat in db.smembers('session.'+session_id+'.chats'):
        print 'Setting group in '+chat+' to globalmod.'
        db.hset('session.'+session_id+'.meta.'+chat, 'group', 'globalmod')

elif sys.argv[1]=='remove':
    print 'Removed from global mods list.'
    db.srem('global-mods', session_id)
    for chat in db.smembers('session.'+session_id+'.chats'):
        if db.hget('session.'+session_id+'.meta.'+chat, 'counter')=='1':
            print 'Setting group in '+chat+' to mod.'
            db.hset('session.'+session_id+'.meta.'+chat, 'group', 'mod')
        else:
            print 'Setting group in '+chat+' to user.'
            db.hset('session.'+session_id+'.meta.'+chat, 'group', 'user')
