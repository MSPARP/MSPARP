#!/usr/bin/python
from redis import Redis
from random import shuffle,choice
import uuid
import time

def getPickyness(db,searchers):
	picky={}
	allchars=db.smembers('all-chars')
	for user in searchers:
		if db.get('user-%s-picky' % user)=='True':
			picky[user]=db.smembers('user-%s-picky-chars' % user)
		else:
			picky[user]=allchars
	return picky

def shuffled(seq):
	local=list(seq)
	shuffle(local)
	return local

def match(picky,first,second):
	chat=str(uuid.uuid4()).replace('-','')
	db.set('chat-'+first,chat)
	db.set('chat-'+second,chat)
	db.zrem('searchers',first)
	db.zrem('searchers',second)
	del picky[first]
	del picky[second]
def matchUser(user,picky,identities):
	acceptable=[]
	try:
		wants=picky[user]
	except KeyError:
		return # we've already been matched
	whoiam=identities[user]
	for other,their_wants in picky.items():
		if other!=user and identities[other] in wants and whoiam in picky[other]:
			acceptable.append(other)

	if acceptable:
		selected=choice(acceptable)
		match(picky,user,selected)

if __name__=='__main__': 
	db=Redis(host='localhost')

	while True:
		searchers=db.zrange('searchers',0,-1)
		print 'searchers: ',searchers
		
		if len(searchers)>=2: # if there aren't at least 2 people, there can't be matches
			identities=dict((user,db.get('user-%s-character' % user)) for user in searchers)
			picky=getPickyness(db,searchers)
			for user in shuffled(picky.keys()):
				matchUser(user,picky,identities)


		time.sleep(1)
