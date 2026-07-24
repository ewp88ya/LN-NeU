class OllamaEmbeddingProvider:


    def __init__(
        self
    ):

        self.name = "ollama-embedding"



    async def embed(
        self,
        text
    ):

        # placeholder production interface
        # nanti connect Ollama embedding model

        vector = [
            float(
                len(text)
            )
        ]


        return vector
