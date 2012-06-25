from redis import Redis

db = Redis()

print 'Converting session-chats.'

for key in db.keys('session-*-*-*-*-*-*'):
    if key[-5:]=='picky':
        new_key = 'session.'+key[8:-6]+'.picky'
    else:
        new_key = 'session.'+key[8:44]+'.chat.'+key[45:]
    db.rename(key, new_key)
    print 'Converting '+key+' to '+new_key+'.'

print 'Session-chats complete.'

print 'Converting sessions.'

for key in db.keys('session-*-*-*-*-*'):
    new_key = 'session.'+key[8:]
    db.rename(key, new_key)
    print 'Converting '+key+' to '+new_key+'.'

print 'Sessions complete.'

print 'Converting user-chats.'

for key in db.keys('user-*-chats'):
    new_key = 'session.'+key[5:-6]+'.chats'
    db.rename(key, new_key)
    print 'Converting '+key+' to '+new_key+'.'

print 'User-chats converted.'

print 'Converting chat-sessions.'

chat_sessions = db.keys('chat-*-sessions')

print str(len(chat_sessions))+' chat-sessions total.'

chat_sessions_converted = 0

for chat_session in chat_sessions:
    chat = chat_session[5:-9]
    db.rename(chat_session, 'chat.'+chat+'.sessions')
    chat_sessions_converted = chat_sessions_converted+1
    print 'Sessions for chat '+chat+' converted. '+str(len(chat_sessions)-chat_sessions_converted)+' chat-sessions remaining.'

print 'Chat-sessions complete.'

print 'Converting chats.'

chats = db.keys('chat-*')

print str(len(chats))+' chats total.'

chats_converted = 0

for chat_key in chats:
    chat = chat_key[5:]
    if db.type(chat_key)=='list':
        db.rename(chat_key, 'chat.'+chat)
    else:
        db.delete(chat_key)
    chats_converted = chats_converted+1
    print 'Chat '+chat+' converted. '+str(len(chats)-chats_converted)+' chats remaining.'

print 'Chats complete.'
