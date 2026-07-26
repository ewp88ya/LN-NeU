from processing.ingestion.document import Document


class IngestionManager:


    def __init__(self):

        self.sources = []


    def register(self, source):

        self.sources.append(source)



    async def process(self, data):

        document = Document(
            id=data.get("id"),
            content=data.get("content"),
            metadata=data.get(
                "metadata",
                {}
            )
        )

        return document

