class VectorStore:


    def __init__(self):

        self.items = []



    def insert(
        self,
        item
    ):

        self.items.append(
            item
        )



    def search(
        self,
        query
    ):

        return self.items
