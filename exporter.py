#!/usr/bin/python

from redis import Redis
import time
import datetime
import os

from lib.model import sm
from lib.export import export_chat

if __name__ == '__main__':

    if not os.path.exists("logs"):
        os.makedirs("logs")

    redis = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))
    sql = sm()

    current_time = datetime.datetime.now()

    while True:
        if datetime.datetime.now().minute != current_time.minute:
            # Export chats.
            for chat in redis.smembers('export-queue'):
                export_chat(redis, sql, chat)
                redis.srem('export-queue', chat)
                redis.set('chat.' + chat + '.exported', 1)
                redis.expire('chat.' + chat + '.exported', 86400)  # 86400 seconds = 1 day

        current_time = datetime.datetime.now()

        time.sleep(1)
