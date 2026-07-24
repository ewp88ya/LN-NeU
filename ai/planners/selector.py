class AgentSelector:


    def select(
        self,
        task
    ):

        text = str(
            task.input
        ).lower()


        agents = []


        if any(
            word in text
            for word in [
                "ping",
                "network",
                "vpn",
                "connection"
            ]
        ):

            agents.append(
                "network-agent"
            )


        if any(
            word in text
            for word in [
                "analyze",
                "check",
                "inspect",
                "report"
            ]
        ):

            agents.append(
                "analysis-agent"
            )


        if any(
            word in text
            for word in [
                "optimize",
                "improve",
                "speed",
                "performance"
            ]
        ):

            agents.append(
                "optimizer-agent"
            )


        if not agents:

            agents = [
                "analysis-agent"
            ]


        return agents
