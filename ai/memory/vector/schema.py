from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class VectorDocument:


    id: str

    text: str

    metadata: dict = field(
        default_factory=dict
    )

    created_at: str = field(
    default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

@dataclass
class SearchResult:


    id: str

    text: str

    score: float

    metadata: dict
