from typing import List, Dict


class AgentPlanner:
    """
    Agent Planner Layer

    Responsible for:
    - analyzing task intent
    - selecting agent
    - creating execution plan
    - preparing multi-step workflow
    """


    def __init__(self):

        self.rules = {

            "network": [
                "network",
                "ping",
                "ip",
                "dns",
                "firewall",
                "port",
                "latency",
                "connection"
            ],

            "optimizer": [
                "optimize",
                "performance",
                "improve",
                "speed",
                "reduce",
                "memory",
                "cpu"
            ],

            "analysis": [
                "analyze",
                "analyse",
                "check",
                "explain",
                "inspect",
                "review"
            ]

        }



    def detect_agent(
        self,
        text: str
    ) -> str:

        text = text.lower()

        selected = "analysis"


        for agent, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:
                    return agent


        return selected



    def build_steps(
        self,
        agent: str,
        task
    ) -> List[Dict]:

        steps = []


        steps.append(
            {
                "step": 1,
                "agent": agent,
                "action": task.action,
                "input": task.input
            }
        )


        return steps



    def plan(
        self,
        task
    ) -> List[Dict]:

        if isinstance(task.input, dict):

            text = (
                task.input.get("message")
                or task.input.get("text")
                or str(task.input)
            )

        else:

            text = str(task.input)



        selected_agent = self.detect_agent(
            text
        )


        return self.build_steps(
            selected_agent,
            task
        )
