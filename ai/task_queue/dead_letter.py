import json
import redis


class DeadLetterQueue:


    def __init__(
        self,
        url="redis://redis:6379"
    ):

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

        data = {

            "payload": payload,

            "reason": reason

        }


        self.redis.rpush(

            self.queue_name,

            json.dumps(data)

        )



    def size(self):

        return self.redis.llen(
            self.queue_name
        )
