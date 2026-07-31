from memory.context import MemoryContext
from memory.persistent import PersistentMemory
from memory import create_memory_manager
from memory import MemoryRetrieval
from tools.http_tool import HTTPTool
from processing import ProcessingOrchestrator
from agents.planner.planner import AgentPlanner
from agents.executor import AgentExecutor

from security import (
    PromptGuard,
    AgentIsolation,
)

from security.middleware import SecurityMiddleware


from observability.logger import (
    get_logger,
    log_event
)

from observability.metrics import MetricsCollector
from observability.audit import AuditLogger
from observability.tracing import TraceManager
from observability.health import HealthMonitor


from processing import (
    ProcessingPipeline,
    TaskContext,
)

from processing.stages import InputStage

from processing.middleware import (
    OutputFormatter,
    ErrorHandler,
)

from tools import (
    ToolRuntime,
    ToolSelector,
)

from tools.network_tool import (
    PingTool,
)

from tools.dns_tool import (
    DNSTool,
)

from tools.http_tool import (
    HTTPTool,
)

from agents.core.manager import AgentManager

from agents.modules.analysis_agent import AnalysisAgent
from agents.modules.network_agent import NetworkAgent
from agents.modules.optimizer_agent import OptimizerAgent



class WorkflowEngine:


    def __init__(self):

        self.processing_orchestrator = ProcessingOrchestrator()

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

        self.security = SecurityMiddleware()

        self.security_audit = self.security.audit


        # =========================
        # Planner
        # =========================

        self.planner = AgentPlanner()

        # =========================
        # Observability
        # =========================

        self.logger = get_logger(
            "workflow_engine"
        )

        self.metrics = MetricsCollector()

        self.audit = AuditLogger()

        self.tracer = TraceManager()

        self.health = HealthMonitor()


        # =========================
        # Processing
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
        # Tool Runtime
        # =========================

        self.tool_runtime = ToolRuntime(
            metrics=self.metrics,
            audit=self.audit

        )
        self.tool_runtime.registry.register(
            "ping_server",
            PingTool()
        )


        self.tool_runtime.registry.register(
            "dns_lookup",
            DNSTool()
        )


        self.tool_runtime.registry.register(
            "http_check",
            HTTPTool()
        )

        self.tool_selector = ToolSelector()



        # =========================
        # Agent Runtime
        # =========================

        self.agent_manager = AgentManager()

        self.executor = AgentExecutor(
            self.agent_manager
        )

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

        print(
            "DEBUG ENTER EXECUTE",
            flush=True
        )

        print(
            "DEBUG TASK:",
            task,
            flush=True
        )

        print(
            "DEBUG ACTION VALUE:",
            task.action,
            type(task.action),
            flush=True
        )

        print(
            "DEBUG INPUT VALUE:",
            task.input,
            type(task.input),
            flush=True
        )


        task_id = task.taskId


        self.metrics.task_started()


        self.audit.record(
            "task_started",
            {
                "task_id": task_id,
                "action": task.action
            }
        )


        trace = self.tracer.start(
            task_id,
            task.action
        )


        runtime = TaskContext(task)



        try:


            # =========================
            # Security Validation
            # =========================

            security_context = self.security.validate(
                task
            )


            self.audit.record(
                "security_validated",
                {
                    "task_id": task_id
                }
            )



            # =========================
            # Input Processing
            # =========================

            runtime = self.input_stage.run(
                runtime
            )

            runtime = await self.processing_orchestrator.run(
                runtime
            )

            task = runtime.task



            # =========================
            # Memory Retrieval
            # =========================

            memory_context = self.memory_retrieval.retrieve_context(
                task_id,
                task.input
            )


            task.context = {

                "memory": memory_context,

                "task_id": task_id

            }


            # =========================
            # Planner
            # =========================

            runtime.plan = self.planner.create_plan(
                task
            )


            log_event(
               self.logger,
               "info",
               "workflow started",
               event="workflow_start",
               service="workflow_engine",
               metadata={
               "task_id": task_id,
               "action": task.action
               }
            )


            # =========================
            # Agent Execution
            # =========================

            for step in runtime.plan.steps:

                agent_name = step["agent"]


                if not self.agent_isolation.validate(
                    agent_name,
                    task
                ):

                    self.metrics.agent_failed()


                    runtime.add_agent_result(
                        {
                            "agent": agent_name,
                            "status": "blocked",
                            "reason": "agent isolation"
                        }
                    )


                    continue



                try:


                    self.audit.record(
                        "agent_execution_started",
                        {
                            "agent":agent_name,
                            "task_id":task_id
                        }
                    )



                    result = await self.executor.execute(
                        step,
                        task,
                        self.tool_runtime,
                        self.tool_selector
                    )


                    if hasattr(
                        result,
                        "model_dump"
                    ):

                        result = result.model_dump()



                    runtime.add_agent_result(
                        result
                    )


                    self.metrics.agent_used()



                    self.audit.record(
                        "agent_execution_completed",
                        {
                            "agent":agent_name,
                            "task_id":task_id
                        }
                    )



                except Exception as agent_error:


                    self.metrics.agent_failed()


                    runtime.add_agent_result(
                        {
                            "agent":agent_name,
                            "status":"failed",
                            "error":repr(agent_error)
                        }
                    )



            # =========================
            # Persistent Memory
            # =========================

            self.persistent.store(

                task_id,

                task.action,

                task.input,

                {

                    "planner":
                        runtime.plan.model_dump(),

                    "agents":
                        runtime.agent_results,

                    "context":
                        task.context

                }

            )

            runtime.execution = {
                "completed": True,
                "agents": runtime.agent_results
            }

            log_event(
                self.logger,
                "info",
                "workflow completed",
                event="workflow_finish",
                service="workflow_engine",
                metadata={
                    "task_id": task_id,
                    "agents": len(runtime.agent_results)
                }
            )

            execution_time = trace.finish()


            self.metrics.task_completed(
                execution_time
            )



            self.audit.record(
                "task_completed",
                {
                    "task_id":task_id,
                    "agents":len(
                        runtime.agent_results
                    )
                }
            )



            response = {

                "status":"completed",

                "task_id":task_id,

                "workflow":
                    "planner-multi-agent",


                "security":{

                    "authenticated":
                        security_context.get(
                            "authenticated",
                            False
                        )

                },


                "planner":
                    runtime.plan.model_dump(),


                "execution":
                    runtime.execution,


                "tool_runtime":{

                    "registered":
                    list(
                        self.tool_runtime.registry.tools.keys()
                    )

                },


                "agents":
                    runtime.agent_results

            }



            return self.output_formatter.format(
                response
            )



        except Exception as error:

            import traceback

            traceback.print_exc()

            self.metrics.task_failed()

            self.audit.record(
                "task_failed",
                {
                    "task_id": task_id,
                    "error": repr(error)
                }
            )

            log_event(
                self.logger,
                "error",
                repr(error),
                event="workflow_error",
                service="workflow_engine",
                metadata={
                    "task_id": task_id
                }
            )

            try:
                trace.finish()

            except Exception:
                pass

            runtime.add_error(
                repr(error)
            )

            return self.error_handler.handle(
                task,
                error
            )
