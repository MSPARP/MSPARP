import datetime
import os
from flask import Flask, g, request, render_template, redirect, url_for, abort
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from webhelpers import paginate

from lib.messages import parse_line
from lib.model import Log, LogPage
from lib.requests import connect_mysql, disconnect_mysql

from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

# Export config
app.config['EXPORT_URL'] = os.environ.get("EXPORT_URL", "http://unsupportedlogs.msparp.com")

app.wsgi_app = ProxyFix(app.wsgi_app, 2)

# Pre and post request stuff
app.before_request(connect_mysql)
app.teardown_request(disconnect_mysql)

# Chat

@app.route('/chat')
@app.route('/chat/<chat>')
def chat(chat=None):
    if chat is None:
        return redirect(url_for("configure"))
    return redirect(url_for("view_log", chat=chat))

@app.route('/logs/group/<chat>')
def old_view_log(chat):
    return redirect(url_for('view_log', chat=chat))

@app.route('/logs/<log_id>')
def view_log_by_id(log_id=None):
    try:
        log_id = int(log_id)
    except ValueError:
        abort(400)
    try:
        log = g.mysql.query(Log).filter(Log.id==log_id).one()
    except NoResultFound:
        abort(404)
    if log.url is not None:
        return redirect(url_for('view_log', chat=log.url))
    abort(404)

@app.route('/chat/<chat>/log')
def view_log(chat=None):

    try:
        log = g.mysql.query(Log).filter(Log.url==chat).one()
    except NoResultFound:
        abort(404)

    current_page = request.args.get('page') or log.page_count
    mode = request.args.get('mode') or 'normal'

    try:
        log_page = g.mysql.query(LogPage).filter(and_(LogPage.log_id==log.id, LogPage.number==current_page)).one()
    except NoResultFound:
        abort(404)

    url_generator = paginate.PageURL(url_for('view_log', chat=chat), {'page': current_page})

    # It's only one row per page and we want to fetch them via both log id and
    # page number rather than slicing, so we'll just give it an empty list and
    # override the count.
    paginator = paginate.Page([], page=current_page, items_per_page=1, item_count=log.page_count, url=url_generator)

    # Pages end with a line break, so the last line is blank.
    lines = log_page.content.split('\n')[0:-1]
    lines = filter(lambda x: x is not None, map(lambda _: parse_line(_, 0), lines))

    for line in lines:
        line['datetime'] = datetime.datetime.fromtimestamp(line['timestamp'])

    return render_template('log.html',
        chat=chat,
        lines=lines,
        current_page=current_page,
        mode=mode,
        paginator=paginator,
    )


@app.route('/health', methods=['GET'])
def doHealthCheck():
    # should probably actually DO a health check here
    return 'ok'
    
# Redirects 

@app.route("/faq")
def faq():
    return render_template("pages/msparpfaq.html")

@app.route("/bbcode")
def bbcode():
    return render_template("pages/bbcode.html")

@app.route("/userguide")
def userguide():
    return render_template("pages/userguide.html")

# Home

@app.route("/")
def configure():
    return render_template("frontpage.html")

# Exporting

@app.route('/chat/<chat>/export')
def export_log(chat=None):
    if g.redis.exists('chat.' + chat + '.exported'):
        return render_template('export_complete.html', chat=chat)

    # Add to queue if chat log exists.
    if g.mysql.query(Log).filter(Log.url == chat).scalar():
        g.redis.sadd('export-queue', chat)

    return render_template('export_progress.html', chat=chat)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
