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
                "network"
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
                "analysis"
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
                "optimizer"
            )


        if not agents:

            agents = [
                "analysis"
            ]


        return agents
