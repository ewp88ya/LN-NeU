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

        runtime.processing = {
            "document": document
        }

        return runtime
