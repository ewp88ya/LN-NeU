import asyncio
import time

import pytest

from task_queue.concurrent_worker import ConcurrentWorker


class StressQueue:

    def __init__(self):

        self.items = []


    def push(self, payload):

        self.items.append(payload)


    def pop(self):

        if not self.items:
            return None

        return self.items.pop(0)


    def size(self):

        return len(self.items)



class StressWorkflow:


    async def execute(
        self,
        task
    ):

        await asyncio.sleep(
            0.001
        )

        return {
            "status": "success",
            "task": task
        }



@pytest.mark.asyncio
async def test_queue_stress():

    queue = StressQueue()


    total_tasks = 1000


    for index in range(
        total_tasks
    ):

        queue.push(
            {
                "task": {
                    "taskId": f"stress-{index}",
                    "type": "stress",
                    "payload": {
                        "index": index
                    }
                }
            }
        )


    worker = ConcurrentWorker(
        queue=queue,
        workflow=StressWorkflow(),
        workers=10
    )


    start = time.time()


    runner = asyncio.create_task(
        worker.start()
    )


    timeout = 15


    while queue.size() > 0:

        await asyncio.sleep(
            0.1
        )


    worker.stop()

    for task in worker.worker_tasks.values():

        if not task.done():

            task.cancel()

    try:

        await asyncio.wait_for(
            runner,
            timeout=timeout
        )

    except asyncio.CancelledError:

        pass

        pytest.fail(
            "worker did not shutdown"
        )


    elapsed = time.time() - start


    print(
        f"Processed {total_tasks} tasks in {elapsed:.2f}s"
    )


    assert queue.size() == 0
