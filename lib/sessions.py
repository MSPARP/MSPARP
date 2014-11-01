try:
    import ujson as json
except:
    import json
import re

from flask import g, request
from uuid import uuid4

from lib import DELETE_SESSION_PERIOD, get_time
from characters import CHARACTER_DETAILS
from messages import send_message

# XXX Move this to characters.py?
CASE_OPTIONS = {
    'normal': 'Normal',
    'upper': 'UPPER CASE',
    'lower': 'adaptive lower',
    'title': 'Title Case',
    'inverted': 'iNVERTED',
    'alternating': 'AlTeRnAtInG CaSe',
	'alt-lines': 'alternating LINES',
	'proper': 'Proper grammar',
	'first-caps': 'First letter caps'
}

META_DEFAULTS = {
    'group': 'user'
}

class Session(object):

    def __init__(self, redis, session_id=None, chat=None):

        self.redis = redis
        self.session_id = session_id or str(uuid4())
        self.chat = chat

        original_prefix = 'session.'+self.session_id
        original_meta_prefix = original_prefix+'.meta'

        # Load metadata and character data.
        if chat is not None:
            self.prefix = original_prefix+'.chat.'+chat
            self.meta_prefix = original_meta_prefix+'.'+chat
            self.meta = get_or_create(
                redis,
                self.meta_prefix,
                lambda: new_chat_metadata(redis, chat, session_id)
            )
            character = get_or_create(
                redis,
                self.prefix,
                lambda: get_or_create(
                    redis,
                    original_prefix,
                    # Redis hashes can't be empty - if there are no keys they are auto-deleted.
                    # So we store the character ID in this dict so it always has at least one.
                    lambda: dict([('character', 'anonymous/other')]+CHARACTER_DETAILS['anonymous/other'].items())
                )
            )
        else:
            self.prefix = original_prefix
            self.meta_prefix = original_meta_prefix
            self.meta = get_or_create(redis, original_meta_prefix, lambda: META_DEFAULTS)
            character = get_or_create(
                redis,
                self.prefix,
                lambda: dict([('character', 'anonymous/other')]+CHARACTER_DETAILS['anonymous/other'].items())
            )

        # Fill in missing fields from the characters dict.
        self.character = fill_in_data(character)

        # Character encodings are stupid.
        self.unicodify()

        redis.zadd('all-sessions', self.session_id, get_time(DELETE_SESSION_PERIOD))
        if chat is not None:
            redis.zadd('chat-sessions', self.chat+'/'+self.session_id, get_time(DELETE_SESSION_PERIOD))

    def unicodify(self):
        for key in self.meta.keys():
            try:
                self.meta[key] = unicode(self.meta[key], encoding='utf-8')
            except TypeError:
                # Don't care if it's already unicode.
                pass
        for key in self.character.keys():
            try:
                self.character[key] = unicode(self.character[key], encoding='utf-8')
            except TypeError:
                # Don't care if it's already unicode.
                pass

    def json_info(self):
        # Unpack the replacement info.
        unpacked_character = dict(self.character)
        unpacked_character['replacements'] = json.loads(unpacked_character['replacements'])
        return { 'meta': self.meta, 'character': unpacked_character }

    def save(self, form):
        self.save_character(form)
        self.save_pickiness(form)

    def save_character(self, form):

        redis = self.redis
        character = self.character

        old_acronym = character.get('acronym', '')
        old_name = character.get('name', '')
        old_color = character.get('color', '000000')

        # Truncate acronym to 15 characters.
        character['acronym'] = form['acronym'][:15]

        # Validate name
        if len(form['name'])>0:
            # Truncate name to 50 characters.
            character['name'] = form['name'][:50]
        else:
            raise ValueError("name")

        # Validate colour
        if re.compile('^[0-9a-fA-F]{6}$').search(form['color']):
            character['color'] = form['color']
        else:
            raise ValueError("color")

        # Validate character
        # XXX Get all-chars from CHARACTER_DEFAULTS.keys()?
        if form['character'] in redis.smembers('all-chars'):
            character['character'] = form['character']
        else:
            raise ValueError("character")

        character['quirk_prefix'] = form['quirk_prefix']
        character['quirk_suffix'] = form['quirk_suffix']

        # Validate case
        if form['case'] in CASE_OPTIONS.keys():
            character['case'] = form['case']
        else:
            raise ValueError("case")

        replacements = zip(form.getlist('quirk_from'), form.getlist('quirk_to'))
        # Strip out any rows where from is blank or the same as to.
        replacements = [_ for _ in replacements if _[0]!='' and _[0]!=_[1]]
        # And encode as JSON.
        character['replacements'] = json.dumps(replacements)

        saved_character = dict(character)
        for key, value in CHARACTER_DETAILS[character['character']].items():
            if saved_character[key]==value:
                del saved_character[key]
        pipe = redis.pipeline()
        pipe.delete(self.prefix)
        pipe.hmset(self.prefix, saved_character)
        pipe.execute()

        # Chat-related things.
        if self.chat is not None:
            redis.sadd('chat.'+self.chat+'.characters', character['character'])
            if character['name']!=old_name or character['acronym']!=old_acronym:
                if self.meta['group']=='silent':
                    user_change_message = None
                else:
                    user_change_message = '%s [%s] is now %s [%s]. ~~ %s ~~' % (old_name, old_acronym, character['name'], character['acronym'], self.meta['counter'])
                send_message(redis, request.form['chat'], -1, 'user_change', user_change_message)
            elif character['color']!=old_color:
                send_message(redis, request.form['chat'], -1, 'user_change', None)

    def save_pickiness(self, form):
        # Characters
        picky_key = self.prefix+'.picky'
        self.redis.delete(picky_key)
        chars = self.picky = set(k[6:] for k in form.keys() if k.startswith('picky-'))
        if len(CHARACTER_DETAILS)>len(chars)>0:
            self.redis.sadd(picky_key, *chars)
        # Other options
        option_key = self.prefix+'.picky-options'
        for option in ['para', 'nsfw']:
            if option in form and form[option] in ['0', '1']:
                self.redis.hset(option_key, option, int(form[option]))
            else:
                self.redis.hdel(option_key, option)

    def set_chat(self, chat):
        if self.chat is None:
            # XXX This is pretty much just cut and pasted from __init__().
            self.chat = chat
            self.prefix = self.prefix+'.chat.'+chat
            self.meta_prefix = self.meta_prefix+'.'+chat
            self.meta = get_or_create(
                self.redis,
                self.meta_prefix,
                lambda: new_chat_metadata(self.redis, chat, self.session_id)
            )
            character = get_or_create(
                self.redis,
                self.prefix,
                lambda: self.character
            )
            self.character = fill_in_data(character)
            self.unicodify()

    def set_group(self, group):
        self.meta['group'] = group
        self.redis.hset(self.meta_prefix, 'group', group)


def get_or_create(redis, key, default):
    data = redis.hgetall(key)
    if data is None or len(data)==0:
        data = default()
        redis.hmset(key, data)
    return data

def new_chat_metadata(redis, chat, session_id):
    # This can be overloaded as a general hook for joining a chat for the first time.
    if type(redis.sismember('global-mods', session_id)) == bool and redis.sismember('global-mods', session_id):
        metadata = { 'group': 'globalmod' }
    elif redis.hget('chat.'+chat+'.meta', 'autosilence')=='1':
        metadata = { 'group': 'silent' }
    else:
        metadata = dict(META_DEFAULTS)
    metadata['counter'] = redis.hincrby('chat.'+chat+'.meta', 'counter', 1)
    redis.hset('chat.'+chat+'.counters', metadata['counter'], session_id)
    redis.sadd('session.'+session_id+'.chats', chat)
    return metadata

def fill_in_data(character_data):
    if len(character_data)<len(CHARACTER_DETAILS[character_data['character']])+1:
        new_character_data = dict(CHARACTER_DETAILS[character_data['character']])
        new_character_data.update(character_data)
        return new_character_data
    return character_data

class PartialSession(object):

    def __init__(self, redis, session, chat):
        self.redis = redis
        self.session = session
        self.chat = chat
        self.character = None

    def __getattr__(self, attr):
        value = self.redis.hget('session.'+self.session+'.chat.'+self.chat, attr)
        if value is None:
            if self.character is None:
                self.character = self.redis.hget('session.'+self.session+'.chat.'+self.chat, 'character')
            value = CHARACTER_DETAILS[self.character][attr]
        setattr(self, attr, value)
        return value

