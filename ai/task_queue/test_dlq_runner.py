import asyncio

from task_queue.instance import task_queue
from task_queue.dead_letter import DeadLetterQueue
from task_queue.concurrent_worker import ConcurrentWorker

from task_queue.test_failed_workflow import FailedWorkflow


async def main():

    task_queue.clear()

    dlq = DeadLetterQueue()
    dlq.clear()

    worker = ConcurrentWorker(
        queue=task_queue,
        workflow=FailedWorkflow(),
        workers=1
    )

    #
    # Supaya cepat, maksimal 2 retry
    #
    worker.retry.max_retry = 2

    task_queue.push(
        {
            "taskId": "dlq-demo-001",
            "action": "analyze",
            "input": "force failure"
        }
    )

    runner = asyncio.create_task(
        worker.start()
    )

    await asyncio.sleep(5)

    worker.stop()

    runner.cancel()

    print()

    print("Queue :", task_queue.size())
    print("DLQ   :", dlq.size())

    print()

    print(dlq.pop())


if __name__ == "__main__":

    asyncio.run(
        main()
    )
