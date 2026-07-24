from processing.normalizer import DataNormalizer
from processing.chunker import TextChunker


class InputStage:


    def __init__(
        self,
        processor,
        prompt_guard,
        memory_retrieval,
        memory
    ):

        self.processor = processor

        self.prompt_guard = prompt_guard

        self.memory_retrieval = memory_retrieval

        self.memory = memory


        # Sprint 15
        self.normalizer = DataNormalizer()

        self.chunker = TextChunker(
            chunk_size=500
        )



    def run(
        self,
        runtime
    ):


        task = runtime.task


        # =========================
        # Base Processing
        # =========================

        runtime.processed = self.processor.process(
            task
        )

        task = runtime.processed



        # =========================
        # Input Normalization
        # =========================

        normalized_input = self.normalizer.normalize(
            task.input
        )


        task.input = normalized_input



        # =========================
        # Validation
        # =========================

        if not task.input:

            raise ValueError(
                "Task input is empty"
            )



        # =========================
        # Chunking Pipeline
        # =========================

        if isinstance(
            task.input,
            str
        ):

            chunks = self.chunker.split(
                task.input
            )

        else:

            chunks = []



        # =========================
        # Security Check
        # =========================

        security = self.prompt_guard.inspect(
            task.input
        )


        if not security["allowed"]:

            raise PermissionError(
                security["reason"]
            )



        # =========================
        # Memory Retrieval
        # =========================

        runtime.memory = self.memory_retrieval.retrieve_context(

            task.taskId,

            task.input

        )



        # =========================
        # Processing Context Injection
        # =========================

        task.context = {

            "memory": runtime.memory,

            "processing": {

                "normalized": True,

                "chunks": chunks,

                "chunk_count": len(chunks)

            }

        }



        # =========================
        # Memory Save
        # =========================

        self.memory.save(

            task.taskId,

            task

        )



        runtime.task = task


        return runtime
