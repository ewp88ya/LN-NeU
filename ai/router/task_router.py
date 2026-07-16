from agents.executor import AgentExecutor
from workflows.engine import WorkflowEngine


class TaskRouter:

    def __init__(self):
        self.agent = AgentExecutor()
        self.workflow = WorkflowEngine()


    async def route(self, task):

        if task.action == "analyze":
            return await self.workflow.execute(
                task,
                self.agent
            )

        return {
            "status": "error",
            "message": "Unknown action"
        }
