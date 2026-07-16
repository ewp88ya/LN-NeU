from pydantic import BaseModel
from typing import Any


class AIResponse(BaseModel):
    task_id: str
    status: str
    result: Any
