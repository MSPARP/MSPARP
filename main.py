from flask import Flask, g, request, render_template, redirect, url_for, jsonify, abort

from lib import SEARCH_PERIOD, get_time, validate_chat_url
from lib.characters import CHARACTER_GROUPS, CHARACTERS
from lib.messages import parse_line
from lib.requests import connect_redis, create_normal_session, set_cookie

app = Flask(__name__)

# Pre and post request stuff
app.before_request(connect_redis)
app.before_request(create_normal_session)
app.after_request(set_cookie)

# Helper functions

def show_homepage(error):
    return render_template('frontpage.html',
        error=error,
        user=g.user,
        character_dict=g.user.character_dict(unpack_replacements=True),
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        default_char=g.user.character,
        users_searching=g.redis.zcard('searchers'),
        users_chatting=g.redis.scard('sessions-chatting')
    )

# Chat

@app.route('/chat')
@app.route('/chat/<chat>')
def chat(chat=None):

    # Delete value from the matchmaker.
    if g.redis.get('session.'+g.user.session+'.match'):
        g.redis.delete('session.'+g.user.session+'.match')

    if chat is None:
        chat_type = 'match'
        existing_lines = []
        latest_num = -1
    else:
        # Check if chat exists
        chat_type = g.redis.get('chat.'+chat+'.type')
        if chat_type is None:
            abort(404)
        # Load chat-based session data.
        g.user.set_chat(chat)
        existing_lines = [parse_line(line, 0) for line in g.redis.lrange('chat.'+chat, 0, -1)]
        latest_num = len(existing_lines)-1

    return render_template(
        'chat.html',
        user=g.user,
        character_dict=g.user.character_dict(unpack_replacements=True),
        groups=CHARACTER_GROUPS,
        characters=CHARACTERS,
        chat=chat,
        chat_type=chat_type,
        lines=existing_lines,
        latest_num=latest_num
    )

# Searching

@app.route('/search', methods=['POST'])
def foundYet():
    target=g.redis.get('session.'+g.user.session+'.match')
    if target:
        return jsonify(target=target)
    else:
        g.redis.zadd('searchers', g.user.session, get_time(SEARCH_PERIOD*2))
        abort(404)

@app.route('/stop_search', methods=['POST'])
def quitSearching():
    g.redis.zrem('searchers', g.user.session)
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
            if g.redis.exists('chat.'+chat):
                raise ValueError('chaturl_taken')
            # USE VALIDATE_CHAT_URL
            if not validate_chat_url(chat):
                raise ValueError('chaturl_invalid')
            g.user.set_chat(chat)
            g.user.set_group('mod')
            g.redis.set('chat.'+chat+'.type', 'group')
            return redirect(url_for('chat', chat=chat))
    except ValueError as e:
        return show_homepage(e.args[0])

    if 'search' in request.form:
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('configure'))

# Home

@app.route("/")
def configure():
    return show_homepage(None)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

