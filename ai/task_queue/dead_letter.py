import json
import time

import redis


class DeadLetterQueue:


    def __init__(
        self,
        redis_url="redis://localhost:6379",
        queue_name="lnneu:dead-letter"
    ):

        self.redis = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

        self.queue_name = queue_name



    def push(
        self,
        payload,
        reason="unknown"
    ):

        record = {

            "payload": payload,

            "reason": reason,

            "failed_at": time.time()

        }

        self.redis.rpush(
            self.queue_name,
            json.dumps(record)
        )



    def pop(self):

        item = self.redis.lpop(
            self.queue_name
        )

        if item is None:

            return None

        return json.loads(item)



    def size(self):

        return self.redis.llen(
            self.queue_name
        )



    def clear(self):

        self.redis.delete(
            self.queue_name
        )
