import os

from task_queue.metrics import QueueMetrics



class QueueMonitor:


    def __init__(self):


        self.queue_metrics = QueueMetrics(

            redis_url=os.getenv(

                "REDIS_URL",

                "redis://redis:6379"

            )

        )



    def snapshot(self):

        return self.queue_metrics.stats()
