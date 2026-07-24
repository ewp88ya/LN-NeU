from agents.modules.analysis_agent import AnalysisAgent
from agents.modules.network_agent import NetworkAgent
from agents.modules.optimizer_agent import OptimizerAgent


class AgentExecutor:


    def __init__(self):

        self.agents = {
            "analysis": AnalysisAgent(),
            "network": NetworkAgent(),
            "optimizer": OptimizerAgent(),
        }



    async def execute(self, task):

        action = task.action.lower()


        # normalize input
        if isinstance(task.input, dict):

            text = (
                task.input.get("message")
                or task.input.get("text")
                or str(task.input)
            )

        else:

            text = str(task.input)



        text_lower = text.lower()



        if action in self.agents:

            agent = self.agents[action]

        elif "ping" in text_lower:

            agent = self.agents["network"]

        else:

            agent = self.agents["analysis"]



        return await agent.run(
            task
        )
