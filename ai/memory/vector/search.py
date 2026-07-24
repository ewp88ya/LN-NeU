from memory.vector.store import VectorStore


class VectorSearch:

    def __init__(
        self,
        store: VectorStore,
    ):

        self.store = store

    def search(
        self,
        query: str,
        top_k: int = 5,
        collection: str = "default",
    ):

        return self.store.search(
            query=query,
            top_k=top_k,
            collection=collection,
        )
