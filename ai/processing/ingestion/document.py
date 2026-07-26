from datetime import datetime
from pydantic import BaseModel


class Document(BaseModel):

    id: str

    content: str

    metadata: dict = {}

    created_at: datetime = datetime.utcnow()
