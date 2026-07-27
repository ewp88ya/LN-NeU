from .context import RAGContext


class RAGBuilder:


    def __init__(
        self,
        max_length=4000
    ):

        self.context = RAGContext(
            max_length
        )


    def build(
        self,
        retrieval_result
    ):

        return self.context.build(
            retrieval_result
        )
