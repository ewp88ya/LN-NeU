import json
import time
import redis


class TaskQueue:


    def __init__(
        self,
        redis_url="redis://ln-neu-redis:6379",
        queue_name="lnneu:tasks"
    ):

        self.redis = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

        self.queue_name = queue_name



    def push(
        self,
        task
    ):

        payload = {

            "task": task,

            "created_at": time.time(),

            "attempts": 0

        }


        self.redis.rpush(
            self.queue_name,
            json.dumps(payload)
        )


        return True



    def pop(
        self
    ):

        item = self.redis.lpop(
            self.queue_name
        )


        if not item:

            return None


        payload = json.loads(
            item
        )


        return payload["task"]



    def size(self):

        return self.redis.llen(
            self.queue_name
        )



    def clear(self):

        self.redis.delete(
            self.queue_name
        )
