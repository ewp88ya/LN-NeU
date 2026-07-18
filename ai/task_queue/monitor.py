import time

from task_queue.instance import task_queue
from task_queue.dead_letter import DeadLetterQueue


class QueueMonitor:


    def __init__(self):

        self.queue = task_queue
        self.dlq = DeadLetterQueue()


    def snapshot(self):

        return {

            "queue_size": self.queue.size(),

            "dead_letter_size": self.dlq.size(),

            "timestamp": time.time()

        }


    def print_status(self):

        status = self.snapshot()

        print("=" * 50)
        print("LN-NeU Queue Monitor")
        print("=" * 50)
        print(f"Queue        : {status['queue_size']}")
        print(f"Dead Letter  : {status['dead_letter_size']}")
        print(f"Timestamp    : {status['timestamp']}")
        print("=" * 50)
