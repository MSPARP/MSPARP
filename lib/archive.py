import datetime
from sqlalchemy.orm.exc import NoResultFound

from characters import CHARACTER_DETAILS
from model import Chat, ChatSession, Log, LogPage

def get_or_create_log(redis, mysql, chat_url, chat_type='saved'):
    # Find existing Log, LogPage and Chat or create new ones.
    # If the Log doesn't exist, create Log, LogPage and Chat.
    # If the LogPage doesn't exist, create LogPage.
    # If the Chat doesn't exist, create Chat.
    try:
        log = mysql.query(Log).filter(Log.url==chat_url).one()
        try:
            latest_page_query = mysql.query(LogPage).filter(LogPage.log_id==log.id)
            latest_page = latest_page_query[-1]
            # XXX Is IndexError the right exception?
        except IndexError:
            latest_page = new_page(mysql, log)
        try:
            chat = mysql.query(Chat).filter(Chat.log_id==log.id).one()
        except NoResultFound:
            chat = Chat(log_id=log.id, type=chat_type)
            mysql.add(chat)
            mysql.flush()
    except NoResultFound:
        log = Log(url=chat_url)
        mysql.add(log)
        mysql.flush()
        latest_page = new_page(mysql, log)
        chat = Chat(log_id=log.id, type=chat_type)
        mysql.add(chat)
        mysql.flush()
    return log, latest_page, chat

def new_page(mysql, log, last=0):
    new_page_number = last+1
    latest_page = LogPage(log_id=log.id, number=new_page_number, content=u'')
    mysql.add(latest_page)
    mysql.flush()
    log.page_count = new_page_number
    return latest_page

def archive_chat(redis, mysql, chat_url):
    log, latest_page, chat = get_or_create_log(redis, mysql, chat_url)
    # If the chat hasn't saved since the last archive, skip it.
    if redis.llen('chat.'+chat_url)==0:
        return log.id
    # Metadata
    chat.type = redis.hget('chat.'+chat_url+'.meta', 'type')
    chat.counter = redis.hget('chat.'+chat_url+'.meta', 'counter')
    chat.topic = redis.hget('chat.'+chat_url+'.meta', 'topic')
    mysql.flush()
    # Sessions
    mysql_sessions = mysql.query(ChatSession).filter(ChatSession.log_id==log.id)
    redis_sessions = redis.hgetall('chat.'+chat_url+'.counters')
    # Update the sessions which are already in the database.
    for mysql_session in mysql_sessions:
        redis_session = redis.hgetall('session.'+mysql_session.session_id+'.chat.'+chat_url)
        redis_session_meta = redis.hgetall('session.'+mysql_session.session_id+'.meta.'+chat_url)
        # Delete the session from mysql if it's been deleted from redis.
        if len(redis_session)==0 or len(redis_session_meta)==0:
            mysql.delete(mysql_session)
            continue
        expiry_time = datetime.datetime.fromtimestamp(
            redis.zscore('chat-sessions', chat_url+'/'+mysql_session.session_id) or 0
        )
        default_character = CHARACTER_DETAILS[redis_session['character']]
        mysql_session.expiry_time = expiry_time
        mysql_session.group = redis_session_meta['group']
        mysql_session.character = redis_session['character']
        mysql_session.name = redis_session.get('name', default_character['name'])
        mysql_session.acronym = redis_session.get('acronym', default_character['acronym'])
        mysql_session.color = redis_session.get('color', default_character['color'])
        mysql_session.case = redis_session.get('case', default_character['case'])
        mysql_session.replacements = redis_session.get('replacements', default_character['replacements'])
        # XXX NEED TO UNCOMMENT THESE WHEN WE MERGE NEW QUIRKS
        #mysql_session.regexes = redis_session.get('regexes', default_character['regexes'])
        mysql_session.quirk_prefix = redis_session.get('quirk_prefix', default_character['quirk_prefix'])
        #mysql_session.quirk_suffix = redis_session.get('quirk_suffix', default_character['quirk_suffix'])
        del redis_sessions[str(mysql_session.counter)]
    # And create the ones which aren't.
    for counter, session_id in redis_sessions.items():
        redis_session = redis.hgetall('session.'+session_id+'.chat.'+chat_url)
        redis_session_meta = redis.hgetall('session.'+session_id+'.meta.'+chat_url)
        expiry_time = datetime.datetime.fromtimestamp(
            redis.zscore('chat-sessions', chat_url+'/'+session_id) or 0
        )
        default_character = CHARACTER_DETAILS[redis_session['character']]
        mysql_session = ChatSession(
            log_id=log.id,
            session_id=session_id,
            counter=counter,
            expiry_time=expiry_time,
            group=redis_session_meta['group'],
            character=redis_session['character'],
            name=redis_session.get('name', default_character['name']),
            acronym=redis_session.get('acronym', default_character['acronym']),
            color=redis_session.get('color', default_character['color']),
            case=redis_session.get('case', default_character['case']),
            replacements=redis_session.get('replacements', default_character['replacements']),
            # XXX NEED TO UNCOMMENT THESE WHEN WE MERGE NEW QUIRKS
            #regexes=redis_session.get('regexes', default_character['regexes']),
            quirk_prefix=redis_session.get('quirk_prefix', default_character['quirk_prefix']),
            #quirk_suffix=redis_session.get('quirk_suffix', default_character['quirk_suffix']),
        )
        mysql.add(mysql_session)
    mysql.flush()
    # Text
    # XXX MAKE REALLY REALLY REALLY GODDAMN SURE THIS WORKS WITH MINUS NUMBERS
    # XXX FOR GOD'S SAKE
    lines = redis.lrange('chat.'+chat_url, 0, -1)
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
    redis.ltrim('chat.'+chat_url, len(lines), -1)
    return log.id

def delete_chat_session(redis, chat_url, session_id):

    counter = redis.hget('session.'+session_id+'.meta.'+chat_url, 'counter')
    pipe = redis.pipeline()
    pipe.hdel('chat.'+chat_url+'.counters', counter)
    pipe.delete('session.'+session_id+'.chat.'+chat_url)
    pipe.delete('session.'+session_id+'.meta.'+chat_url)
    pipe.srem('session.'+session_id+'.chats', chat_url)
    pipe.zrem('chat-sessions', chat_url+'/'+session_id)
    pipe.execute()

def delete_chat(redis, mysql, chat_url):

    # XXX PIPELINE THIS???

    # Delete metadata first because it's used to check whether a chat exists.
    redis.delete('chat.'+chat_url+'.meta')

    redis.delete('chat.'+chat_url+'.online')
    redis.delete('chat.'+chat_url+'.idle')
    redis.delete('chat.'+chat_url+'.characters')

    for session_id in redis.hvals('chat.'+chat_url+'.counters'):
        redis.srem('session.'+session_id+'.chats', chat_url)
        redis.delete('session.'+session_id+'.chat.'+chat_url)
        redis.delete('session.'+session_id+'.meta.'+chat_url)
        redis.zrem('chat-sessions', chat_url+'/'+session_id)

    redis.delete('chat.'+chat_url+'.counters')
    redis.delete('chat.'+chat_url)

def delete_session(redis, session_id):

    for chat in redis.smembers('session.'+session_id+'.chats'):
        delete_chat_session(redis, chat_url, session_id)

    redis.delete('session.'+session_id)
    redis.delete('session.'+session_id+'.meta')
    redis.delete('session.'+session_id+'.picky')
    redis.delete('session.'+session_id+'.picky-groups')
    redis.delete('session.'+session_id+'.picky-exclude')
    redis.delete('session.'+session_id+'.picky-exclude-groups')
    redis.delete('session.'+session_id+'.picky-options')
    redis.zrem('all-sessions', session_id)

