import asyncio
import time

from task_queue.adapter import TaskAdapter
from task_queue.retry import RetryPolicy
from task_queue.dead_letter import DeadLetterQueue
from task_queue.auto_recovery import AutoRecoveryManager
from task_queue.metrics import QueueMetrics
from memory.manager import MemoryManager


class ConcurrentWorker:

    def __init__(
        self,
        queue,
        workflow,
        workers=3
    ):
        self.queue = queue
        self.workflow = workflow
        self.workers = workers

        self.adapter = TaskAdapter()
        self.retry = RetryPolicy()
        self.dead_letter = DeadLetterQueue()

        self.memory = MemoryManager()
        self.metrics = QueueMetrics()

        self.running = False

        self.worker_state = {}
        self.worker_tasks = {}
        self.monitor_task = None

        self.recovery = AutoRecoveryManager(
            self,
            max_restart=3
        )

    async def process_worker(
        self,
        worker_id
    ):

        print(f"WORKER {worker_id} STARTED", flush=True)

        self.worker_state[worker_id] = {
            "status": "idle",
            "last_seen": time.time()
        }

        while self.running:

            self.worker_state[worker_id]["last_seen"] = time.time()

            payload = self.queue.pop()

            if payload is None:

                self.worker_state[worker_id]["status"] = "idle"

                await asyncio.sleep(0.05)

                continue

            try:

                self.worker_state[worker_id]["status"] = "busy"

                print("POP", payload["task"]["taskId"])

                print("PAYLOAD", payload)

                task = self.adapter.convert(
                    payload["task"]
                )

                print("CONVERT OK")

                result = await self.workflow.execute(
                    task
                )

                print(
                    "WORKFLOW RESULT:",
                    result,
                    flush=True
                )

                print("EXECUTE OK")

                self.metrics.record_processed()

                if (
                    isinstance(result, dict)
                    and result.get("status") == "failed"
                ):

                    self.metrics.record_failed()

                    if self.retry.should_retry(payload):

                        payload = self.retry.increase_retry(
                            payload
                        )

                        self.queue.push(payload)

                    else:

                        self.dead_letter.push(
                            payload,
                            reason="retry_limit"
                        )

                        self.metrics.record_dead_letter()

            except Exception as error:

                self.metrics.record_failed()

                if payload:

                    if self.retry.should_retry(payload):

                        payload = self.retry.increase_retry(
                            payload
                        )

                        self.queue.push(payload)

                    else:

                        self.dead_letter.push(
                            payload,
                            reason=str(error)
                        )

                        self.metrics.record_dead_letter()

            finally:

                self.worker_state[worker_id]["status"] = "idle"

        print(f"Worker-{worker_id} exit")

    async def monitor_workers(
        self
    ):
        while self.running:

            self.metrics.record_queue_depth(
                self.queue.size()
            )

            await asyncio.sleep(1)

    async def start(
        self
    ):
        self.running = True

        self.monitor_task = asyncio.create_task(
            self.monitor_workers()
        )

        for index in range(self.workers):

            worker_id = index + 1

            task = asyncio.create_task(
                self.process_worker(worker_id)
            )

            self.worker_tasks[worker_id] = task

        while self.running:

            await asyncio.sleep(1)

        await asyncio.gather(
            *self.worker_tasks.values(),
            return_exceptions=True
        )

        if self.monitor_task:
            await asyncio.gather(
                self.monitor_task,
                return_exceptions=True
            )

    def stop(
        self
    ):
        self.running = False

        for task in self.worker_tasks.values():
            if not task.done():
                task.cancel()

        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()

    def worker_health(
        self
    ):
        return self.worker_state
