from pydantic import BaseModel
from typing import List


class PlannerDecision(BaseModel):

    goal: str

    strategy: str

    agents: List[str]

    reasoning: str | None = None
