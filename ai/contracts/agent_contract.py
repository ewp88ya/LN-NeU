from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List



class AgentTask(BaseModel):

    task_id: str = Field(
        alias="taskId"
    )

    action: str

    input: str

    context: Dict[str, Any] = {}

    metadata: Dict[str, Any] = {}



    class Config:

        populate_by_name = True




class AgentResult(BaseModel):

    agent: str

    status: str

    output: Optional[Any] = None

    error: Optional[str] = None

    metadata: Dict[str, Any] = {}




class AgentExecution(BaseModel):

    task_id: str

    results: List[AgentResult] = []
