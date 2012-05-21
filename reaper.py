#!/usr/bin/python
from redis import Redis
import time
from messages import addSystemMessage
STARTTIME=1302231346
PING_PERIOD=10
SEARCH_PERIOD=2
def getTime():
	return time.time()-STARTTIME
def getD(db,key,defaultValue=''):
	v=db.get(key)
	if v is not None:
		return v
	return defaultValue

if __name__=='__main__':
	db=Redis(host='localhost')
	while True:
		for dead in db.smembers('quits').union(db.zrangebyscore('chats-alive',0,getTime()-PING_PERIOD*2)):
			chat,uid=dead.split('/') # FIXME: what if a user fucks this up by sticking a / in their uid?
			db.zrem('chats-alive',dead)
			db.srem(('chat-%s-users' % chat),uid)
			db.srem('users-chatting',uid)
			db.srem('quits',dead)
			name=getD(db,'user-'+uid+'-name','UNKNOWN USER')
			acronym=getD(db,'user-'+uid+'-acronym','??')
			print 'dead',dead,name,acronym
			addSystemMessage(db,chat,'%s [%s] disconnected.' % (name,acronym))
		for dead in db.zrangebyscore('searchers',0,getTime()-SEARCH_PERIOD*2):
			print 'reaping searcher',dead
			db.zrem('searchers',dead)
		time.sleep(1)
