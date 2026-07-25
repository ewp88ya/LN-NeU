import time

from observability.health_monitor import HealthMonitor
from observability.queue_monitor import QueueMonitor
from observability.error_tracker import ErrorTracker


class Dashboard:

    def __init__(self):

        self.started_at = time.time()

        self.health = HealthMonitor()

        self.queue = QueueMonitor()

        self.errors = ErrorTracker()


    def snapshot(self):

        return {

            "status": "ok",

            "uptime": round(
                time.time() - self.started_at,
                2
            ),

            "health": self.health.check_all(),

            "metrics": self.queue.snapshot(),

            "errors": {

                "total": self.errors.total(),

                "recent": self.errors.recent()

            }

        }
