from agents.core.base_agent import BaseAgent
from providers.factory import get_provider


class AnalysisAgent(BaseAgent):

    name = "analysis-agent"


    def __init__(self):
        self.model = get_provider()


    async def run(self, task):

        prompt = f"""
You are Analysis Agent.

Analyze this task:

Action:
{task.action}

Input:
{task.input}

Give technical analysis.
"""

        response = await self.model.generate(prompt)

        return {
            "agent": self.name,
            "result": response
        }
