from task_queue.queue_api import QueueAPI


class QueueManager:

    def __init__(self):
        self.queues = {}

        self.register_queue(
            "default",
            QueueAPI()
        )

    def register_queue(
        self,
        name,
        queue
    ):
        self.queues[name] = queue


    def get_queue(
        self,
        name="default"
    ):
        return self.queues.get(name)


    def push(
        self,
        payload,
        queue_name="default",
        priority="normal"
    ):
        queue = self.get_queue(queue_name)

        if not queue:
            raise ValueError(
                f"Queue '{queue_name}' not found"
            )

        return queue.push(
            payload,
            priority
        )


    def pop(
        self,
        queue_name="default"
    ):
        queue = self.get_queue(queue_name)

        if not queue:
            raise ValueError(
                f"Queue '{queue_name}' not found"
            )

        return queue.pop()


    def clear(
        self,
        queue_name="default"
    ):
        queue = self.get_queue(queue_name)

        if not queue:
            raise ValueError(
                f"Queue '{queue_name}' not found"
            )

        return queue.clear()


    def route_failed_task(
        self,
        payload,
        reason
    ):
        queue = self.get_queue(
            "default"
        )

        return queue.dlq_push(
            payload,
            reason
        )


    def stats(self):

        result = {}

        for name, queue in self.queues.items():
            result[name] = queue.stats()

        return result

    def exists(
        self,
        queue_name="default"
    ):

        return (
            queue_name
            in
            self.queues
        )
