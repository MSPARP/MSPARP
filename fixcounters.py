from lib import SEARCH_PERIOD, ARCHIVE_PERIOD, OUBLIETTE_ID, get_time, validate_chat_url
from lib.characters import CHARACTER_GROUPS, CHARACTERS, CHARACTER_DETAILS
from lib.messages import parse_line
from lib.sessions import CASE_OPTIONS
from redis import ConnectionPool, Redis, UnixDomainSocketConnection
from progressbar import Bar, Percentage, ProgressBar
import os

#redis_pool = ConnectionPool(host='127.0.0.1', port=6380, db=0)
redis_pool = ConnectionPool(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))
redis = Redis(connection_pool=redis_pool)

chats = set()
brokenChats = set()
fixedLines = 0
fixedCounters = 0

a = redis.keys("chat.*.meta")
for x in a:
    split = x.split(".")
    chats.add(split[1])

pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(chats)).start()
i = 0
for chat in chats:
	i += 1
	for line in redis.lrange('chat.'+chat, 0, -1):
		try:
			l = parse_line(line, 0)
		except ValueError:
			brokenChats.add(chat)
			fixedLines += 1
			redis.lrem('chat.' + chat, line, 0)
	for counter in redis.hgetall('chat.' + chat + '.counters'):
		if counter.isdigit():
			pass
		else:
			fixedCounters += 1
			cookie = redis.hget('chat.' + chat + '.counters',counter)
			#print cookie
			redis.hdel('chat.'+chat+'.counters',counter)
			redis.delete('session.' + cookie + '.chat.' + chat)
			redis.delete('session.' + cookie + '.meta.' + chat)
	pbar.update(i)
pbar.finish()

print "-----"
print "Chats repaired:"
print brokenChats
print "-----"
print "Total fixed lines   : " + str(fixedLines)
print "Total fixed counters: " + str(fixedCounters)