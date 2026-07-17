from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = "base-tool"

    async def execute(self, **kwargs):
        return await self.run(**kwargs)

    @abstractmethod
    async def run(self, **kwargs):
        pass
