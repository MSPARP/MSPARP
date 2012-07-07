import sys
from gevent.wsgi import WSGIServer
from gevent import monkey; monkey.patch_socket()

try:
    if sys.argv[1]=='main':
        from main import app
        port = 8000
    elif sys.argv[1]=='chat':
        from chat import app
        port = 9000
except:
    sys.exit("Usage: python run_server.py (main|chat) (port) [--debug]")

try:
    # If we can get a port from the arguments, override the default.
    port = int(sys.argv[2])
except:
    pass

if '--debug' in sys.argv:
    app.debug = True

http_server = WSGIServer(('', port), app)
http_server.serve_forever()

