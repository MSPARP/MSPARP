import itertools, re, time

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

    ATTRIBUTES=['acronym', 'name', 'color', 'character', 'picky']

    def __init__(self, session):
        self.session = session
        self.acronym = u'??'
        self.name = u'Anonymous'
        self.color = '000000'
        self.character = 'anonymous/other'
        self.quirks = set()
        self.quirkargs = defaultdict(list)
        self.picky = False
        self.picky_characters = set()
        self.fresh = True

    def load(self,db):

        self.fresh = False
        prefix = self.prefix

        stored_data = db.hgetall(prefix)
        for attrib, value in stored_data.items():
            if value is not None:
                if attrib in ('picky',):
                    setattr(self, attrib, (value=='True'))
                else:
                    setattr(self, attrib, unicode(value, encoding='utf-8'))

        if self.picky:
            self.picky_characters = db.smembers(prefix+'-picky-chars')
        else:
            self.picky_characters = db.smembers('all-chars')

        quirks = self.quirks = db.smembers(prefix+'-quirks')
        qa = self.quirkargs = defaultdict(list)
        for q in quirks:
            qa[q] = [unicode(_, encoding='utf-8') for _ in db.lrange(prefix+'-quirks-'+q, 0, -1)]
    
    def save(self,db):

        prefix = self.prefix

        db.hmset(prefix, dict((attrib, getattr(self, attrib)) for attrib in User.ATTRIBUTES))

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

    @property
    def prefix(self):
        return 'session-'+self.session
    
    def apply(self,form):

        setattr(self, 'acronym', form['acronym'])

        # Validate name
        if len(form['name'])>0:
            setattr(self, 'name', form['name'])
        else:
            raise ValueError("name")

        # Validate colour
        if re.compile('^[0-9a-fA-F]{6}$').search(form['color']):
            setattr(self, 'color', form['color'])
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

def announceIfNew(chatid):
    chatkey = 'chat-%s-sessions' % chatid
    if not g.db.sismember(chatkey, g.user.session):
        g.db.sadd(chatkey, g.user.session)
        addSystemMessage(g.db, chatid, '%s [%s] joined chat' % (g.user.name, g.user.acronym))

def markAlive(chatid):
    g.db.zadd('chats-alive', chatid+'/'+g.user.session, getTime())    
    g.db.sadd('sessions-chatting', g.user.session)

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

# Cookie management

@app.before_request
def connect():
    # connect to database 
    db = g.db = Redis(host='localhost')

    # if the user has logged in, go ahead and load their user object
    session = request.cookies.get('session',None)
    if session is not None:
        g.user = user = User(session)
        user.load(db)
    else:
        g.user = user = User(str(uuid4()))
        user.save(g.db)

@app.after_request
def set_cookie(response):
    if request.cookies.get('session', None) is None:
        response.set_cookie('session', g.user.session, max_age=365*24*60*60)
    return response

# Chat

@app.route('/chat/<chat:chatid>')
def chat(chatid):

    existing_lines = [parseLine(line, 0) for line in g.db.lrange('chat-'+chatid, 0, -1)]
    latestNum = len(existing_lines)-1
    quirks_func, quirks_args=g.user.buildQuirksFunction()

    return render_template(
        'chat.html',
        user=g.user,
        chatid=chatid,
        lines=existing_lines,
        latestNum=latestNum,
        applyQuirks=quirks_func,
        quirks_args=quirks_args
    )

@app.route('/chat/<chat:chatid>/post', methods=['POST'])
def postMessage(chatid):
    addMessage(g.db, chatid, g.user.color, g.user.acronym, request.form['line'])
    markAlive(chatid)
    return 'ok'

@app.route('/chat/<chat:chatid>/ping', methods=['POST'])
def pingServer(chatid):
    markAlive(chatid)
    return 'ok'

@app.route('/chat/<chat:chatid>/messages', methods=['POST'])
def getMessages(chatid):

    after = int(request.form['after'])
    announceIfNew(chatid)
    markAlive(chatid)
    messages = g.db.lrange('chat-'+chatid, after+1, -1)

    if messages:
        return parseMessages(messages, after+1)
    g.db.subscribe('channel-'+chatid)

    for msg in g.db.listen():
        if msg['type']=='message':
            id, rest = msg['data'].split('#', 1)
            return parseMessages([rest], int(id)) # TEST THIS

@app.route('/bye/chat/<chat:chatid>', methods=['POST'])
def quitChatting(chatid):
    # Check if they're actually a member of the chat first?
    g.db.zrem('chats-alive', chatid+'/'+g.user.session)
    g.db.srem(('chat-%s-sessions' % chatid), g.user.session)
    g.db.srem('sessions-chatting', g.user.session)
    addSystemMessage(g.db, chatid, '%s [%s] disconnected.' % (g.user.name, g.user.acronym))
    return 'ok'

# Searching

@app.route('/matches', methods=['POST'])
def findMatches():

    try:
        g.user.apply(request.form)
    except ValueError as e:
        return show_homepage(e.args[0])
    g.user.save(g.db)

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

