from .vector_retriever import VectorRetriever


class RetrievalManager:


    def __init__(
        self,
        vector_db,
        embedding_service
    ):

        self.retriever = VectorRetriever(
            vector_db,
            embedding_service
        )



    def retrieve(
        self,
        query,
        limit=5
    ):

        return self.retriever.retrieve(
            query,
            limit
        )
