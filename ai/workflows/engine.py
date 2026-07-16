from memory.context import MemoryContext
from memory.persistent import PersistentMemory
from observability.logger import AILogger


class WorkflowEngine:

    def __init__(self):

        self.memory = MemoryContext()
        self.persistent = PersistentMemory()
        self.logger = AILogger()


    async def execute(self, task, agent):

        log = self.logger.start(
            task.taskId,
            task.action
        )


        self.memory.save(
            task.taskId,
            {
                "action": task.action,
                "input": task.input
            }
        )


        result = await agent.execute(task)


        self.persistent.store(
            task.taskId,
            task.action,
            task.input,
            result
        )


        execution = self.logger.finish(
            log,
            result
        )


        return {
            "workflow": "default",
            "persistent": True,
            "execution": execution,
            "result": result
        }
