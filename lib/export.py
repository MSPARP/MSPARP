import codecs
import os
import datetime
import shutil
import zipfile
from jinja2 import Environment, FileSystemLoader
from webhelpers import paginate
from messages import parse_line
from model import Log

env = Environment(loader=FileSystemLoader('templates'))
log_template = env.get_template('archivelog.html')

class PageURL(object):
    """A simple page URL generator for any framework."""

    def __init__(self, path):
        """
        ``path`` is the current URL path, with or without a "scheme://host"
         prefix.

        ``params`` is the current URL's query parameters as a dict or dict-like
        object.
        """
        self.path = path

    def __call__(self, page, partial=False):
        return str(page) + ".html"

def zipdir(path, ziph, logname):
    for root, dirs, files in os.walk(path):
        for f in files:
            ziph.write(os.path.join(root, f), logname + '/' + f)

def export_chat(redis, sql, url):
    log = sql.query(Log).filter(Log.url == url).scalar()

    if not log:
        return

    # Create temp directory.
    if not os.path.exists('tmp/' + log.url):
        os.makedirs('tmp/' + log.url)

    # Create export pages.
    for page in log.pages:
        with codecs.open('tmp/' + log.url + '/' + str(page.number) + '.html', 'w', 'utf8') as f:
            paginator = paginate.Page([], page=page.number, items_per_page=1, item_count=log.page_count, url=PageURL(log.url))

            lines = page.content.split('\n')[0:-1]
            lines = filter(lambda x: x is not None, map(lambda _: parse_line(_, 0), lines))

            for line in lines:
                line['datetime'] = datetime.datetime.fromtimestamp(line['timestamp']/1000.0)

            f.write(log_template.render(
                lines=lines,
                paginator=paginator
            ))

    # Copy static assets
    shutil.copyfile('static/js/bbcode.js', 'tmp/' + log.url + '/bbcode.js')
    shutil.copyfile('static/js/jquery.min.js', 'tmp/' + log.url + '/jquery.min.js')
    shutil.copyfile('static/css/msparp.css', 'tmp/' + log.url + '/msparp.css')
    shutil.copyfile('static/css/chat.css', 'tmp/' + log.url + '/chat.css')

    # Create export zip.
    with zipfile.ZipFile('logs/' + log.url + ".zip", 'w', zipfile.ZIP_DEFLATED) as logzip:
        zipdir('tmp/'+log.url, logzip, log.url)

    # Cleanup the temporary files.
    shutil.rmtree('tmp/' + log.url, ignore_errors=True)
