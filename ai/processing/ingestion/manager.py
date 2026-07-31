from processing.ingestion.base import BaseIngestion
from processing.ingestion.document import Document
import json



class IngestionManager(BaseIngestion):


    def __init__(self):

        self.sources = []



    def register(
        self,
        source
    ):

        self.sources.append(
            source
        )



    async def ingest(
        self,
        data
    ):

        return await self.process(
            data
        )



    async def process(
        self,
        data
    ):

        content = data.get(
            "content"
        )

        if isinstance(content, dict):
            content = json.dumps(
                content
            )


        document = Document(
            id=data.get("id"),
            content=content,
            metadata=data.get(
                "metadata",
                {}
            )
        )

        return document
