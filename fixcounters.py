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

a = redis.keys("chat.*.meta")
for x in a:
    split = x.split(".")
    chats.add(split[1])

pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(chats)).start()
i = 0
for chat in chats:
	i += 1
	#print chat
	chat_meta = redis.hgetall('chat.'+chat+'.meta')
	for line in redis.lrange('chat.'+chat, 0, -1):
		try:
			l = parse_line(line, 0)
		except ValueError:
			brokenChats.add(chat)
	pbar.update(i)
pbar.finish()

print brokenChats