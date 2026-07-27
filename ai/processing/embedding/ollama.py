import httpx

from .provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        url="http://172.17.160.1:11434",
        model="nomic-embed-text"
    ):
        self.url = url
        self.model = model


    def embed(self, text):

        response = httpx.post(
            f"{self.url}/api/embeddings",
            json={
                "model": self.model,
                "prompt": text
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return {
            "model": self.model,
            "vector": data["embedding"]
        }
