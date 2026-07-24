from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult
)


class OptimizerAgent(BaseAgent):

    name = "optimizer-agent"

    def __init__(
        self,
        selector=None,
        runtime=None
    ):

        super().__init__()

        self.selector = selector
        self.runtime = runtime

    async def run(
        self,
        task: AgentTask
    ) -> AgentResult:

        try:

            memory = self.get_memory(
                task
            )

            tool_result = await self.execute_tool(
                task,
                host="8.8.8.8"
            )

            optimization = {

                "type": "optimization",

                "recommendation":
                    "Analyze bottleneck and apply optimization strategy",

                "context": memory,

                "tool_result": (
                    tool_result.model_dump()
                    if tool_result
                    else None
                )

            }

            return self.success(

                output=optimization,

                metadata={

                  "task_id": getattr(
                       task,
                       "taskId",
                       getattr(task, "task_id", None)
                ),

                    "agent": self.name

                }

            )

        except Exception as error:

            return self.failed(

                error,

                metadata={

                    "task_id": getattr(
                        task,
                        "task_id",
                        None
                    ),

                    "agent": self.name

                }

            )
