from .base import BaseVectorDB



class MemoryVectorDB(BaseVectorDB):


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
