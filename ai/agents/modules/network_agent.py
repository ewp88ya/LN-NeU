from agents.core.base_agent import BaseAgent


class NetworkAgent(BaseAgent):

    name = "network-agent"


    async def run(self, task):

        memory = self.get_memory(task)

        return {
            "agent": self.name,
            "memory_used": True,
            "result": {
                "type": "network-analysis",
                "message": f"Checking network issue: {task.input}",
                "context": memory
            }
        }
