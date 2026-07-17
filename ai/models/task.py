from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any


class AITask(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


    taskId: str

    action: str

    input: str


    context: Optional[Dict[str, Any]] = None


    # Workflow runtime fields

    plan: Optional[Any] = None

    processed: Optional[Any] = None
