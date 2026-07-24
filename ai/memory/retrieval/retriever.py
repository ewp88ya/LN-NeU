from memory.vector.store import VectorStore

from memory.retrieval.reranker import ResultReranker

from memory.retrieval.context_builder import ContextBuilder



class MemoryRetriever:


    def __init__(
        self,
        vector_store=None
    ):


        self.vector = (

            vector_store

            or

            VectorStore()

        )


        self.reranker = ResultReranker()


        self.builder = ContextBuilder()



    def retrieve(

        self,

        query: str,

        top_k=5,

        metadata_filter=None

    ):


        results = self.vector.search(

            query,

            top_k

        )



        if metadata_filter:


            filtered = []


            for item in results:


                match = True


                for key, value in metadata_filter.items():


                    if item.metadata.get(key) != value:

                        match = False


                if match:

                    filtered.append(item)



            results = filtered



        ranked = self.reranker.rerank(

            results

        )


        return self.builder.build(

            ranked,

            top_k

        )



    # ==================================================
    # Compatibility API
    # Used by Processing InputStage
    # ==================================================

    def retrieve_context(

        self,

        task_id: str,

        query: str,

        top_k=5

    ):


        context = self.retrieve(

            query,

            top_k

        )


        return {


            "task_id":

                task_id,


            "query":

                query,


            "results":

                context,


            "source":

                "memory_retrieval"


        }
