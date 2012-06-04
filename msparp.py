import itertools, re, time

from functools import wraps
from flask import Flask, g, request, render_template, make_response, redirect, url_for, jsonify, abort
from redis import Redis
from uuid import uuid4
from collections import defaultdict
from werkzeug.routing import BaseConverter, ValidationError

from characters import CHARACTER_GROUPS, CHARACTERS
from quirks import QUIRKS
from reaper import getTime
from messages import addMessage, addSystemMessage


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

    ATTRIBUTES = ['acronym', 'name', 'color', 'character', 'picky']
    DEFAULTS = { 'acronym': '??', 'name': 'Anonymous', 'color': '000000', 'character': 'anonymous/other', 'picky': False }

    def __init__(self, db, session=None, chat=None):

        self.db = db
        self.session = session or str(uuid4())
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
            if attrib in ('picky',):
                setattr(self, attrib, (value=='True'))
            else:
                setattr(self, attrib, unicode(value, encoding='utf-8'))

        # XXX lazy loading on these?

        self.picky_characters = db.smembers(self.prefix+'-picky-chars')

        self.quirks = db.smembers(self.prefix+'-quirks')
        self.quirkargs = defaultdict(list)
        for quirk in self.quirks:
            self.quirkargs[quirk] = [unicode(_, encoding='utf-8') for _ in db.lrange(self.prefix+'-quirks-'+quirk, 0, -1)]


    def save(self):

        db = self.db
        prefix = self.prefix

        db.hmset(self.chat_prefix, dict((attrib, getattr(self, attrib)) for attrib in User.ATTRIBUTES))

        db.sadd('all-sessions', self.session)

        ckey = prefix+'-picky-chars'
        if self.picky:
            db.delete(ckey)
            for char in self.picky_characters:
                db.sadd(ckey, char)
        else:
            db.sunionstore(ckey, ('all-chars',))

        quirkey = prefix+'-quirks'
        db.delete(quirkey)
        for quirk in self.quirks:
            db.sadd(quirkey, quirk)
        for key, values in self.quirkargs.items():
            rkey = quirkey+'-'+key
            if values:
                db.delete(rkey)
                for v in values:
                    db.rpush(rkey, v)
    
    def apply(self,form):

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

        picky = self.picky = 'picky' in form
        if picky:
            chars = self.picky_characters = set(k[6:] for k in form.keys() if k.startswith('picky-'))
            if not chars:
                raise ValueError("no_characters")

        quirks = self.quirks = set(k[6:] for k in form.keys() if k.startswith('quirk-'))
        qa = self.quirkargs = defaultdict(list)
        for q in quirks:
            qa[q] = [value for (key,value) in sorted(form.items()) if key.startswith('qarg-'+q)]

        self.save()
    
    def buildQuirksFunction(self):

        wrap = 'text'
        qa = self.quirkargs
        vcount = itertools.count()
        args = {}

        for q in self.quirks:
            values = qa.get(q, [])
            if values:
                params = [('qarg'+str(num), value) for (num, value) in itertools.izip(vcount, values)]
                args.update(dict(params))
                wrap='%s(%s,%s)' % (q, wrap, ','.join(k for (k,v) in params))
            else:
                wrap='%s(%s)' % (q,wrap)
        return wrap,args


# Helper functions

def parseLine(line, id):
    "Parse a chat line like 'FF00FF#Some Text' into a dict"
    parts = line.split('#', 1)
    return {
        'id': id,
        'color': parts[0],
        'line': unicode(parts[1], encoding='utf-8')
    }

def parseMessages(seq, offset):
    return jsonify(messages=[parseLine(line, i) for (i, line) in enumerate(seq, offset)])

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character,
        quirks=QUIRKS,
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
            addSystemMessage(g.db, chat, '%s [%s] joined chat' % (g.user.name, g.user.acronym))
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
    chat = (request.form['chat'] if 'chat' in request.form else
            request.view_args['chat'] if 'chat' in request.view_args else None)
    g.user = user = User(db, session, chat)

@app.after_request
def set_cookie(response):
    if request.cookies.get('session', None) is None:
        response.set_cookie('session', g.user.session, max_age=365*24*60*60)
    return response

# Chat

@app.route('/chat/<chat:chat>')
def chat(chat):

    existing_lines = [parseLine(line, 0) for line in g.db.lrange('chat-'+chat, 0, -1)]
    latestNum = len(existing_lines)-1
    quirks_func, quirks_args=g.user.buildQuirksFunction()

    return render_template(
        'chat.html',
        user=g.user,
        chat=chat,
        lines=existing_lines,
        latestNum=latestNum,
        applyQuirks=quirks_func,
        quirks_args=quirks_args
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
        return parseMessages(messages, after+1)
    g.db.subscribe('channel-'+request.form['chat'])

    for msg in g.db.listen():
        if msg['type']=='message':
            id, rest = msg['data'].split('#', 1)
            return parseMessages([rest], int(id)) # TEST THIS

@app.route('/bye', methods=['POST'])
@validate_chat
def quitChatting():
    # Check if they're actually a member of the chat first?
    g.db.zrem('chats-alive', request.form['chat']+'/'+g.user.session)
    g.db.srem(('chat-%s-sessions' % request.form['chat']), g.user.session)
    g.db.srem('sessions-chatting', g.user.session)
    addSystemMessage(g.db, request.form['chat'], '%s [%s] disconnected.' % (g.user.name, g.user.acronym))
    return 'ok'

# Searching

@app.route('/matches', methods=['POST'])
def findMatches():

    try:
        g.user.apply(request.form)
    except ValueError as e:
        return show_homepage(e.args[0])

    if 'chat' in request.form:
        session = g.user.session
        g.db.zadd('searchers', session, getTime())
        g.db.publish('search-alert', session)
        g.db.delete('chat-'+session)
        return render_template("searching.html")
    else:
        return redirect(url_for('configure'))

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

