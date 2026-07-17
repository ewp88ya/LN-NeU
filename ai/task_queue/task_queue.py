import json
import redis

from models.task import AITask


class TaskQueue:

    def __init__(self):

        self.redis = redis.Redis(
            host="ln-neu-redis",
            port=6379,
            decode_responses=True
        )

        self.key = "lnneu:tasks"


    def push(self, task):

        data = task.model_dump()

        self.redis.rpush(
            self.key,
            json.dumps(data)
        )


    def pop(self):

        result = self.redis.lpop(
            self.key
        )


        if not result:
            return None


        data = json.loads(result)


        return AITask(
            **data
        )


    def size(self):

        return self.redis.llen(
            self.key
        )
