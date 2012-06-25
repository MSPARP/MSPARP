import itertools, json, re, time

from functools import wraps
from flask import Flask, g, request, render_template, make_response, redirect, url_for, jsonify, abort
from redis import Redis
from uuid import uuid4
from collections import defaultdict
from werkzeug.routing import BaseConverter, ValidationError

from characters import CHARACTER_GROUPS, CHARACTERS
from reaper import getTime
from messages import send_message, get_user_list, parseLine, parseMessages


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
        'case': 'normal',
        'replacements': '[]',
        'group': 'user'
    }

    def __init__(self, db, session=None, chat=None):

        self.db = db
        self.session = session or str(uuid4())
        self.chat = chat
        self.prefix = self.chat_prefix = "session."+self.session

        chat_data = User.DEFAULTS

        # Load global session data.
        if db.exists(self.prefix):
            chat_data = db.hgetall(self.chat_prefix)
        else:
            db.hmset(self.prefix, chat_data)

        # Load chat-specific data.
        if chat is not None:
            self.chat_prefix += '.chat.'+chat
            if db.exists(self.chat_prefix):
                chat_data = db.hgetall(self.chat_prefix)
            else:
                db.hmset(self.chat_prefix, chat_data)

        for attrib, value in chat_data.items():
            setattr(self, attrib, unicode(value, encoding='utf-8'))

        # XXX lazy loading on these?

        self.picky = db.smembers(self.prefix+'.picky')

    def character_dict(self, unpack_replacements=False):
        character_dict = dict((attrib, getattr(self, attrib)) for attrib in User.DEFAULTS.keys())
        # Don't tell silenced users that they're silenced.
        if character_dict['group']=='silent':
            character_dict['group'] = 'user'
        if unpack_replacements:
            character_dict['replacements'] = json.loads(character_dict['replacements'])
        return character_dict

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

        self.replacements = zip(form.getlist('quirk_from'), form.getlist('quirk_to'))
        # Strip out any rows where from is blank or the same as to.
        self.replacements = [_ for _ in self.replacements if _[0]!='' and _[0]!=_[1]]
        # And encode as JSON.
        self.replacements = json.dumps(self.replacements)

        db.hmset(self.chat_prefix, self.character_dict())

        if (self.chat is not None and g.db.hget('chat.%s.sessions' % self.chat, self.session) in ['online', 'away']
            and (self.name!=old_name or self.acronym!=old_acronym)):
            send_message(g.db, request.form['chat'], 'user_change', '%s [%s] is now %s [%s].' % (old_name, old_acronym, self.name, self.acronym))

        db.sadd('all-sessions', self.session)

    def save_pickiness(self, form):

        ckey = self.prefix+'.picky'
        self.db.delete(ckey)

        if 'picky' in form:
            chars = self.picky = set(k[6:] for k in form.keys() if k.startswith('picky-'))
            if not chars:
                raise ValueError("no_characters")
            for char in self.picky:
                self.db.sadd(ckey, char)

    def set_chat(self, chat):
        if self.chat is None:
            self.chat = chat
            self.chat_prefix = self.prefix+'.chat.'+chat
            self.db.hmset(self.chat_prefix, self.character_dict())

    def set_group(self, group):
        self.group = group
        self.db.hset(self.chat_prefix, 'group', group)


# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        character_dict=g.user.character_dict(True),
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character,
        users_searching=g.db.zcard('searchers'),
        users_chatting=g.db.scard('sessions-chatting')
    )

def get_counter(chat, session):
    return g.db.lrange('chat.'+chat+'.counter', 0, -1).index(session)

def get_wanted_channels(channel_main, channel_mod, channel_self):
    wanted_channels = set()
    wanted_channels.add(channel_main)
    if g.user.group=='mod':
        # Moderator messages.
        wanted_channels.add(channel_mod)
    if g.user.group=='silent':
        # Channel for self messages if silent.
        wanted_channels.add(channel_self)
    return wanted_channels

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
        state_key = 'chat.%s.sessions' % chat
        session_state = g.db.hget(state_key, g.user.session)
        if session_state is None:
            # This session has never been in this chat before; we need to add them to the counter.
            g.db.rpush('chat.%s.counter' % chat, g.user.session)
            g.db.sadd('session.%s.chats' % g.user.session, chat)
        if session_state not in ['online', 'away']:
            g.db.hset(state_key, g.user.session, 'online')
            send_message(g.db, chat, 'user_change', '%s [%s] joined chat.' % (g.user.name, g.user.acronym))
            g.db.sadd('sessions-chatting', g.user.session)
        g.db.zadd('chats-alive', chat+'/'+g.user.session, getTime())
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
    if g.db.get('session.'+g.user.session+'.match'):
        g.db.delete('session.'+g.user.session+'.match')

    existing_lines = [parseLine(line, 0) for line in g.db.lrange('chat.'+chat, 0, -1)]
    latestNum = len(existing_lines)-1

    return render_template(
        'chat.html',
        user=g.user,
        character_dict=g.user.character_dict(True),
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
    chat = request.form['chat']
    if 'line' in request.form:
        if g.user.group=='silent':
            send_message(g.db, chat, 'private', request.form['line'], g.user.color, g.user.acronym, g.user.session)
        else:
            send_message(g.db, chat, 'message', request.form['line'], g.user.color, g.user.acronym)
    if 'state' in request.form and request.form['state'] in ['online', 'away']:
        current_state = g.db.hget('chat.%s.sessions' % chat, g.user.session)
        if request.form['state']!=current_state:
            g.db.hset('chat.%s.sessions' % chat, g.user.session, request.form['state'])
            if request.form['state']=='away':
                send_message(g.db, chat, 'user_change')
            else:
                send_message(g.db, chat, 'user_change')
    if 'set_group' in request.form and 'counter' in request.form:
        if g.user.group=='mod':
            set_group = request.form['set_group']
            set_session_id = g.db.lindex('chat.%s.counter' % chat, request.form['counter']) or abort(400)
            set_session_key = 'session.%s.chat.%s' % (set_session_id, chat)
            set_session = g.db.hgetall(set_session_key)
            if set_session['group']!=set_group and set_group in ['user', 'mod', 'silent']:
                g.db.hset(set_session_key, 'group', set_group)
                set_message = None
                if set_session['group']!='mod' and set_group=='mod':
                    set_message = '%s [%s] gave moderator status to %s [%s].' % (g.user.name, g.user.acronym, set_session['name'], set_session['acronym'])
                elif set_session['group']=='mod' and set_group!='mod':
                    set_message = '%s [%s] removed moderator status from %s [%s].' % (g.user.name, g.user.acronym, set_session['name'], set_session['acronym'])
                # Refresh the user's subscriptions.
                g.db.publish('channel.'+chat+'.refresh', set_session_id+'#'+set_group)
                send_message(g.db, chat, 'user_change', set_message)
        else:
            abort(403)
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

    chat = request.form['chat']

    after = int(request.form['after'])
    messages = g.db.lrange('chat.'+chat, after+1, -1)

    if messages:
        message_dict = {
            'messages': parseMessages(messages, after+1),
            'online': get_user_list(g.db, chat, 'mod' if g.user.group=='mod' else 'user')
        }
        if 'fetchCounter' in request.form:
            message_dict['counter'] = get_counter(chat, g.user.session)
        return jsonify(message_dict)

    # Channel names.
    channel_main = 'channel.'+chat
    channel_mod = channel_main+'.mod'
    channel_self = channel_main+'.'+g.user.session
    channel_refresh = channel_main+'.refresh'

    # We subscribe to all four channels then ignore what we don't want because
    # changing subscriptions doesn't happen quickly enough and we end up missing
    # messages.
    g.db.subscribe(channel_main)
    g.db.subscribe(channel_mod)
    g.db.subscribe(channel_self)
    g.db.subscribe(channel_refresh)

    # This gives us a list of all the channels we want to listen to.
    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)

    for msg in g.db.listen():
        if msg['type']=='message':
            if msg['channel']==channel_refresh:
                refresh_user, refresh_group = msg['data'].split('#', 1)
                if refresh_user==g.user.session:
                    # Our group has changed. Alter wanted channels accordingly.
                    g.user.group = refresh_group
                    wanted_channels = get_wanted_channels(channel_main, channel_mod, channel_self)
            elif msg['channel'] in wanted_channels:
                # The pubsub channel sends us a JSON string, so we return that instead of using jsonify.
                resp = make_response(msg['data'])
                resp.headers['Content-type'] = 'application/json'
                return resp

@app.route('/bye', methods=['POST'])
@validate_chat
def quitChatting():
    # Check if they're actually a member of the chat first?
    chatkey = 'chat.%s.sessions' % request.form['chat']
    if g.db.hexists(chatkey, g.user.session):
        g.db.zrem('chats-alive', request.form['chat']+'/'+g.user.session)
        g.db.hset(chatkey, g.user.session, 'offline')
        g.db.srem('sessions-chatting', g.user.session)
        send_message(g.db, request.form['chat'], 'user_change', '%s [%s] disconnected.' % (g.user.name, g.user.acronym))
        return 'ok'

# Save

@app.route('/save', methods=['POST'])
def save():
    try:
        if 'character' in request.form:
            g.user.save_character(request.form)
        if 'save_pickiness' in request.form:
            g.user.save_pickiness(request.form)
        if 'create' in request.form:
            chat = request.form['chaturl']
            if g.db.exists('chat.'+chat):
                raise ValueError('chaturl_taken')
            if not re.match('^[-a-zA-Z0-9]+$', chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
            g.user.set_group('mod')
            return redirect(url_for('chat', chat=chat))
    except ValueError as e:
        if request.is_xhr:
            abort(400)
        else:
            return show_homepage(e.args[0])

    if request.is_xhr:
        return 'ok'
    elif 'search' in request.form:
        return redirect(url_for('findMatches'))
    else:
        return redirect(url_for('configure'))

# Searching

@app.route('/matches')
def findMatches():
        return render_template("searching.html")

@app.route('/matches/foundYet', methods=['POST'])
def foundYet():
    target=g.db.get('session.'+g.user.session+'.match')
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

