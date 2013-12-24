from flask import g, request, abort
from redis import ConnectionPool, Redis

from lib import validate_chat_url
from characters import CHARACTER_DETAILS
from model import sm
from sessions import Session
import os

# Connection pooling. This takes far too much effort.
redis_pool = ConnectionPool(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])

# Application start

def populate_all_chars():
    redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])
    pipe = redis.pipeline()
    pipe.delete('all-chars')
    pipe.sadd('all-chars', *CHARACTER_DETAILS.keys())
    pipe.execute()
    del pipe
    del redis

# Before request

def connect_redis():
    # Connect to database 
    g.redis = Redis(connection_pool=redis_pool)

def connect_mysql():
    g.mysql = sm()

def create_normal_session():
    # Create a user object, using session ID.
    session_id = request.cookies.get('session', None)
    g.user = Session(g.redis, session_id)

def create_chat_session():
    # Create a user object, using session and chat IDs.
    session_id = request.cookies.get('session', None)
    # Don't accept chat requests if there's no cookie.
    if session_id is None:
        abort(400)
    # Validate chat ID.
    if 'chat' in request.form and validate_chat_url(request.form['chat']):
        chat = request.form['chat']
    else:
        abort(400)
    g.chat_type = g.redis.hget('chat.'+chat+'.meta', 'type')
    if g.chat_type is None:
        abort(404)
    g.user = user = Session(g.redis, session_id, chat)

# After request

def set_cookie(response):
    if request.cookies.get('session', None) is None:
        try:
            response.set_cookie('session', g.user.session_id, max_age=365*24*60*60)
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
