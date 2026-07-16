import os
from openai import AsyncOpenAI
from providers.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )


    async def generate(self, prompt: str):

        response = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are LN-NeU AI Engine"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "provider": "openai",
            "response": response.choices[0].message.content
        }
