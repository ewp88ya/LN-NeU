from pydantic import BaseModel
from typing import Any, Dict


class WorkflowResponse(BaseModel):

    status: str

    task_id: str

    workflow: str

    result: Dict[str, Any] | None = None

    error: str | None = None
