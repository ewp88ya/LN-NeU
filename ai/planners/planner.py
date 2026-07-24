from models.plan import AgentPlan, PlanStep
from models.planner_decision import PlannerDecision

from planners.graph import AgentDependencyGraph
from planners.selector import AgentSelector



class PlannerAgent:

    name = "planner-agent"



    def __init__(self):

        self.graph = AgentDependencyGraph()

        self.selector = AgentSelector()



    def decide(
        self,
        task
    ):

        action = task.action.lower()


        #
        # Explicit action priority
        #

        if action in [
            "network",
            "ping"
        ]:

            return PlannerDecision(

                goal="network operation",

                strategy="single-agent",

                agents=[
                    "network-agent"
                ],

                reasoning="Explicit network action detected"

            )



        if action in [
            "analyze",
            "analysis"
        ]:

            return PlannerDecision(

                goal="analysis task",

                strategy="single-agent",

                agents=[
                    "analysis-agent"
                ],

                reasoning="Explicit analysis action detected"

            )



        if action in [
            "optimize"
        ]:

            return PlannerDecision(

                goal="optimization task",

                strategy="single-agent",

                agents=[
                    "optimizer-agent"
                ],

                reasoning="Explicit optimization action detected"

            )



        #
        # Dynamic intent selection
        #

        selected_agents = self.selector.select(
            task
        )


        #
        # Strategy decision
        #

        if len(selected_agents) == 1:

            strategy = "single-agent"

        else:

            strategy = "sequential"



        return PlannerDecision(

            goal="dynamic multi agent task",

            strategy=strategy,

            agents=selected_agents,

            reasoning="Agent selected from task intent"

        )



    def create_plan(
        self,
        task
    ):


        decision = self.decide(
            task
        )


        dependency_steps = self.graph.build(
            decision.agents
        )


        steps = []


        for item in dependency_steps:


            steps.append(

                PlanStep(

                    id=item["id"],

                    agent=item["agent"],

                    depends_on=item["depends_on"],

                    action=task.action

                )

            )



        return AgentPlan(

            planner=self.name,

            goal=decision.goal,

            strategy=decision.strategy,

            agents=decision.agents,

            steps=steps,

            reasoning=decision.reasoning

        )
