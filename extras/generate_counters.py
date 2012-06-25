from redis import Redis

db = Redis()

chats = db.keys('chat.*.sessions')

print str(len(chats))+' chats.'

counters_generated = 0

for chat in chats:
    chat_sessions = db.hgetall(chat)
    for session in chat_sessions.keys():
        db.rpush(chat[:-9]+'.counter', session)
    counters_generated = counters_generated+1
    print 'Counter for '+chat[:-9]+' generated. '+str(len(chats)-counters_generated)+' remaining.'
