from abc import ABC, abstractmethod


class AIModel(ABC):

    @abstractmethod
    async def generate(self, prompt: str):
        pass
