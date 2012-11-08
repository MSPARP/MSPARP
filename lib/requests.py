from flask import g, request, abort
from redis import Redis

from lib import validate_chat_url
from characters import CHARACTER_DETAILS
from model import sm
from sessions import Session

# Application start

def populate_all_chars():
    redis = Redis(unix_socket_path='/tmp/redis.sock')
    pipe = redis.pipeline()
    pipe.delete('all-chars')
    pipe.sadd('all-chars', *CHARACTER_DETAILS.keys())
    pipe.execute()
    del pipe
    del redis

# Before request

def connect_redis():
    # Connect to database 
    g.redis = Redis(unix_socket_path='/tmp/redis.sock')

def connect_mysql():
    g.mysql = sm()

def create_normal_session():
    # Create a user object, using session ID.
    session = request.cookies.get('session', None)
    g.user = Session(g.redis, session)

def create_chat_session():
    # Create a user object, using session and chat IDs.
    session = request.cookies.get('session', None)
    # Don't accept chat requests if there's no cookie.
    if session is None:
        abort(400)
    # Validate chat ID.
    if 'chat' in request.form and validate_chat_url(request.form['chat']):
        chat = request.form['chat']
    else:
        abort(400)
    g.chat_type = g.redis.hget('chat.'+chat+'.meta', 'type')
    if g.chat_type is None:
        abort(404)
    g.user = user = Session(g.redis, session, chat)

# After request

def set_cookie(response):
    if request.cookies.get('session', None) is None:
        try:
            response.set_cookie('session', g.user.session, max_age=365*24*60*60)
        except AttributeError:
            # That isn't gonna work if we don't have a user object, just ignore it.
            pass
    return response

def disconnect_redis(response):
    del g.redis
    return response

def disconnect_mysql(response):
    g.mysql.close()
    del g.mysql
    return response
