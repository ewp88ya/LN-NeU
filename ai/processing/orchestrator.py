from processing.ingestion import DataIngestionPipeline
from processing.etl import ETLPipeline
from processing.loader import LoaderManager
from processing.embedding import EmbeddingService
from processing.vector_db import VectorDBManager
from processing.retrieval import RetrievalManager


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


    async def run(self, runtime):

        task = runtime.task

        document = await self.ingestion.process(
            {
                "id": task.taskId,
                "content": task.input,
                "metadata": {
                    "source": "workflow"
                }
            }
        )

        etl_result = await self.etl.run(
            document
        )

        loaded = etl_result

        embedding = self.embedding.embed(
            loaded["content"]
        )

        self.vector_db.insert(
            {
                "embedding": embedding,
                "content": loaded["content"]
            }
        )

        runtime.processing = {
            "document": document,
            "etl": etl_result,
            "loaded": loaded,
            "embedding": embedding,
        }

        return runtime
