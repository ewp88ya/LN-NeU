from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, Optional, List


class AgentTask(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True
    )

    task_id: str = Field(
        alias="taskId"
    )

    agent_id: Optional[str] = None

    action: str

    input: Any

    context: Dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    memory: Optional[Dict[str, Any]] = None

    plan: Optional[Any] = None

    processed: Optional[Any] = None


class AgentResult(BaseModel):

    agent: str

    status: str

    output: Optional[Any] = None

    error: Optional[str] = None

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class AgentExecution(BaseModel):

    task_id: str

    results: List[AgentResult] = Field(
        default_factory=list
    )
