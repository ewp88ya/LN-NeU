from pydantic import BaseModel
from typing import List


class PlanStep(BaseModel):

    id: int

    agent: str

    depends_on: list[int] = []

    action: str | None = None



class AgentPlan(BaseModel):

    planner: str

    goal: str

    strategy: str

    agents: List[str]

    steps: List[PlanStep]

    reasoning: str | None = None
