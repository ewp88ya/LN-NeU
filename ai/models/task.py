from pydantic import BaseModel
from typing import Dict, Any, Optional


class AITask(BaseModel):
    task_id: str
    action: str
    input: str
    context: Optional[Dict[str, Any]] = None
