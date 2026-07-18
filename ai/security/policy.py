class SecurityPolicy:


    def __init__(self):

        self.policies = {

            "agents": {

                "analysis-agent": [
                    "memory",
                    "llm"
                ],

                "network-agent": [
                    "network_tool"
                ],

                "optimizer-agent": [
                    "analysis"
                ]

            },


            "tools": {

                "ping_server": [
                    "network-agent",
                    "analysis-agent"
                ]

            },


            "actions": {

                "analyze": [
                    "analysis-agent"
                ],

                "network": [
                    "network-agent"
                ],

                "optimize": [
                    "optimizer-agent"
                ]

            }

        }



    def allow_agent(
        self,
        agent,
        capability
    ):

        allowed = self.policies[
            "agents"
        ].get(
            agent,
            []
        )


        return capability in allowed



    def allow_tool(
        self,
        agent,
        tool
    ):

        allowed = self.policies[
            "tools"
        ].get(
            tool,
            []
        )


        return agent in allowed



    def allow_action(
        self,
        action,
        agent
    ):

        allowed = self.policies[
            "actions"
        ].get(
            action,
            []
        )


        return agent in allowed
