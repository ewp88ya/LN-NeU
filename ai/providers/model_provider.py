from abc import ABC, abstractmethod


class ModelProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str
    ):
        pass
