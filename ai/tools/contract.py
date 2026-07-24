from pydantic import BaseModel
from typing import Any, Dict, Optional



class ToolRequest(BaseModel):

    agent: str

    tool: str

    action: str

    payload: Dict[str, Any] = {}



class ToolResult(BaseModel):

    tool: str

    status: str

    output: Optional[Any] = None

    error: Optional[str] = None

    metadata: Dict[str, Any] = {}
