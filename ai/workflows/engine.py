from memory.context import MemoryContext
from memory.persistent import PersistentMemory
from observability.logger import AILogger

from agents.core.manager import AgentManager
from agents.modules.analysis_agent import AnalysisAgent
from agents.modules.network_agent import NetworkAgent
from agents.modules.optimizer_agent import OptimizerAgent


class WorkflowEngine:

    def __init__(self):

        self.memory = MemoryContext()
        self.persistent = PersistentMemory()
        self.logger = AILogger()

        self.agent_manager = AgentManager()

        self.agent_manager.register_agent(
            AnalysisAgent()
        )

        self.agent_manager.register_agent(
            NetworkAgent()
        )

        self.agent_manager.register_agent(
            OptimizerAgent()
        )


    async def execute(self, task, agent=None):

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


        results = []


        selected_agents = [
            "network-agent",
            "analysis-agent",
            "optimizer-agent"
        ]


        for agent_name in selected_agents:

            result = await self.agent_manager.execute(
                agent_name,
                task
            )

            results.append(result)


        self.persistent.store(
            task.taskId,
            task.action,
            task.input,
            results
        )


        execution = self.logger.finish(
            log,
            results
        )


        return {
            "workflow": "multi-agent",
            "persistent": True,
            "execution": execution,
            "agents": results
        }
