import datetime
from sqlalchemy.orm.exc import NoResultFound

from model import Log, LogPage

def get_or_create_log(redis, mysql, chat):
    # Find existing log or create a new one.
    try:
        log = mysql.query(Log).filter(Log.url==chat).one()
        try:
            latest_page_query = mysql.query(LogPage).filter(LogPage.log_id==log.id).order_by(LogPage.number.asc())
            latest_page = latest_page_query[-1]
            # XXX Is IndexError the right exception?
        except IndexError:
            latest_page = new_page(mysql, log)
    except NoResultFound:
        log = Log(url=chat)
        mysql.add(log)
        mysql.flush()
        latest_page = new_page(mysql, log)
    return log, latest_page

def new_page(mysql, log, last=0):
    new_page_number = last+1
    latest_page = LogPage(log_id=log.id, number=new_page_number, content=u'')
    mysql.add(latest_page)
    # XXX COMMIT HERE?
    log.page_count = new_page_number
    return latest_page

def archive_chat(redis, mysql, chat, backlog=0):
    log, latest_page = get_or_create_log(redis, mysql, chat)
    # XXX MAKE REALLY REALLY REALLY GODDAMN SURE THIS WORKS WITH MINUS NUMBERS
    # XXX FOR GOD'S SAKE
    lines = redis.lrange('chat.'+chat, 0, -1-backlog)
    for line in lines:
        # Create a new page if the line won't fit on this one.
        #if len(latest_page.content.encode('utf8'))+len(line)>65535:
        if len(latest_page.content.encode('utf8'))+len(line)>65535:
            print "creating a new page"
            latest_page = latest_page = new_page(mysql, log, latest_page.number)
            print "page "+str(latest_page.number)
        latest_page.content += unicode(line, encoding='utf8')+'\n'
    log.time_saved = datetime.datetime.now()
    mysql.commit()
    # Don't delete from redis until we've successfully committed.
    redis.ltrim('chat.'+chat, len(lines), -1)
    return log.id

def delete_chat_session(redis, chat, session_id):

    counter = redis.hget('session.'+session_id+'.meta.'+chat, 'counter')
    pipe = redis.pipeline()
    pipe.hdel('chat.'+chat+'.counters', counter)
    pipe.delete('session.'+session_id+'.chat.'+chat)
    pipe.delete('session.'+session_id+'.meta.'+chat)
    pipe.srem('session.'+session_id+'.chats', chat)
    pipe.zrem('chat-sessions', chat+'/'+session_id)
    pipe.execute()

def delete_chat(redis, mysql, chat):

    # XXX PIPELINE THIS???

    # If it's been saved before, save it again before deleting.
    if redis.hget('chat.'+chat+'.meta', 'type')!='unsaved':
        archive_chat(redis, mysql, chat, 0)

    # Delete metadata first because it's used to check whether a chat exists.
    redis.delete('chat.'+chat+'.meta')

    redis.delete('chat.'+chat+'.online')
    redis.delete('chat.'+chat+'.idle')
    redis.delete('chat.'+chat+'.characters')

    for session_id in redis.hvals('chat.'+chat+'.counters'):
        redis.srem('session.'+session_id+'.chats', chat)
        redis.delete('session.'+session_id+'.chat.'+chat)
        redis.delete('session.'+session_id+'.meta.'+chat)
        redis.zrem('chat-sessions', chat+'/'+session_id)

    redis.delete('chat.'+chat+'.counters')
    redis.delete('chat.'+chat)
    redis.zrem('delete-queue', chat)

def delete_session(redis, session_id):

    for chat in redis.smembers('session.'+session_id+'.chats'):
        delete_chat_session(redis, chat, session_id)

    redis.delete('session.'+session_id)
    redis.delete('session.'+session_id+'.meta')
    redis.zrem('all-sessions', session_id)

