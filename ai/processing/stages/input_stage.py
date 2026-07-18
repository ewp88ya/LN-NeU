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

    def run(
        self,
        runtime
    ):

        task = runtime.task

        runtime.processed = self.processor.process(
            task
        )

        task = runtime.processed

        security = self.prompt_guard.inspect(
            task.input
        )

        if not security["allowed"]:

            raise PermissionError(
                security["reason"]
            )

        runtime.memory = self.memory_retrieval.retrieve_context(
            task.taskId,
            task.input
        )

        task.context = runtime.memory

        self.memory.save(
            task.taskId,
            task
        )

        runtime.task = task

        return runtime
