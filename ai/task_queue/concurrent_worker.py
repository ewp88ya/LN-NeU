import asyncio

from task_queue.adapter import TaskAdapter
from task_queue.retry import RetryPolicy
from task_queue.dead_letter import DeadLetterQueue
from agents.executor import AgentExecutor
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

        self.agent = AgentExecutor()

        self.memory = MemoryManager()

        self.running = False



    async def process_worker(
        self,
        worker_id
    ):

        print(
            f"Worker-{worker_id} started"
        )

        while self.running:

            payload = None

            try:

                payload = self.queue.pop()

                if payload is None:

                    await asyncio.sleep(
                        0.2
                    )

                    continue


                print(
                    f"Worker-{worker_id} processing {payload['task']['taskId']}"
                )


                task = self.adapter.convert(
                    payload["task"]
                )


                result = await self.workflow.execute(
                    task
                )


                print(
                    f"Worker-{worker_id} completed:"
                )

                print(
                    result
                )


                #
                # Workflow gagal
                #
                if (
                    isinstance(result, dict)
                    and result.get("status") == "failed"
                ):

                    if self.retry.should_retry(
                        payload
                    ):

                        payload = self.retry.increase_retry(
                            payload
                        )

                        print(
                            f"Worker-{worker_id} retry #{payload['retry_count']} -> {payload['task']['taskId']}"
                        )

                        self.queue.push(
                            payload
                        )

                    else:

                        self.dead_letter.push(
                            payload,
                            reason="retry_limit"
                        )

                        print(
                            f"Worker-{worker_id} moved to DLQ -> {payload['task']['taskId']}"
                        )


            except Exception as error:

                print(
                    f"Worker-{worker_id} failed:"
                )

                print(
                    error
                )


                if payload is not None:

                    if self.retry.should_retry(
                        payload
                    ):

                        payload = self.retry.increase_retry(
                            payload
                        )

                        print(
                            f"Worker-{worker_id} exception retry #{payload['retry_count']} -> {payload['task']['taskId']}"
                        )

                        self.queue.push(
                            payload
                        )

                    else:

                        self.dead_letter.push(
                            payload,
                            reason=str(error)
                        )

                        print(
                            f"Worker-{worker_id} exception moved to DLQ -> {payload['task']['taskId']}"
                        )

                        print(
                            payload
                        )



    async def start(self):

        self.running = True

        workers = []


        for index in range(
            self.workers
        ):

            workers.append(

                asyncio.create_task(

                    self.process_worker(
                        index + 1
                    )

                )

            )


        await asyncio.gather(
            *workers
        )



    def stop(self):

        self.running = False
