from config.settings import settings

import httpx
import time
from datetime import datetime, UTC

class OllamaProvider:


    def __init__(self):

        self.url = settings.OLLAMA_URL.replace(
            "/api/generate",
            "/api/chat"
        )

        self.model = settings.OLLAMA_MODEL


    async def generate(
        self,
        prompt: str,
        context=None
    ):


        start_time = time.time()


        payload = {

            "model": self.model,

            "messages": [

                {
                    "role": "system",
                    "content":
                    "You are LN-NeU AI Core Engine."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            "stream": False,

            "options": {

                "num_ctx": 4096,

                "temperature": 0.7,

                "num_predict": 1024

            }

        }



        if context:

            payload["messages"].insert(

                1,

                {

                    "role":"system",

                    "content":
                    f"Context:\n{context}"

                }

            )



        async with httpx.AsyncClient(

            timeout=180.0

        ) as client:


            response = await client.post(

                self.url,

                json=payload

            )


        response.raise_for_status()



        data = response.json()



        latency = (
            time.time()
            -
            start_time
        )



        content = data.get(

            "message",

            {}

        ).get(

            "content",

            ""

        )



        return {


            "provider":
            "ollama",


            "model":
            self.model,


            "response":
            content,


            "metadata":{


                "timestamp":
                datetime.now(UTC).isoformat(),


                "latency":
                latency,


                "context_size":
                4096,


                "tokens":
                len(content.split())

            }

        }
