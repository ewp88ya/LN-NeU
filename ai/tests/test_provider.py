import pytest
from providers.ollama_provider import OllamaProvider


@pytest.mark.asyncio
async def test_provider_generate(monkeypatch):

    provider = OllamaProvider()

    async def mock_generate(*args, **kwargs):
        return {
            "response": "hello from mock"
        }

    monkeypatch.setattr(
        provider,
        "generate",
        mock_generate
    )

    result = await provider.generate("hello")

    assert result["response"] == "hello from mock"
