from task_queue.instance import task_queue

from agents.executor import AgentExecutor
from workflows.engine import WorkflowEngine


class TaskRouter:

    def __init__(self):

        self.agent = AgentExecutor()

        self.workflow = WorkflowEngine()

        # Shared queue with worker
        self.queue = task_queue


    async def route(self, task):

        self.queue.push(task)

        return {
            "status": "queued",
            "message": "Task successfully queued",
            "task_id": task.taskId,
            "queue_size": self.queue.size()
        }
