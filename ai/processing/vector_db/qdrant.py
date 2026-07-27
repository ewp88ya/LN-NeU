from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from .config import (
    QDRANT_URL,
    QDRANT_COLLECTION
)


class QdrantVectorDB:


    def __init__(self):

        self.client = QdrantClient(
            url=QDRANT_URL
        )

        self.collection = QDRANT_COLLECTION

        self._ensure_collection()



    def _ensure_collection(self):

        collections = (
            self.client
            .get_collections()
            .collections
        )

        exists = any(
            c.name == self.collection
            for c in collections
        )


        if not exists:

            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE
                )
            )



    def insert(
        self,
        item
    ):

        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=item.id,
                    vector=item.embedding,
                    payload={
                        "content": item.content,
                        "metadata": item.metadata
                    }
                )
            ]
        )



    def search(
        self,
        vector,
        limit=5
    ):

        results = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=limit
        )


        return [
            {
                "content": r.payload["content"],
                "metadata": r.payload["metadata"]
            }
            for r in results
        ]
