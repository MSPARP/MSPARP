main: gunicorn -b 0.0.0.0:8000 -k gevent -w 3 main:app
main-debug: gunicorn --debug --log-level=debug -b 0.0.0.0:8000 -k gevent -w 1 main:app
archiver: python archiver.py
initdb: python initdb.py
exporter: python exporter.py
