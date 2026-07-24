from memory.retrieval.retriever import MemoryRetriever


class MemoryRetrieval:


    def __init__(
        self,
        memory_manager
    ):

        self.manager = memory_manager


        vector_store = self.manager.get(
            "vector"
        )


        self.retriever = MemoryRetriever(
            vector_store
        )



    def retrieve_context(

        self,

        task_id,

        query

    ):


        return self.retriever.retrieve_context(

            task_id,

            query

        )



    def retrieve(

        self,

        task

    ):


        return self.retriever.retrieve(

            task.input

        )
