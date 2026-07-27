from .base import BaseRetriever


class VectorRetriever(BaseRetriever):

    def __init__(
        self,
        vector_db,
        embedding_service,
        threshold=0.0
    ):
        self.vector_db = vector_db
        self.embedding_service = embedding_service
        self.threshold = threshold


    def retrieve(
        self,
        query,
        limit=5,
        metadata_filter=None
    ):

        embedding = self.embedding_service.embed(
            query
        )

        results = self.vector_db.search(
            embedding["vector"],
            limit
        )


        output = []

        for item in results:

            if hasattr(item, "content"):
                content = item.content
                metadata = item.metadata
                score = getattr(
                    item,
                    "score",
                    1.0
                )

            else:
                content = item["content"]
                metadata = item.get(
                    "metadata",
                    {}
                )
                score = item.get(
                    "score",
                    1.0
                )


            # similarity threshold
            if score < self.threshold:
                continue


            # metadata filtering
            if metadata_filter:

                match = all(
                    metadata.get(k) == v
                    for k, v in metadata_filter.items()
                )

                if not match:
                    continue


            output.append(
                {
                    "content": content,
                    "metadata": metadata,
                    "score": score
                }
            )


        return output
