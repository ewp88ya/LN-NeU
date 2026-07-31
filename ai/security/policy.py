class SecurityPolicy:

    def __init__(self):

        self.policies = {

            "agents": {

                "analysis": [
                    "memory",
                    "llm"
                ],

                "network": [
                    "network_tool"
                ],

                "optimizer": [
                    "analysis"
                ]

            },

            "tools": {

                "ping_server": [
                    "network",
                    "analysis"
                ],

                "dns_lookup": [
                    "network",
                    "analysis"
                ],

                "http_check": [
                    "network"
                ]

            },

            "actions": {

                "analyze": [
                    "analysis"
                ],

                "analysis": [
                    "analysis"
                ],

                "network": [
                    "network"
                ],

                "network_scan": [
                    "network"
                ],

                "ping": [
                    "network"
                ],

                "dns_lookup": [
                    "network"
                ],

                "http_check": [
                    "network"
                ],

                "optimize": [
                    "optimizer"
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
