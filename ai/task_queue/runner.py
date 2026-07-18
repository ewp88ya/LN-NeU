import asyncio

from task_queue.instance import task_queue

from task_queue.concurrent_worker import (
    ConcurrentWorker
)

from workflows.engine import WorkflowEngine



async def main():

    workflow = WorkflowEngine()


    worker = ConcurrentWorker(
        queue=task_queue,
        workflow=workflow,
        workers=3
    )


    await worker.start()



if __name__ == "__main__":

    asyncio.run(
        main()
    )
