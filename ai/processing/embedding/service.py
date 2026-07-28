from providers.embedding_factory import get_embedding_provider


class EmbeddingService:

    def __init__(
        self,
        provider=None
    ):

        self.provider = (
            provider
            or get_embedding_provider()
        )

    def embed(
        self,
        text
    ):

        return self.provider.embed(
            text
        )
