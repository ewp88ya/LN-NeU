import json
import redis


class TaskQueue:

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

        self.queue_name = "ln-neu-task-queue"

    def push(
        self,
        task
    ):

        if (
            isinstance(task, dict)
            and "task" in task
            and "retry_count" in task
        ):
            payload = task

        else:

            if hasattr(task, "model_dump"):
                task_payload = task.model_dump()

            elif isinstance(task, dict):
                task_payload = task

            else:
                task_payload = task.__dict__

            payload = {
                "task": task_payload,
                "retry_count": 0
            }

        self.redis.lpush(
            self.queue_name,
            json.dumps(payload)
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

    def empty(self):

        return self.size() == 0
