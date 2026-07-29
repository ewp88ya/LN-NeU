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
        text:str
    ) -> str:


        text=text.lower()


        for agent, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:
                    return agent


        return "analysis"



    def create_plan(
        self,
        task
    ):


        if isinstance(task.input, dict):

            text = (
                task.input.get("message")
                or task.input.get("text")
                or str(task.input)
            )

        else:

            text=str(task.input)



        agent=self.detect_agent(text)



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
