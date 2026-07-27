from .vector_retriever import VectorRetriever


class RetrievalManager:

    def __init__(
        self,
        vector_db,
        embedding_service
    ):

        self.retriever = VectorRetriever(
            vector_db,
            embedding_service,
            threshold=0.0
        )


    def retrieve(
        self,
        query,
        limit=5,
        metadata_filter=None
    ):

        return self.retriever.retrieve(
            query,
            limit,
            metadata_filter
        )
