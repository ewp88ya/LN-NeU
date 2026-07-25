import os
import json
import time
import redis



class ErrorStore:


    def __init__(
        self,
        redis_url=None
    ):


        redis_url = (

            redis_url

            or os.getenv(
                "REDIS_URL",
                "redis://redis:6379"
            )

        )


        self.redis = redis.Redis.from_url(

            redis_url,

            decode_responses=True

        )


        self.key = (
            "ln-neu-errors"
        )



    def save(
        self,
        error
    ):


        payload = {

            "service": error.get(
                "service",
                "unknown"
            ),

            "type": error.get(
                "type",
                "Error"
            ),

            "message": error.get(
                "message",
                ""
            ),

            "timestamp": time.time()

        }


        self.redis.lpush(

            self.key,

            json.dumps(payload)

        )


        self.redis.ltrim(

            self.key,

            0,

            99

        )



    def latest(
        self,
        limit=10
    ):


        items = self.redis.lrange(

            self.key,

            0,

            limit - 1

        )


        return [

            json.loads(item)

            for item in items

        ]



    def count(self):

        return self.redis.llen(
            self.key
        )



    def clear(self):

        self.redis.delete(
            self.key
        )
