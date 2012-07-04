import re, time

START_TIME = 1302231346
PING_PERIOD = 10
SEARCH_PERIOD = 1

def get_time():
    return time.time() - START_TIME

def validate_chat_url(url):
    return re.match('^[-a-zA-Z0-9]+$', url)
