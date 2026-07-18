from agents.core.base_agent import BaseAgent

class NetworkAgent(BaseAgent):

    name = "network-agent"

    async def run(self, task):

        tool_name = self.selector.select(task)

        result = await self.runtime.execute(
            self.name,
            tool_name,
            host=task.input
        )

        return {
            "agent": self.name,
            "tool": tool_name,
            "result": result
        }
