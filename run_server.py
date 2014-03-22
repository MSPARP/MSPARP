import os
import sys
from gevent.socket import getfqdn, socket, AF_UNIX
from gevent.wsgi import WSGIServer
from gevent import monkey; monkey.patch_socket()

try:
    if sys.argv[1].startswith('main'):
        from main import app
    elif sys.argv[1].startswith('chat'):
        from chat import app
except ImportError:
    sys.exit("Usage: python run_server.py (main|chat) [--debug]")

if '--debug' in sys.argv:
    app.debug = True

socket_path = '/tmp/'+sys.argv[1]+'.sock'

# Delete the socket file if it already exists.
try:
    os.remove(socket_path)
except OSError:
    pass

sock = socket(AF_UNIX)
sock.bind(socket_path)
sock.setblocking(0)
sock.listen(256)

os.chmod(socket_path, 0777)

http_server = WSGIServer(sock, app)
# yeah this is a hack.
http_server.environ['SERVER_NAME'] = getfqdn()
http_server.serve_forever()

