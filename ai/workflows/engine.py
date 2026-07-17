from memory.context import MemoryContext
from memory.persistent import PersistentMemory
from memory import create_memory_manager
from memory import MemoryRetrieval

from security import PromptGuard, AgentIsolation

from planners.planner import PlannerAgent

from observability.logger import AILogger
from processing.pipeline import ProcessingPipeline

from agents.core.manager import AgentManager
from agents.modules.analysis_agent import AnalysisAgent
from agents.modules.network_agent import NetworkAgent
from agents.modules.optimizer_agent import OptimizerAgent


class WorkflowEngine:

    def __init__(self):

        self.memory = MemoryContext()
        self.persistent = PersistentMemory()

        self.memory_manager = create_memory_manager()

        self.memory_retrieval = MemoryRetrieval(
            self.memory_manager
        )

        self.prompt_guard = PromptGuard()

        self.agent_isolation = AgentIsolation()

        self.planner = PlannerAgent()

        self.logger = AILogger()

        self.processor = ProcessingPipeline()

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

        security = self.prompt_guard.inspect(
            task.input
        )

        if not security["allowed"]:
            return {
                "status": "blocked",
                "reason": security["reason"]
            }

        log = self.logger.start(
            task.task_id,
            task.action
        )

        context = self.memory_retrieval.retrieve_context(
            task.task_id,
            task.input
        )

        task.context = context

        processed = self.processor.process(
            task
        )

        self.memory.save(
            task.task_id,
            processed
        )

        plan = self.planner.create_plan(
            task
        )

        task.plan = plan

        results = []

        for agent_name in plan.agents:

            if not self.agent_isolation.validate(
                agent_name,
                task
            ):
                results.append({
                    "agent": agent_name,
                    "status": "blocked",
                    "reason": "agent isolation"
                })
                continue

            result = await self.agent_manager.execute(
                agent_name,
                task
            )

            results.append(result)

        self.persistent.store(
            task.task_id,
            task.action,
            task.input,
            results
        )

        execution = self.logger.finish(
            log,
            results
        )

        return {
            "workflow": "planner-multi-agent",
            "planner": plan.model_dump(),
            "persistent": True,
            "memory_context": True,
            "security": {
                "prompt_guard": True,
                "agent_isolation": True
            },
            "execution": execution,
            "agents": results
        }
