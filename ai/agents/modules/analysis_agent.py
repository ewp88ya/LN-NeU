from agents.core.base_agent import BaseAgent
from providers.factory import get_provider


class AnalysisAgent(BaseAgent):

    name = "analysis-agent"


    def __init__(self):
        self.model = get_provider()


    async def run(self, task):

        memory = self.get_memory(task)

        prompt = f"""
You are Analysis Agent.

Analyze this task.

Action:
{task.action}

Input:
{task.input}

Previous Context:
{memory}

Use previous context when relevant.

Give technical analysis.
"""

        response = await self.model.generate(
            prompt
        )

        return {
            "agent": self.name,
            "memory_used": True,
            "result": response
        }
