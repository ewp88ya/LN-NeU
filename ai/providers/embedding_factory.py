import os

from providers.mock_embedding import MockEmbeddingProvider
from providers.ollama_embedding import OllamaEmbeddingProvider


def get_embedding_provider():
    provider = os.getenv("EMBEDDING_PROVIDER", "mock").lower()

    if provider == "ollama":
        return OllamaEmbeddingProvider()

    return MockEmbeddingProvider()
