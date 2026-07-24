import asyncio

from agents.executor import AgentExecutor
from memory.manager import MemoryManager


class AsyncWorker:

    def __init__(
        self,
        queue,
        workflow
    ):

        self.queue = queue
        self.workflow = workflow

        self.agent = AgentExecutor()
        self.memory = MemoryManager()

        self.running = False


    async def start(self):

        self.running = True

        print(
            "Worker listening...",
            flush=True
        )


        while self.running:

            try:

                task = self.queue.pop()


                if task is None:

                    await asyncio.sleep(0.1)
                    continue


                print(
                    f"Processing task: {task.task_id}",
                    flush=True
                )


                # Memory Context Injection
                memory_context = {}

                try:
                    memory_context = self.memory.retrieve(
                        "short_term",
                        task.task_id
                    )
                except Exception:
                    memory_context = {}

                task.memory = memory_context

                # Agent Execution
                result = await self.agent.execute(
                    task
                )


                print(
                    "Task completed:",
                    result,
                    flush=True
                )


            except Exception as e:

                print(
                    "Worker error:",
                    repr(e),
                    flush=True
                )


                await asyncio.sleep(1)



    def stop(self):

        self.running = False
