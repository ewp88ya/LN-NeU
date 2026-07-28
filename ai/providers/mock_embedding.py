import hashlib

from processing.embedding.provider import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):

    def embed(self, text):

        digest = hashlib.sha256(
            text.encode()
        ).digest()

        vector = []

        while len(vector) < 768:
            for b in digest:
                vector.append(b / 255.0)
                if len(vector) == 768:
                    break

        return {
            "model": "mock-embedding",
            "vector": vector
        }
