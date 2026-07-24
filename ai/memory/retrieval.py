class MemoryRetrieval:


    def __init__(
        self,
        memory_manager
    ):

        self.memory_manager = memory_manager



    def retrieve_context(
        self,
        task=None,
        task_id=None,
        query=None
    ):

        context = []


        try:

            if task:

                task_id = getattr(
                    task,
                    "taskId",
                    None
                )

                query = getattr(
                    task,
                    "input",
                    None
                )


            if self.memory_manager:

                if hasattr(
                    self.memory_manager,
                    "search"
                ):

                    result = self.memory_manager.search(
                        query
                    )

                    if result:

                        context = result


        except Exception:

            context = []



        return {

            "task_id": task_id,

            "query": query,

            "context": context

        }



    def retrieve(
        self,
        task=None
    ):

        return self.retrieve_context(
            task=task
        )
