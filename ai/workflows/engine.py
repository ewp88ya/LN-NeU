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
        # Planning Layer
        # =========================

        self.planner = PlannerAgent()


        # =========================
        # Observability
        # =========================

        self.logger = AILogger()


        # =========================
        # Processing Pipeline
        # =========================

        self.processor = ProcessingPipeline()


        # =========================
        # Agent Runtime
        # =========================

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


    async def execute(
        self,
        task,
        agent=None
    ):

        # Compatible with AITask schema
        task_id = task.taskId


        # =========================
        # Security Check
        # =========================

        security = self.prompt_guard.inspect(
            task.input
        )


        if not security["allowed"]:

            return {
                "status": "blocked",
                "task_id": task_id,
                "reason": security["reason"]
            }


        # =========================
        # Start Logging
        # =========================

        log = self.logger.start(
            task_id,
            task.action
        )


        try:


            # =========================
            # Memory Retrieval
            # =========================

            context = self.memory_retrieval.retrieve_context(
                task_id,
                task.input
            )


            task.context = context



            # =========================
            # Processing Pipeline
            # =========================

            processed = self.processor.process(
                task
            )


            self.memory.save(
                task_id,
                processed
            )



            # =========================
            # Planner
            # =========================

            plan = self.planner.create_plan(
                task
            )


            task.plan = plan



            results = []



            # =========================
            # Agent Execution
            # =========================

            for agent_name in plan.agents:


                if not self.agent_isolation.validate(
                    agent_name,
                    task
                ):

                    results.append(
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
                        task
                    )


                    results.append(
                        result
                    )


                except Exception as agent_error:

                    results.append(
                        {
                            "agent": agent_name,
                            "status": "failed",
                            "error": str(agent_error)
                        }
                    )



            # =========================
            # Persistent Memory
            # =========================

            self.persistent.store(
                task_id,
                task.action,
                task.input,
                results
            )



            # =========================
            # Finish Logging
            # =========================

            execution = self.logger.finish(
                log,
                results
            )



            return {

                "status": "completed",

                "task_id": task_id,

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



        except Exception as error:


            self.logger.error(
                task_id,
                str(error)
            )


            return {

                "status": "failed",

                "task_id": task_id,

                "error": str(error)

            }
