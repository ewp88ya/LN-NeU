from providers.model_provider import ModelProvider


class MockProvider(ModelProvider):

    async def generate(self, prompt: str):

        return {
            "provider": "mock",
            "response": prompt
        }
