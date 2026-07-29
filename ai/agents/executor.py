from agents.core.manager import AgentManager


class AgentExecutor:


    def __init__(
        self,
        agent_manager: AgentManager
    ):

        self.agent_manager = agent_manager



    async def execute(
        self,
        step,
        task,
        runtime=None,
        selector=None
    ):

        agent_name = step["agent"]


        return await self.agent_manager.execute(
            agent_name,
            task,
            runtime,
            selector
        )

