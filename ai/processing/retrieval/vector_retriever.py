from .base import BaseRetriever



class VectorRetriever(BaseRetriever):


    def __init__(
        self,
        vector_db,
        embedding_service
    ):

        self.vector_db = vector_db

        self.embedding_service = embedding_service



    def retrieve(
        self,
        query,
        limit=5
    ):

        embedding = (
            self.embedding_service
            .embed(query)
        )


        results = (
            self.vector_db
            .search(
                embedding["vector"],
                limit
            )
        )


        return results
