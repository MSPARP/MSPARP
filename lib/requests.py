from flask import g, request
from redis import Redis

from sessions import Session

def connect():
    # connect to database 
    db = g.db = Redis(host='localhost')
    # Create a user object, using session and chat IDs if present.
    session = request.cookies.get('session', None)
    if (session is None and request.url_rule is not None
        and request.url_rule.endpoint in ("postMessage", "pingServer", "getMessages", "quitChatting")):
        # Don't accept chat requests if there's no cookie.
        abort(400)
    if request.form is not None and 'chat' in request.form:
        chat = request.form['chat']
    elif request.view_args is not None and 'chat' in request.view_args:
        chat = request.view_args['chat']
    else:
        chat = None
    g.user = user = Session(db, session, chat)

def set_cookie(response):
    if request.cookies.get('session', None) is None:
        try:
            response.set_cookie('session', g.user.session, max_age=365*24*60*60)
        except AttributeError:
            # That isn't gonna work if we don't have a user object, just ignore it.
            pass
    return response
