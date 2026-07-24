class ResultReranker:


    def rerank(
        self,
        results
    ):


        ranked = sorted(

            results,

            key=lambda x:
            x.score,

            reverse=True

        )


        return ranked
