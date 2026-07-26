from .base import DataSource
from .document import Document
from .manager import IngestionManager


DataIngestionPipeline = IngestionManager


__all__ = [
    "DataSource",
    "Document",
    "IngestionManager",
    "DataIngestionPipeline",
]
