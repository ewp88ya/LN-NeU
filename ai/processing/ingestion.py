from processing.document_loader import DocumentLoader
from processing.chunker import TextChunker
from processing.embedding import EmbeddingPreparation

from memory.vector.store import VectorStore


class DataIngestionPipeline:

    def __init__(self):

        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedding = EmbeddingPreparation()

        self.vector = VectorStore()

    def ingest(
        self,
        file_path: str
    ):

        document = self.loader.load(
            file_path
        )

        chunks = self.chunker.split(
            document
        )

        embeddings = self.embedding.prepare(
            chunks
        )

        for item in embeddings:

            self.vector.add(
                item["text"],
                {
                    "chunk_id": item["id"]
                }
            )

        return {
            "chunks": len(chunks),
            "indexed": len(embeddings)
        }
