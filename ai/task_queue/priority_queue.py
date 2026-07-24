import json
import time
import redis


class PriorityQueue:

    PRIORITY_MAP = {
        "high": 1,
        "normal": 5,
        "low": 10
    }


    def __init__(
        self,
        url=None,
        redis_url=None
    ):

        if redis_url:
            url = redis_url

        if url is None:
            import os

            url = os.getenv(
                "REDIS_URL",
                "redis://localhost:6379"
            )


        self.redis = redis.Redis.from_url(
            url,
            decode_responses=True
        )

        self.queue_name = (
            "ln-neu-priority-queue"
        )


    def push(
        self,
        payload,
        priority="normal"
    ):

        score = (
            self.PRIORITY_MAP
            .get(priority, 5)
        )

        task = {
            "payload": payload,
            "priority": priority,
            "created_at": time.time()
        }

        self.redis.zadd(
            self.queue_name,
            {
                json.dumps(task): score
            }
        )


    def pop(self):

        items = self.redis.zrange(
            self.queue_name,
            0,
            0
        )

        if not items:
            return None


        item = items[0]

        self.redis.zrem(
            self.queue_name,
            item
        )

        return json.loads(item)


    def peek(self):

        items = self.redis.zrange(
            self.queue_name,
            0,
            0
        )

        if not items:
            return None

        return json.loads(
            items[0]
        )


    def clear(self):

        self.redis.delete(
            self.queue_name
        )


    def size(self):

        return self.redis.zcard(
            self.queue_name
        )
