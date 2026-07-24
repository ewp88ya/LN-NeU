from task_queue.queue_manager import QueueManager
from task_queue.scheduler import Scheduler
from task_queue.metrics import QueueMetrics


class WorkflowQueueAdapter:

    def __init__(self):

        self.queue_manager = QueueManager()

        self.scheduler = Scheduler()

        self.metrics = QueueMetrics()


    def submit_workflow(
        self,
        workflow,
        priority="normal"
    ):

        self.metrics.record_enqueue()

        return self.queue_manager.push(
            workflow,
            priority=priority
        )


    def get_workflow(
        self
    ):

        return self.queue_manager.pop()


    def schedule_workflow(
        self,
        workflow,
        execute_at
    ):

        return self.scheduler.schedule(
            workflow,
            execute_at
        )


    def fail_workflow(
        self,
        workflow,
        reason
    ):

        self.metrics.record_failed()

        return self.queue_manager.route_failed_task(
            workflow,
            reason
        )


    def stats(self):

        return {
            "queue": self.queue_manager.stats(),
            "metrics": self.metrics.stats(),
            "scheduled": self.scheduler.size()
        }
