import os

from providers.mock_provider import MockProvider
from providers.ollama_provider import OllamaProvider


def get_provider():

    provider = os.getenv(
        "AI_PROVIDER",
        "ollama"
    )

    if provider == "ollama":
        return OllamaProvider()

    return MockProvider()
