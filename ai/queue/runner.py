import asyncio

from queue import TaskQueue, AsyncWorker
from workflows.engine import WorkflowEngine


async def run():

    queue = TaskQueue()
    workflow = WorkflowEngine()

    worker = AsyncWorker(
        queue,
        workflow
    )

    await worker.start()


if __name__ == "__main__":
    asyncio.run(run())
