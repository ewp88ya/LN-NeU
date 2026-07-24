import asyncio
from providers.ollama_provider import OllamaProvider

async def main():
    provider = OllamaProvider()
    result = await provider.generate("hello")
    print(result)

asyncio.run(main())
