from agents.core.base_agent import BaseAgent


class NetworkAgent(BaseAgent):

    name = "network-agent"


    async def run(self, task):

        return {
            "agent": self.name,
            "result": {
                "type": "network-analysis",
                "message": f"Checking network issue: {task.input}"
            }
        }
