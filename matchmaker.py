#!/usr/bin/python
from redis import Redis
import uuid
import time
import os

OPTION_LABELS = {
    'para0': 'script style',
    'para1': 'paragraph style',
    'nsfw0': 'safe for work',
    'nsfw1': 'not safe for work',
}

def check_compatibility(first, second):
    selected_options = []
    for option in ["para", "nsfw"]:
        first_option = first['options'].get(option)
        second_option = second['options'].get(option)
        if (
            first_option is not None
            and second_option is not None
            and first_option!=second_option
        ):
            return False, selected_options
        if first_option is not None:
            selected_options.append(option+first_option)
        elif second_option is not None:
            selected_options.append(option+second_option)
    compatible = first['char'] in second['wanted_chars'] and second['char'] in first['wanted_chars']
    if first['lastmatched'] == None or second['lastmatched'] == None:
        pass
    elif first['lastmatched'] == second['id'] and second['lastmatched'] == first['id']:
        return False, selected_options
    return compatible, selected_options

if __name__=='__main__': 

    redis = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))

    while True:
        searchers = redis.zrange('searchers', 0, -1)
        
        if len(searchers)>=2: # if there aren't at least 2 people, there can't be matches

            all_chars = redis.smembers('all-chars')
            sessions = [{
                'id': session_id,
                'char': redis.hget('session.'+session_id, 'character'),
                'wanted_chars': redis.smembers('session.'+session_id+'.picky') or all_chars,
                'options': redis.hgetall('session.'+session_id+'.picky-options'),
                'lastmatched': redis.get('session.'+session_id+'.matched'),
            } for session_id in searchers]

            already_matched = set()
            for n in range(len(sessions)):
                for m in range(n+1, len(sessions)):
                    print sessions[n]['id'], sessions[m]['id']
                    if (
                        sessions[n]['id'] not in already_matched
                        and sessions[m]['id'] not in already_matched
                    ):
                        compatible, selected_options = check_compatibility(sessions[n], sessions[m])
                        print compatible, selected_options
                        if not compatible:
                            continue
                        chat = str(uuid.uuid4()).replace('-','')
                        redis.hset('chat.'+chat+'.meta', 'type', 'unsaved')
                        if len(selected_options)>0:
                            option_text = ', '.join(OPTION_LABELS[_] for _ in selected_options)
                            redis.rpush(
                                'chat.'+chat,
                                str(int(time.time()))+',-1,message,000000,This is a '+option_text+' chat.'
                            )
                        redis.set('session.'+sessions[n]['id']+'.match', chat)
                        redis.set('session.'+sessions[m]['id']+'.match', chat)
                        redis.zrem('searchers', sessions[n]['id'])
                        redis.zrem('searchers', sessions[m]['id'])
                        already_matched.add(sessions[n]['id'])
                        already_matched.add(sessions[m]['id'])
                        redis.setex('session.'+sessions[n]['id']+'.matched', sessions[m]['id'], 60)
                        redis.setex('session.'+sessions[m]['id']+'.matched', sessions[n]['id'], 60)

        time.sleep(1)

