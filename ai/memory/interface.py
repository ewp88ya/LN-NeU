from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class MemoryInterface(ABC):
    """
    Base interface for LN-NeU memory systems.
    """

    @abstractmethod
    def save(
        self,
        key: str,
        value: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        pass


    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int = 5
    ):
        pass


    @abstractmethod
    def delete(
        self,
        key: str
    ):
        pass
