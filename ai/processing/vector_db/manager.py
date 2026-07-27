from .memory_store import MemoryVectorDB



class VectorDBManager:


    def __init__(self):

        self.backends = {
            "memory": MemoryVectorDB()
        }



    def insert(
        self,
        item,
        backend="memory"
    ):

        db = self.backends.get(
            backend
        )

        if not db:
            raise ValueError(
                "Vector backend not found"
            )


        db.insert(
            item
        )


    def search(
        self,
        vector,
        limit=5,
        backend="memory"
    ):

        db = self.backends.get(
            backend
        )

        if not db:
            raise ValueError(
                "Vector backend not found"
            )

        return db.search(
            vector,
            limit
        )
