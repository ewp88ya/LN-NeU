import asyncio

from workflows.engine import WorkflowEngine
from task_queue.instance import task_queue
from task_queue.concurrent_worker import ConcurrentWorker
from observability.logger import (
    get_logger,
    log_event,
)


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

        self.logger = get_logger(
            "scaling_manager"
        )

    async def start(self):

        log_event(
            self.logger,
            "info",
            "Scaling manager started",
            event="scaling_start",
            service="queue_scaling",
            metadata={
                "workers": self.worker_count
            }
        )

        await self.worker.start()
