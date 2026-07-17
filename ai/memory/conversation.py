from datetime import datetime


class ConversationMemory:

    def __init__(self):
        self.history = {}


    def add_message(
        self,
        task_id: str,
        role: str,
        content: str
    ):

        if task_id not in self.history:
            self.history[task_id] = []

        self.history[task_id].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow()
            }
        )


    def retrieve(
        self,
        task_id: str
    ):

        return self.history.get(
            task_id,
            []
        )


    def clear(
        self,
        task_id: str
    ):

        if task_id in self.history:
            del self.history[task_id]
