import re, time

SEARCH_PERIOD = 1
PING_PERIOD = 10
DELETE_MATCH_PERIOD = 1800
DELETE_GROUP_PERIOD = 2592000
ARCHIVE_PERIOD = 1800
DELETE_SESSION_PERIOD = 2592000

def get_time(offset=0):
    return int(time.time())+offset

def validate_chat_url(url):
    return re.match('^[-a-zA-Z0-9]+$', url)
