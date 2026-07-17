import asyncio

from task_queue import task_queue, AsyncWorker

from workflows.engine import WorkflowEngine


async def run():

    print(
    "LN-NeU AI Worker started",
    flush=True
    )

    workflow = WorkflowEngine()


    worker = AsyncWorker(
        task_queue,
        workflow
    )

    print(
    "Worker listening...",
    flush=True
    )


    await worker.start()



if __name__ == "__main__":

    asyncio.run(run())
