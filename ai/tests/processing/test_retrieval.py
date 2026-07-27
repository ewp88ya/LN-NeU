import pytest

from processing.embedding import EmbeddingService
from processing.vector_db import VectorDBManager
from processing.retrieval import RetrievalManager


def test_retrieval_flow():

    embedding = EmbeddingService()

    vector_db = VectorDBManager()

    retrieval = RetrievalManager(
        vector_db=vector_db,
        embedding_service=embedding
    )

    vector = embedding.embed(
        "network security"
    )

    vector_db.insert(
        {
            "embedding": vector,
            "content": "Network security configuration"
        }
    )

    result = retrieval.retrieve(
        "network security"
    )

    assert result is not None
    assert len(result) > 0
