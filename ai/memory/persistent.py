from memory.vector.store import VectorStore
from memory.vector.search import VectorSearch
from memory.storage.database import MemoryDatabase

class PersistentMemory:

    def __init__(self):
        self.db = MemoryDatabase()
      
        self.vector = VectorStore()
        self.search_engine = VectorSearch(
            self.vector
        )


    def store(
        self,
        task_id,
        action,
        input_text,
        response
    ):

        self.db.save(
            task_id,
            action,
            input_text,
            response
        )

        self.vector.add(
            input_text,
            {
                "taskId": task_id,
                "action": action
            }
        )


    def retrieve(self, task_id):

        return self.db.get(task_id)

    def retrieve_context(self, query):

        return self.search_engine.search(query)
