import itertools, re, time

from functools import wraps
from flask import Flask, g, request, render_template, make_response, redirect, url_for, jsonify, abort
from redis import Redis
from uuid import uuid4
from collections import defaultdict
from werkzeug.routing import BaseConverter, ValidationError

from characters import CHARACTER_GROUPS, CHARACTERS
from reaper import getTime
from messages import addMessage, addSystemMessage, get_user_list, parseLine, parseMessages


class ChatIDConverter(BaseConverter):

    def __init__(self, url_map):
        super(ChatIDConverter, self).__init__(url_map)

    def to_python(self, value):
        if re.match('^[-a-zA-Z0-9]+$',value):
            return value
        else:
            raise ValidationError()

    def to_url(self, value):
        return value

app = Flask(__name__)
app.url_map.converters['chat'] = ChatIDConverter


class User(object):

    CASE_OPTIONS = {
        'normal': 'Normal',
        'upper': 'UPPER CASE',
        'lower': 'lower case',
        'title': 'Title Case',
        'inverted': 'iNVERTED',
        'alternating': 'AlTeRnAtInG'
    }

    DEFAULTS = {
        'acronym': '??',
        'name': 'Anonymous',
        'color': '000000',
        'character': 'anonymous/other',
        'quirk_prefix': '',
        'case': 'normal'
    }

    def __init__(self, db, session=None, chat=None):

        self.db = db
        self.session = session or str(uuid4())
        self.chat = chat
        self.prefix = self.chat_prefix = "session-"+self.session

        chat_data = User.DEFAULTS

        # Load global session data.
        if db.exists(self.prefix):
            chat_data = db.hgetall(self.chat_prefix)
        else:
            db.hmset(self.prefix, chat_data)

        # Load chat-specific data.
        if chat is not None:
            self.chat_prefix += '-'+chat
            if db.exists(self.chat_prefix):
                chat_data = db.hgetall(self.chat_prefix)
            else:
                db.hmset(self.chat_prefix, chat_data)

        for attrib, value in chat_data.items():
            setattr(self, attrib, unicode(value, encoding='utf-8'))

        # XXX lazy loading on these?

        self.picky = db.smembers(self.prefix+'-picky')

    def character_dict(self):
        return dict((attrib, getattr(self, attrib)) for attrib in User.DEFAULTS.keys())

    def save(self, form):
        self.save_character(form)
        self.save_pickiness(form)

    def save_character(self, form):

        db = self.db
        prefix = self.prefix

        old_name = self.name
        old_acronym = self.acronym

        self.acronym = form['acronym']

        # Validate name
        if len(form['name'])>0:
            self.name = form['name']
        else:
            raise ValueError("name")

        # Validate colour
        if re.compile('^[0-9a-fA-F]{6}$').search(form['color']):
            self.color = form['color']
        else:
            raise ValueError("color")

        # Validate character
        if form['character'] in g.db.smembers('all-chars'):
            setattr(self, 'character', form['character'])
        else:
            raise ValueError("character")

        self.quirk_prefix = form['quirk_prefix']

        # Validate case
        if form['case'] in self.CASE_OPTIONS.keys():
            setattr(self, 'case', form['case'])
        else:
            raise ValueError("case")

        db.hmset(self.chat_prefix, self.character_dict())

        if (self.chat is not None and self.session in g.db.smembers('chat-%s-sessions' % self.chat)
            and (self.name!=old_name or self.acronym!=old_acronym)):
            addSystemMessage(g.db, request.form['chat'], '%s [%s] is now %s [%s].' % (old_name, old_acronym, self.name, self.acronym), True)

        db.sadd('all-sessions', self.session)

    def save_pickiness(self, form):

        ckey = self.prefix+'-picky'
        self.db.delete(ckey)

        if 'picky' in form:
            chars = self.picky = set(k[6:] for k in form.keys() if k.startswith('picky-'))
            if not chars:
                raise ValueError("no_characters")
            for char in self.picky:
                self.db.sadd(ckey, char)


# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character,
        users_searching=g.db.zcard('searchers'),
        users_chatting=g.db.scard('sessions-chatting')
    )

# Decorators

def validate_chat(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'chat' in request.form and re.match('^[-a-zA-Z0-9]+$', request.form['chat']):
            return f(*args, **kwargs)
        abort(400)
    return decorated_function

def mark_alive(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        chat = request.form['chat']
        chatkey = 'chat-%s-sessions' % chat
        if not g.db.sismember(chatkey, g.user.session):
            g.db.sadd(chatkey, g.user.session)
            addSystemMessage(g.db, chat, '%s [%s] joined chat.' % (g.user.name, g.user.acronym), True)
        g.db.zadd('chats-alive', chat+'/'+g.user.session, getTime())    
        g.db.sadd('sessions-chatting', g.user.session)
        return f(*args, **kwargs)
    return decorated_function

# Cookie management

@app.before_request
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
    g.user = user = User(db, session, chat)

@app.after_request
def set_cookie(response):
    if request.cookies.get('session', None) is None:
        try:
            response.set_cookie('session', g.user.session, max_age=365*24*60*60)
        except AttributeError:
            # That isn't gonna work if we don't have a user object, just ignore it.
            pass
    return response

# Chat

@app.route('/chat/<chat:chat>')
def chat(chat):

    # Delete value from the matchmaker.
    if g.db.get('chat-'+g.user.session):
        g.db.delete('chat-'+g.user.session)

    existing_lines = [parseLine(line, 0) for line in g.db.lrange('chat-'+chat, 0, -1)]
    latestNum = len(existing_lines)-1

    return render_template(
        'chat.html',
        user=g.user,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        chat=chat,
        lines=existing_lines,
        latestNum=latestNum
    )

@app.route('/post', methods=['POST'])
@validate_chat
@mark_alive
def postMessage():
    addMessage(g.db, request.form['chat'], g.user.color, g.user.acronym, request.form['line'])
    return 'ok'

@app.route('/ping', methods=['POST'])
@validate_chat
@mark_alive
def pingServer():
    return 'ok'

@app.route('/messages', methods=['POST'])
@validate_chat
@mark_alive
def getMessages():

    after = int(request.form['after'])
    messages = g.db.lrange('chat-'+request.form['chat'], after+1, -1)

    if messages:
        return jsonify(messages=parseMessages(messages, after+1), online=get_user_list(g.db, request.form['chat']))

    g.db.subscribe('channel-'+request.form['chat'])
    for msg in g.db.listen():
        if msg['type']=='message':
            # The pubsub channel sends us a JSON string, so we just return that.
            resp = make_response(msg['data'])
            resp.headers['Content-type'] = 'application/json'
            return resp

@app.route('/bye', methods=['POST'])
@validate_chat
def quitChatting():
    # Check if they're actually a member of the chat first?
    g.db.zrem('chats-alive', request.form['chat']+'/'+g.user.session)
    g.db.srem(('chat-%s-sessions' % request.form['chat']), g.user.session)
    g.db.srem('sessions-chatting', g.user.session)
    addSystemMessage(g.db, request.form['chat'], '%s [%s] disconnected.' % (g.user.name, g.user.acronym), True)
    return 'ok'

# Save

@app.route('/save', methods=['POST'])
def save():

    try:
        if 'character' in request.form:
            g.user.save_character(request.form)
        if 'save_pickiness' in request.form:
            g.user.save_pickiness(request.form)
    except ValueError as e:
        if request.is_xhr:
            abort(400)
        else:
            return show_homepage(e.args[0])

    if request.is_xhr:
        return 'ok'
    elif 'match' in request.form:
        return redirect(url_for('findMatches'))
    else:
        return redirect(url_for('configure'))

# Searching

@app.route('/matches')
def findMatches():
        return render_template("searching.html")

@app.route('/matches/foundYet', methods=['POST'])
def foundYet():
    target=g.db.get('chat-'+g.user.session)
    if target:
        return jsonify(target=target)
    else:
        g.db.zadd('searchers', g.user.session, getTime())
        abort(404)

@app.route('/bye/searching', methods=['POST'])
def quitSearching():
    g.db.zrem('searchers', g.user.session)
    return 'ok'

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

