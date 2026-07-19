class MemoryRetrieval:


    def __init__(
        self,
        memory_manager
    ):

        self.memory_manager = memory_manager



    def retrieve_context(
        self,
        task_id=None,
        query=None
    ):

        context = []


        try:

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



    # compatibility
    def retrieve(
        self,
        task_id=None,
        query=None
    ):

        return self.retrieve_context(
            task_id,
            query
        )
