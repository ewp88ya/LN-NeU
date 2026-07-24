from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult,
)

from providers.factory import get_provider


class AnalysisAgent(BaseAgent):

    name = "analysis-agent"

    def __init__(
        self,
        selector=None,
        runtime=None,
    ):
        super().__init__()

        self.selector = selector
        self.runtime = runtime

        self.model = get_provider()

    async def run(
        self,
        task: AgentTask,
    ) -> AgentResult:

        try:

            memory = self.get_memory(task)

            prompt = f"""
You are LN-NeU Analysis Agent.

Your role:
- Analyze incoming tasks
- Use available memory context
- Produce structured technical analysis.

Task Action:
{task.action}

Task Input:
{task.input}

Memory Context:
{memory}

Instructions:
1. Analyze the request carefully.
2. Use previous context when relevant.
3. Provide clear technical reasoning.
4. Return useful information for the workflow engine.
"""

            response = await self.model.generate(prompt)

            tool_result = await self.execute_tool(
                task,
                host="8.8.8.8",
            )

            if hasattr(tool_result, "model_dump"):
                tool_output = tool_result.model_dump()
            else:
                tool_output = tool_result

            task_id = getattr(
                task,
                "taskId",
                getattr(task, "task_id", None),
            )

            return self.success(
                output={
                    "analysis": response,
                    "memory_used": bool(memory),
                    "tool_result": tool_output,
                },
                metadata={
                    "task_id": task_id,
                    "agent": self.name,
                },
            )

        except Exception as error:

            task_id = getattr(
                task,
                "taskId",
                getattr(task, "task_id", None),
            )

            return self.failed(
                error,
                metadata={
                    "task_id": task_id,
                    "agent": self.name,
                },
            )
