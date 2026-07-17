from typing import Dict, Any
from datetime import datetime


class ShortTermMemory:

    def __init__(self):
        self.sessions = {}


    def save(
        self,
        task_id: str,
        context: Dict[str, Any]
    ):

        self.sessions[task_id] = {
            "context": context,
            "updated_at": datetime.utcnow()
        }


    def retrieve(
        self,
        task_id: str
    ):

        return self.sessions.get(task_id)


    def clear(
        self,
        task_id: str
    ):

        if task_id in self.sessions:
            del self.sessions[task_id]
