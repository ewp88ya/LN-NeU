import os

from providers.ollama_embedding import (
    OllamaEmbeddingProvider
)



def get_embedding_provider():


    provider = os.getenv(
        "EMBEDDING_PROVIDER",
        "ollama"
    )


    if provider == "ollama":

        return OllamaEmbeddingProvider()


    return OllamaEmbeddingProvider()
