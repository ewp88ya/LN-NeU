from .ollama import OllamaEmbeddingProvider


class EmbeddingService:


    def __init__(
        self,
        provider=None
    ):

        self.provider = (
            provider
            or OllamaEmbeddingProvider()
        )


    def embed(
        self,
        text
    ):

        return self.provider.embed(
            text
        )
