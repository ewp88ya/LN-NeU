class PlannerAgent:

    name = "planner-agent"


    def create_plan(self, task):

        if task.action == "analyze":
            agents = [
                "analysis-agent"
            ]

        elif task.action == "network":
            agents = [
                "network-agent"
            ]

        elif task.action == "optimize":
            agents = [
                "optimizer-agent"
            ]

        else:
            agents = [
                "analysis-agent",
                "network-agent",
                "optimizer-agent"
            ]


        return {
            "planner": self.name,
            "agents": agents
        }
