from prompts.manager import PromptManager
from providers.factory import get_provider
from tools.registry import ToolRegistry


class AgentExecutor:

    def __init__(self):

        self.prompt = PromptManager()
        self.model = get_provider()
        self.tools = ToolRegistry()


    async def execute(self, task):

        tool_result = None

        # contoh tool trigger
        if "ping" in task.input.lower():

            tool = self.tools.get("ping_server")

            tool_result = await tool.run(
                host="8.8.8.8"
            )


        prompt = self.prompt.build(
            task.action,
            task.input
        )


        if tool_result:

            prompt += f"""

Tool Result:
{tool_result}
"""


        response = await self.model.generate(
            prompt
        )


        return {
            "taskId": task.taskId,
            "agent": "analysis-agent",
            "tool": tool_result,
            "response": response
        }
