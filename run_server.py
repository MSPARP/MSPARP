import sys
from gevent.wsgi import WSGIServer
from gevent import monkey; monkey.patch_socket()
from msparp import app

if '--debug' in sys.argv:
    app.debug = True

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()

