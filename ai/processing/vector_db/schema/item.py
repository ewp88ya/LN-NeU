from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class VectorItem:

    id: str

    embedding: list[float]

    content: str

    metadata: Dict[str, Any]
