from processing.ingestion.document import Document


class Extractor:


    async def extract(
        self,
        document: Document
    ) -> dict:

        return {
            "id": document.id,
            "content": document.content,
            "metadata": document.metadata
        }
