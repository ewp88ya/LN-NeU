from agents.core.registry import AgentRegistry


class AgentManager:

    def __init__(self):

        self.registry = AgentRegistry()


    def register_agent(self, agent):

        self.registry.register(agent)


    async def execute(

        self,

        agent_name,

        task,

        runtime=None,

        selector=None

    ):

        agent = self.registry.get(agent_name)

        if not agent:

            return {
                "error": f"Agent {agent_name} not found"
            }


        agent.runtime = runtime

        agent.selector = selector


        return await agent.run(task)
