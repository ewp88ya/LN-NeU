from models.plan import AgentPlan


class PlannerAgent:

    name = "planner-agent"


    def create_plan(self, task):

        if task.action == "analyze":

            agents = [
                "analysis-agent"
            ]

            reason = "Analysis task detected"


        elif task.action == "network":

            agents = [
                "network-agent"
            ]

            reason = "Network task detected"


        elif task.action == "optimize":

            agents = [
                "optimizer-agent"
            ]

            reason = "Optimization task detected"


        else:

            agents = [
                "analysis-agent",
                "network-agent",
                "optimizer-agent"
            ]

            reason = "General multi-agent execution"


        return AgentPlan(
            planner=self.name,
            agents=agents,
            reasoning=reason
        )
