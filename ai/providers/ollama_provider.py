import os
import httpx


class OllamaProvider:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:7b"


    async def generate(self, prompt: str):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                self.url,
                json=payload
            )

        data = response.json()

        return {
            "provider": "ollama",
            "model": self.model,
            "response": data.get("response", "")
        }
