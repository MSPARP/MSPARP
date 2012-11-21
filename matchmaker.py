#!/usr/bin/python
from redis import Redis
from random import shuffle, choice
import uuid
import time

def getPickyness(redis,searchers):
    picky = {}
    allchars = redis.smembers('all-chars')
    for session in searchers:
        picky[session] = redis.smembers('session.%s.picky' % session)
        if len(picky[session])==0:
            picky[session] = allchars
    return picky

def shuffled(seq):
    local = list(seq)
    shuffle(local)
    return local

def match(picky, first, second):
    chat=str(uuid.uuid4()).replace('-','')
    redis.hset('chat.'+chat+'.meta', 'type', 'unsaved')
    redis.set('session.'+first+'.match', chat)
    redis.set('session.'+second+'.match', chat)
    redis.zrem('searchers', first)
    redis.zrem('searchers', second)
    del picky[first]
    del picky[second]

def matchUser(session, picky, identities):
    acceptable = []
    try:
        wants = picky[session]
    except KeyError:
        return # we've already been matched
    whoiam = identities[session]
    for other, their_wants in picky.items():
        if other!=session and identities[other] in wants and whoiam in picky[other]:
            acceptable.append(other)

    if acceptable:
        selected = choice(acceptable)
        match(picky, session, selected)

if __name__=='__main__': 

    redis = Redis(unix_socket_path='/tmp/redis.sock')

    while True:
        searchers = redis.zrange('searchers', 0, -1)
        print 'searchers: ', searchers
        
        if len(searchers)>=2: # if there aren't at least 2 people, there can't be matches
            identities = dict((session, redis.hget('session.'+session, 'character')) for session in searchers)
            picky = getPickyness(redis, searchers)
            for session in shuffled(picky.keys()):
                matchUser(session, picky, identities)

        time.sleep(1)

