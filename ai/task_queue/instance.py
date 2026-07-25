from task_queue.task_queue import TaskQueue
from config.settings import settings


task_queue = TaskQueue(
    redis_url=settings.REDIS_URL
)
