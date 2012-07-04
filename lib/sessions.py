import json

from flask import g

class Session(object):

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

        chat_data = Session.DEFAULTS

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

    def character_dict(self, unpack_replacements=False, hide_silence=True):
        character_dict = dict((attrib, getattr(self, attrib)) for attrib in Session.DEFAULTS.keys())
        # Don't tell silenced users that they're silenced.
        if hide_silence and character_dict['group']=='silent':
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

        # Truncate acronym to 10 characters.
        self.acronym = form['acronym'][:10]

        # Validate name
        if len(form['name'])>0:
            # Truncate name to 50 characters.
            self.name = form['name'][:50]
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

        db.hmset(self.chat_prefix, self.character_dict(hide_silence=False))

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
            self.db.hmset(self.chat_prefix, self.character_dict(hide_silence=False))

    def set_group(self, group):
        self.group = group
        self.db.hset(self.chat_prefix, 'group', group)

def get_counter(chat, session):
    return g.db.lrange('chat.'+chat+'.counter', 0, -1).index(session)

