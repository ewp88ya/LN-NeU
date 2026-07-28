from providers.model_provider import ModelProvider


class MockProvider(ModelProvider):

    async def generate(self, prompt: str):

        return {
            "provider": "mock",
            "response": prompt,
        }

    async def embed(self, text: str):

        return {
            "model": "mock-embedding",
            "vector": [0.0] * 768,
        }
