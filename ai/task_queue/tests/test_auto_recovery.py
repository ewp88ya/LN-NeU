import pytest

from task_queue.auto_recovery import AutoRecoveryManager


class DummyWorker:

    def __init__(self):

        self.worker_state = {
            1: {
                "status": "dead"
            }
        }


    async def process_worker(self, worker_id):

        self.worker_state[worker_id] = {
            "status": "idle"
        }



@pytest.mark.asyncio
async def test_worker_recovery():

    worker = DummyWorker()


    recovery = AutoRecoveryManager(
        worker,
        max_restart=3
    )


    result = await recovery.recover_worker(
        1
    )


    assert result is True

    assert recovery.recovery_counter[1] == 1



@pytest.mark.asyncio
async def test_max_restart():

    worker = DummyWorker()


    recovery = AutoRecoveryManager(
        worker,
        max_restart=2
    )


    await recovery.recover_worker(1)
    await recovery.recover_worker(1)


    result = await recovery.recover_worker(1)


    assert result is False

    assert (
        recovery.recovery_status[1]["reason"]
        ==
        "max_restart_exceeded"
    )
