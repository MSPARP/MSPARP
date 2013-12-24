main: gunicorn -b 0.0.0.0:8000 -w 3 main:app
chat: gunicorn -b 0.0.0.0:8000 -w 3 chat:app
archiver: python archiver.py
matchmaker: python matchmaker.py
reaper: python reaper.py
hello: python hello.py