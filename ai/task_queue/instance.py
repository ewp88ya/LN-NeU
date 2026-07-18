from task_queue.task_queue import TaskQueue
import os


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)


task_queue = TaskQueue(
    redis_url=REDIS_URL
)
