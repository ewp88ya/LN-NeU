import asyncio

from workflows.engine import WorkflowEngine
from task_queue.instance import task_queue
from task_queue.concurrent_worker import ConcurrentWorker


class ScalingManager:


    def __init__(
        self,
        worker_count=3
    ):

        self.worker_count = worker_count

        self.worker = ConcurrentWorker(
            queue=task_queue,
            workflow=WorkflowEngine(),
            workers=worker_count
        )


    async def start(self):

        print("=" * 50)
        print("LN-NeU Scaling Manager")
        print(f"Workers : {self.worker_count}")
        print("=" * 50)

        await self.worker.start()


    def stop(self):

        self.worker.stop()
