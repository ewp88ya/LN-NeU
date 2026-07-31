from processing.ingestion import DataIngestionPipeline
from processing.etl import ETLPipeline
from processing.loader import LoaderManager
from processing.embedding import EmbeddingService
from processing.vector_db import VectorDBManager
from processing.retrieval import RetrievalManager
from processing.schema import create_metadata
from processing.vector_db.schema import VectorItem
from processing.rag import RAGBuilder

class ProcessingOrchestrator:


    def __init__(self):

        self.ingestion = DataIngestionPipeline()

        self.etl = ETLPipeline()

        self.loader = LoaderManager()

        self.embedding = EmbeddingService()

        self.vector_db = VectorDBManager()

        self.retrieval = RetrievalManager(
            vector_db=self.vector_db,
            embedding_service=self.embedding,
        )

        self.rag = RAGBuilder()


    async def run(
        self,
        runtime
    ):

        task = runtime.task


        # 1. Ingestion
        ingestion_metadata = create_metadata(
            document_id=task.taskId,
            source="workflow",
            stage="ingestion"
        )


        document = await self.ingestion.process(
            {
                "id": task.taskId,
                "content": task.input,
                "metadata": ingestion_metadata
            }
        )


        # 2. ETL
        etl_result = await self.etl.run(
            document
        )


        # 3. Loader
        loaded = etl_result


        # 4. Embedding
        embedding = self.embedding.embed(
            loaded["content"]
        )


        # 5. Vector metadata
        embedding_metadata = create_metadata(
            document_id=task.taskId,
            source="workflow",
            stage="embedding"
        )


        # 6. Vector item schema
        vector_item = VectorItem(
            id=task.taskId,
            embedding=embedding["vector"],
            content=loaded["content"],
            metadata=embedding_metadata
        )


        # 7. Store vector
        self.vector_db.insert(
            vector_item
        )


        # 8. Retrieval
        retrieved = self.retrieval.retrieve(
            loaded["content"]
        )

        # 9. RAG Context
        rag_context = self.rag.build(
            retrieved
        )


        # 10. Processing result
        runtime.processing = {
            "document": document,
            "etl": etl_result,
            "embedding": embedding,
            "retrieval": retrieved,
            "rag_context": rag_context,
        }


        return runtime
