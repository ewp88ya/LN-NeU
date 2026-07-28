import os

from providers.ollama_embedding import (
    OllamaEmbeddingProvider
)
from providers.mock_embedding import (
    MockEmbeddingProvider
)


def get_embedding_provider():

    provider = os.getenv(
        "EMBEDDING_PROVIDER",
        "ollama"
    ).lower()

    if provider == "mock":
        return MockEmbeddingProvider()

    return OllamaEmbeddingProvider()
