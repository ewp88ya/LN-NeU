from queue import TaskQueue

from agents.executor import AgentExecutor
from workflows.engine import WorkflowEngine


class TaskRouter:

    def __init__(self):

        self.agent = AgentExecutor()

        self.workflow = WorkflowEngine()

        self.queue = TaskQueue()

    async def route(self, task):

        self.queue.push(task)

        return {
            "status": "queued",
            "message": "Task successfully queued",
            "task_id": task.task_id,
            "queue_size": self.queue.size()
        }
