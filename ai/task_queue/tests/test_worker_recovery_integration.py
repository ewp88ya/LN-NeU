import asyncio
import pytest

from task_queue.concurrent_worker import ConcurrentWorker
from task_queue.auto_recovery import AutoRecoveryManager


class DummyQueue:

    def pop(self):
        return None



class DummyWorkflow:

    async def execute(self, task):
        return {
            "status": "success"
        }



@pytest.mark.asyncio
async def test_worker_crash_recovery():

    worker = ConcurrentWorker(
        queue=DummyQueue(),
        workflow=DummyWorkflow(),
        workers=1
    )


    worker.running = True


    #
    # simulate worker crash
    #
    async def crashed_worker(worker_id):

        raise RuntimeError(
            "simulated worker crash"
        )


    worker.process_worker = crashed_worker


    task = asyncio.create_task(
        worker.process_worker(1)
    )


    worker.worker_tasks[1] = task


    await asyncio.sleep(
        0.1
    )

    assert task.done()

    with pytest.raises(RuntimeError):
        task.result()


    assert task.done()


    worker.worker_state[1] = {
        "status": "dead"
    }


    recovery_result = await worker.recovery.recover_worker(
        1,
        reason="worker_crash"
    )


    assert recovery_result is True


    assert (
        worker.recovery.recovery_counter[1]
        ==
        1
    )


    assert (
        worker.recovery.recovery_status[1]["status"]
        ==
        "running"
    )
