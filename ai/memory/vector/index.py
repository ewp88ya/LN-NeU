import math

from memory.vector.schema import SearchResult



class VectorIndex:


    def similarity(
        self,
        query:str,
        text:str
    ):


        query_words = set(
            query.lower().split()
        )


        text_words = set(
            text.lower().split()
        )


        if not query_words:

            return 0



        intersection = len(
            query_words &
            text_words
        )


        union = len(
            query_words |
            text_words
        )


        return intersection / union



    def search(

        self,

        query,

        documents,

        top_k=5

    ):


        results=[]


        for doc in documents:


            score = self.similarity(

                query,

                doc.text

            )


            results.append(

                SearchResult(

                    id=doc.id,

                    text=doc.text,

                    score=score,

                    metadata=doc.metadata

                )

            )


        results.sort(

            key=lambda x:x.score,

            reverse=True

        )


        return results[:top_k]
