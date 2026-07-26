from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    async def ingest(self, data):
        pass
