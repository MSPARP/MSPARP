import datetime
from sqlalchemy.orm.exc import NoResultFound

from model import Log, LogPage

class NoLogId(Exception):
    pass

def get_or_create_log(redis, mysql, chat, chat_type):

    # Find existing log or create a new one.

    try:
        print "getting log"
        log = mysql.query(Log).filter(Log.url==chat).one()
        try:
            print "getting latest page"
            latest_page_query = mysql.query(LogPage).filter(LogPage.log_id==log.id)
            print latest_page_query
            print list(latest_page_query)
            latest_page = latest_page_query[-1]
            print latest_page
        except:
            print "no latest page"
            latest_page = new_page(mysql, log)
    except (NoResultFound, NoLogId):
        print "not got log"
        log = Log(url=chat)
        print log
        mysql.add(log)
        print log
        mysql.flush()
        print log
        print log.id
        if chat_type=='match':
            redis.set('chat.'+chat+'.log', log.id)
        latest_page = new_page(mysql, log)

    return log, latest_page

def new_page(mysql, log, last=0):
    new_page_number = last+1
    latest_page = LogPage(log_id=log.id, number=new_page_number, content=u'')
    print latest_page
    mysql.add(latest_page)
    log.page_count = new_page_number
    return latest_page

def archive_chat(redis, mysql, chat, chat_type=None, backlog=0):

    if chat_type is None:
        chat_type = redis.hget('chat.'+chat+'.meta', 'type')

    log, latest_page = get_or_create_log(redis, mysql, chat, chat_type)

    print latest_page
    print latest_page.number

    archive_length = redis.llen('chat.'+chat)-backlog

    if archive_length<1:
        # Nothing to archive; just commit and return.
        mysql.commit()
        return log.id

    for n in range(archive_length):
        line = redis.lindex('chat.'+chat, n)
        print len(latest_page.content.encode('utf8'))
        print len(line)
        # Create a new page if the line won't fit on this one.
        #if len(latest_page.content.encode('utf8'))+len(line)>65535:
        if len(latest_page.content.encode('utf8'))+len(line)>65535:
            print "creating a new page"
            latest_page = latest_page = new_page(mysql, log, latest_page.number)
            print "page "+str(latest_page.number)
        latest_page.content += unicode(line, encoding='utf8')+'\n'

    log.time_saved = datetime.datetime.now()

    print "PRE-COMMIT"
    mysql.commit()
    print "POST-COMMIT"

    # Don't delete from redis until we've successfully committed.
    redis.ltrim('chat.'+chat, archive_length, -1)

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

def delete_chat(redis, chat):

    # XXX PIPELINE THIS???

    # XXX IF IT'S BEEN SAVED BEFORE, SAVE IT AGAIN BEFORE DELETING.
    # XXX SAVE HERE RATHER THAN IN reaper.py

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

