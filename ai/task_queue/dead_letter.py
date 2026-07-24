import os
import json
import redis


class DeadLetterQueue:

    def __init__(
        self,
        url=None
    ):

        if url is None:

            url = os.getenv(
                "REDIS_URL",
                "redis://localhost:6379"
            )

        self.redis = redis.Redis.from_url(
            url,
            decode_responses=True
        )

        self.queue_name = "ln-neu-dead-letter"
    def push(
        self,
        payload,
        reason
    ):

        self.redis.lpush(

            self.queue_name,

            json.dumps({

                "payload": payload,

                "reason": reason

            })

        )

    def pop(self):

        item = self.redis.rpop(
            self.queue_name
        )

        if item:
            return json.loads(item)

        return None

    def peek(self):

        item = self.redis.lindex(
            self.queue_name,
            -1
        )

        if item:
            return json.loads(item)

        return None

    def clear(self):

        self.redis.delete(
            self.queue_name
        )

    def size(self):

        return self.redis.llen(
            self.queue_name
        )
