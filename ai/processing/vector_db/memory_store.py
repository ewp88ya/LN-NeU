from .schema import VectorItem


class MemoryVectorDB:


    def __init__(self):

        self.storage = []


    def insert(
        self,
        item
    ):

        self.storage.append(
            item
        )


    def search(
        self,
        vector,
        limit=5
    ):

        return self.storage[:limit]
