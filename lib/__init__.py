import re, time

# Timeout period for searchers.
SEARCH_PERIOD = 1

# Timeout period for chats.
PING_PERIOD = 10

# Period in which saved chats are archived.
ARCHIVE_PERIOD = 30 * 60

# Time after which unsaved chats are deleted - 7 days.
DELETE_UNSAVED_PERIOD = 604800

# Time after which saved chars are deleted - 30 days.
DELETE_SAVED_PERIOD = 2592000

# Time after which chat session data is deleted - 30 days.
DELETE_CHAT_SESSION_PERIOD = 2592000

# Time after which global session data is deleted - 30 days.
DELETE_SESSION_PERIOD = 2592000

def get_time(offset=0):
    return int(time.time())+offset

def validate_chat_url(url):
    if len(url)<=100:
        return re.match('^[-a-zA-Z0-9]+$', url)
    return False
