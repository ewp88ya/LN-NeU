from config.settings import settings
import httpx


class OllamaProvider:

    def __init__(self):
        self.url = settings.OLLAMA_URL.replace(
            "/api/generate",
            "/api/chat"
        )

        self.model = settings.OLLAMA_MODEL


    async def generate(self, prompt: str):

        payload = {
            "model": self.model,

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            "stream": False,

            "options": {
                "num_ctx": 2048,
                "temperature": 0.7,
                "num_predict": 512
            }
        }


        print("=" * 60)
        print("LN-NeU Ollama Provider")
        print("URL          :", self.url)
        print("MODEL        :", self.model)
        print("CONTEXT      :", 2048)
        print("MAX TOKENS   :", 512)
        print("PROMPT LEN   :", len(prompt))
        print("=" * 60)


        try:

            async with httpx.AsyncClient(
                timeout=180.0
            ) as client:

                print("Sending request to Ollama...")

                response = await client.post(
                    self.url,
                    json=payload
                )

                print("Response received.")
                print("HTTP Status:", response.status_code)


            response.raise_for_status()


        except httpx.ConnectError as e:

            print("Ollama connection failed:")
            print(e)

            raise


        except httpx.RemoteProtocolError as e:

            print("Ollama disconnected during generation.")
            print(e)

            raise


        data = response.json()


        print("Response parsed successfully.")
        print("=" * 60)


        return {
            "provider": "ollama",
            "model": self.model,
            "response": data.get(
                "message",
                {}
            ).get(
                "content",
                ""
            )
        }
