from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult
)


class NetworkAgent(BaseAgent):

    name = "network-agent"


    def __init__(
        self,
        selector=None,
        runtime=None
    ):
        self.selector = selector
        self.runtime = runtime


    async def run(
        self,
        task: AgentTask
    ) -> AgentResult:

        try:

            if self.selector is None or self.runtime is None:
                return self.failed(
                    "Network runtime not configured",
                    metadata={
                        "task_id": getattr(task, "task_id", None),
                        "agent": self.name
                    }
                )


            tool_name = self.selector.select(task)


            if isinstance(task.input, dict):
                host = (
                    task.input.get("host")
                    or task.input.get("message")
                    or task.input.get("text")
                    or str(task.input)
                )
            else:
                host = str(task.input)


            result = await self.runtime.execute(
                self.name,
                tool_name,
                host=host
            )


            return self.success(
                output={
                    "tool": tool_name,
                    "result": result
                },
                metadata={
                    "task_id": task.task_id,
                    "agent": self.name
                }
            )


        except Exception as error:

            return self.failed(
                error,
                metadata={
                    "task_id": getattr(task, "task_id", None),
                    "agent": self.name
                }
            )
