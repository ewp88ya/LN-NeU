from datetime import datetime, UTC
from pydantic import BaseModel


class Document(BaseModel):

    id: str

    content: str

    metadata: dict = {}

    created_at: datetime = datetime.now(UTC)
