from abc import ABC, abstractmethod


class BaseVectorDB(ABC):


    @abstractmethod
    def insert(
        self,
        item
    ):
        pass


    @abstractmethod
    def search(
        self,
        vector,
        limit=5
    ):
        pass
