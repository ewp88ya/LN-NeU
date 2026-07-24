from task_queue.task_queue import TaskQueue
from task_queue.dead_letter import DeadLetterQueue


class QueueAPI:
    def __init__(self):
        self.queue = TaskQueue()
        self.dlq = DeadLetterQueue()

    def push(self, payload, priority="normal"):
        return self.queue.push(
            {
                "payload": payload,
                "priority": priority
            }
        )

    def pop(self):
        return self.queue.pop()

    def peek(self):
        return self.queue.peek()

    def clear(self):
        return self.queue.clear()

    def size(self):
        return self.queue.size()

    # DLQ

    def dlq_push(self, payload, reason):
        return self.dlq.push(
            payload,
            reason
        )

    def dlq_pop(self):
        return self.dlq.pop()

    def dlq_peek(self):
        return self.dlq.peek()

    def dlq_clear(self):
        return self.dlq.clear()

    def stats(self):
        return {
            "queue_size": self.queue.size(),
            "dlq_size": self.dlq.size()
        }
