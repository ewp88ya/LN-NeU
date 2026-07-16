from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name = "base-agent"

    @abstractmethod
    async def run(self, task):
        pass
