from pydantic import BaseModel, Field
from typing import List, Optional



class PlanStep(BaseModel):

    id: int

    agent: str

    depends_on: List[int] = Field(
        default_factory=list
    )

    action: Optional[str] = None



class AgentPlan(BaseModel):

    planner: str

    goal: Optional[str] = None

    strategy: str = "sequential"

    agents: List[str] = Field(
        default_factory=list
    )

    steps: List[PlanStep] = Field(
        default_factory=list
    )

    reasoning: Optional[str] = None
