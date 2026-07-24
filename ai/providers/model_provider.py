from abc import ABC, abstractmethod


class ModelProvider(ABC):


    @abstractmethod
    async def generate(
        self,
        prompt
    ):
        pass



    @abstractmethod
    async def embed(
        self,
        text
    ):
        pass
