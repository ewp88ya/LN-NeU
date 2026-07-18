import redis

from task_queue.instance import task_queue
from task_queue.dead_letter import DeadLetterQueue


class QueueHealth:


    def __init__(self):

        self.queue = task_queue
        self.dlq = DeadLetterQueue()


    def check(self):

        try:

            self.queue.redis.ping()

            redis_ok = True

        except redis.RedisError:

            redis_ok = False


        return {

            "status": "healthy" if redis_ok else "unhealthy",

            "redis": redis_ok,

            "queue_size": self.queue.size() if redis_ok else None,

            "dead_letter_size": self.dlq.size() if redis_ok else None

        }


    def print_health(self):

        result = self.check()

        print("=" * 50)
        print("LN-NeU Queue Health")
        print("=" * 50)

        for key, value in result.items():

            print(f"{key:<18}: {value}")

        print("=" * 50)
