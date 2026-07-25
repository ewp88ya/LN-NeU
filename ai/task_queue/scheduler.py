import json
import time
import os
import redis


class Scheduler:


    def __init__(
        self,
        url=None,
        redis_url=None
    ):


        url = (

            redis_url

            or url

            or os.getenv(
                "REDIS_URL",
                "redis://redis:6379"
            )

        )


        self.redis = redis.Redis.from_url(

            url,

            decode_responses=True

        )


        self.queue_name = (
            "ln-neu-scheduler"
        )



    def schedule(
        self,
        payload,
        execute_at
    ):


        task = {

            "payload": payload,

            "execute_at": execute_at

        }


        self.redis.zadd(

            self.queue_name,

            {
                json.dumps(task):
                execute_at
            }

        )



    def get_ready_tasks(self):

        now = time.time()


        items = self.redis.zrangebyscore(

            self.queue_name,

            0,

            now

        )


        tasks = []


        for item in items:


            self.redis.zrem(

                self.queue_name,

                item

            )


            tasks.append(

                json.loads(item)

            )


        return tasks



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
