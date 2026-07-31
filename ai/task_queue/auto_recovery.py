import asyncio
import time

from task_queue.metrics import QueueMetrics

class AutoRecoveryManager:

    def __init__(
        self,
        worker_pool,
        max_restart=3
    ):

        self.worker_pool = worker_pool
        self.max_restart = max_restart

        self.recovery_counter = {}

        self.recovery_status = {}

        self.metrics = QueueMetrics()


    async def recover_worker(
        self,
        worker_id,
        reason="worker_dead"
    ):

        count = self.recovery_counter.get(
            worker_id,
            0
        )


        if count >= self.max_restart:

            self.recovery_status[worker_id] = {
                "status": "dead",
                "restart_count": count,
                "reason": "max_restart_exceeded",
                "timestamp": time.time()
            }

            return False



        self.recovery_counter[worker_id] = count + 1

        self.metrics.record_recovery()

        self.worker_pool.worker_state[worker_id] = {
            "status": "recovering",
            "last_seen": time.time()
        }


        self.recovery_status[worker_id] = {
            "status": "recovering",
            "restart_count": self.recovery_counter[worker_id],
            "reason": reason,
            "timestamp": time.time()
        }


        try:

            task = asyncio.create_task(
                self.worker_pool.process_worker(
                    worker_id
                )
            )


            self.recovery_status[worker_id]["status"] = "running"

            return True


        except Exception as error:

            self.worker_pool.worker_state[worker_id]["status"] = "dead"

            self.recovery_status[worker_id] = {
                "status": "dead",
                "restart_count": self.recovery_counter[worker_id],
                "reason": str(error),
                "timestamp": time.time()
            }

            return False


    def get_status(
        self,
        worker_id
    ):
        return self.recovery_status.get(
            worker_id
        )

