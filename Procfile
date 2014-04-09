main: gunicorn -b 0.0.0.0:8000 -k gevent -w 3 main:app
chat: gunicorn -b 0.0.0.0:8000 -k gevent -w 3 chat:app
main-debug: gunicorn --debug --log-level=debug -b 0.0.0.0:8000 -k gevent -w 1 main:app
chat-debug: gunicorn --debug --log-level=debug -b 0.0.0.0:8000 -k gevent -w 1 chat:app
archiver: python archiver.py
matchmaker: python matchmaker.py
reaper: python reaper.py
initdb: python initdb.py