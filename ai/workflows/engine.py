from memory.context import MemoryContext
from memory.persistent import PersistentMemory
from memory import create_memory_manager
from memory import MemoryRetrieval

from security import PromptGuard, AgentIsolation
from planners.planner import PlannerAgent
from observability.logger import AILogger

from processing import (
    ProcessingPipeline,
    TaskContext,
)

from processing.stages import InputStage

from processing.middleware import (
    OutputFormatter,
    ErrorHandler,
)

from tools import ToolRuntime
from tools import ToolSelector
from tools.network_tool import PingTool

from agents.core.manager import AgentManager
from agents.modules.analysis_agent import AnalysisAgent
from agents.modules.network_agent import NetworkAgent
from agents.modules.optimizer_agent import OptimizerAgent


class WorkflowEngine:

    def __init__(self):

        # =========================
        # Memory Layer
        # =========================

        self.memory = MemoryContext()

        self.persistent = PersistentMemory()

        self.memory_manager = create_memory_manager()

        self.memory_retrieval = MemoryRetrieval(
            self.memory_manager
        )


        # =========================
        # Security Layer
        # =========================

        self.prompt_guard = PromptGuard()

        self.agent_isolation = AgentIsolation()


        # =========================
        # Planner Layer
        # =========================

        self.planner = PlannerAgent()


        # =========================
        # Observability
        # =========================

        self.logger = AILogger()


        # =========================
        # Processing Layer
        # =========================

        self.processor = ProcessingPipeline()

        self.input_stage = InputStage(
            self.processor,
            self.prompt_guard,
            self.memory_retrieval,
            self.memory
        )

        self.output_formatter = OutputFormatter()

        self.error_handler = ErrorHandler()


        # =========================
        # Tool Runtime Layer
        # =========================

        self.tool_runtime = ToolRuntime()

        self.tool_runtime.registry.register(
            "ping_server",
            PingTool()
        )

        self.tool_selector = ToolSelector()

        # =========================
        # Agent Runtime Layer
        # =========================

        self.agent_manager = AgentManager()


        self.agent_manager.register_agent(
            AnalysisAgent()
        )


        self.agent_manager.register_agent(
            NetworkAgent(
                selector=self.tool_selector,
                runtime=self.tool_runtime
            )
        )


        self.agent_manager.register_agent(
            OptimizerAgent()
        )



    async def execute(
        self,
        task,
        agent=None
    ):

        task_id = task.taskId

        runtime = TaskContext(task)


        try:

            runtime = self.input_stage.run(
                runtime
            )

            task = runtime.task


            # Memory Context Injection

            memory_context = self.memory_retrieval.retrieve(
                task
            )


            task.context = {

                "memory": memory_context,

                "task_id": task_id

            }



            log = self.logger.start(
                task_id,
                task.action
            )



            # Planner

            runtime.plan = self.planner.create_plan(
                task
            )

            task.plan = runtime.plan

            # =========================
            # Agent Execution
            # =========================

            for agent_name in runtime.plan.agents:

                if not self.agent_isolation.validate(
                    agent_name,
                    task
                ):

                    runtime.add_agent_result(
                        {
                            "agent": agent_name,
                            "status": "blocked",
                            "reason": "agent isolation"
                        }
                    )

                    continue

                try:

                    result = await self.agent_manager.execute(
                        agent_name,
                        task,
                        self.tool_runtime,
                        self.tool_selector
                    )

                    if hasattr(result, "model_dump"):
                        agent_result = result.model_dump()
                    else:
                        agent_result = result

                    runtime.add_agent_result(
                        agent_result
                    )

                except Exception as agent_error:

                    runtime.add_agent_result(
                        {
                            "agent": agent_name,
                            "status": "failed",
                            "error": repr(agent_error),
                            "error_type": type(agent_error).__name__
                        }
                    )

            # Persistent Memory
            persistent_payload = {

                "planner": runtime.plan.model_dump(),

                "agents": runtime.agent_results,

                "context": task.context

            }

            self.persistent.store(

                task_id,

                task.action,

                task.input,

                persistent_payload

            )

            runtime.execution = self.logger.finish(
                log,
                runtime.agent_results
            )


            response = {

                "status": "completed",

                "task_id": task_id,

                "workflow": "planner-multi-agent",

                "planner": runtime.plan.model_dump(),

                "memory_context": True,

                "security": {

                    "prompt_guard": True,

                    "agent_isolation": True

                },

                "execution": runtime.execution,

                "tool_runtime": {

                    "enabled": True,

                    "results": [

                        agent.get("output", {}).get("tool_result")

                        for agent in runtime.agent_results

                        if isinstance(agent, dict)
                        and isinstance(agent.get("output"), dict)
                        and "tool_result" in agent["output"]

                    ]

                },

                "agents": runtime.agent_results

            }

            return self.output_formatter.format(
                response
            )



        except Exception as error:


            self.logger.error(
                task_id,
                repr(error)
            )


            runtime.add_error(
                repr(error)
            )


            return self.error_handler.handle(
                task,
                error
            )
