#!/usr/bin/python
from redis import Redis
import uuid
import time

def check_compatibility(first, second):
    for option in ["para", "nsfw"]:
        first_option = first['options'].get(option)
        second_option = second['options'].get(option)
        if (
            first_option is not None
            and second_option is not None
            and first_option!=second_option
        ):
            return False
    return first['char'] in second['wanted_chars'] and second['char'] in first['wanted_chars']

if __name__=='__main__': 

    redis = Redis(unix_socket_path='/tmp/redis.sock')

    while True:
        searchers = redis.zrange('searchers', 0, -1)
        
        if len(searchers)>=2: # if there aren't at least 2 people, there can't be matches

            all_chars = redis.smembers('all-chars')
            sessions = [{
                'id': session_id,
                'char': redis.hget('session.'+session_id, 'character'),
                'wanted_chars': redis.smembers('session.'+session_id+'.picky') or all_chars,
                'options': redis.hgetall('session.'+session_id+'.picky-options'),
            } for session_id in searchers]

            already_matched = set()
            for n in range(len(sessions)):
                for m in range(n+1, len(sessions)):
                    if (
                        sessions[n]['id'] not in already_matched
                        and sessions[m]['id'] not in already_matched
                        and check_compatibility(sessions[n], sessions[m])
                    ):
                        chat = str(uuid.uuid4()).replace('-','')
                        redis.hset('chat.'+chat+'.meta', 'type', 'unsaved')
                        redis.set('session.'+sessions[n]['id']+'.match', chat)
                        redis.set('session.'+sessions[m]['id']+'.match', chat)
                        redis.zrem('searchers', sessions[n]['id'])
                        redis.zrem('searchers', sessions[m]['id'])
                        already_matched.add(sessions[n]['id'])
                        already_matched.add(sessions[m]['id'])

        time.sleep(1)

