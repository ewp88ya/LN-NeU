from pydantic import BaseModel
from typing import List


class AgentPlan(BaseModel):

    planner: str
    agents: List[str]
    reasoning: str | None = None
