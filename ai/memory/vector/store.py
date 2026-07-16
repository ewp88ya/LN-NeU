class VectorStore:

    def __init__(self):
        self.documents = []


    def add(self, text, metadata=None):

        self.documents.append({
            "text": text,
            "metadata": metadata or {}
        })


    def all(self):

        return self.documents
