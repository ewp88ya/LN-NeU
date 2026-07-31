from agents.core.registry import AgentRegistry


class AgentManager:

    def __init__(self):

        self.registry = AgentRegistry()


    def register_agent(
        self,
        agent
    ):

        print(
            "REGISTER AGENT:",
            agent.name
        )

        self.registry.register(
            agent
        )


    async def execute(

        self,

        agent_name,

        task,

        runtime=None,

        selector=None

    ):

        print(
            "REQUEST AGENT:",
            agent_name
        )

        print(
            "AVAILABLE AGENTS:",
            self.registry.list()
        )


        agent = self.registry.get(
            agent_name
        )


        if not agent:

            return {
                "error": f"Agent {agent_name} not found"
            }


        agent.runtime = runtime

        agent.selector = selector


        return await agent.run(
            task
        )
