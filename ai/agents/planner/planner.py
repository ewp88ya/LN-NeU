from pydantic import BaseModel
from typing import List, Dict



class AgentPlan(BaseModel):

    agents: List[str]

    steps: List[Dict]



class AgentPlanner:


    def __init__(self):

        self.rules = {


            "network": [

                "network",
                "ping",
                "dns",
                "ip",
                "firewall",
                "port",
                "latency",
                "connection",
                "scan"

            ],



            "optimizer": [

                "optimize",
                "performance",
                "improve",
                "speed",
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


        for agent, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:

                    return agent


        return "analysis"



    def create_plan(
        self,
        task
    ):


        #
        # PRIORITY 1
        # Check action first
        #

        action_text = str(
            task.action
        )


        agent = self.detect_agent(
            action_text
        )


        #
        # PRIORITY 2
        # Check input if action unclear
        #

        if agent == "analysis":


            if isinstance(
                task.input,
                dict
            ):

                text = (

                    task.input.get(
                        "message"
                    )

                    or

                    task.input.get(
                        "text"
                    )

                    or

                    str(task.input)

                )


            else:

                text = str(
                    task.input
                )


            agent = self.detect_agent(
                text
            )



        return AgentPlan(


            agents=[

                agent

            ],



            steps=[


                {

                    "step":1,

                    "agent":agent,

                    "action":task.action,

                    "input":task.input

                }


            ]

        )
