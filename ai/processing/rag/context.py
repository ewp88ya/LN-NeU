class RAGContext:


    def __init__(
        self,
        max_length=4000
    ):
        self.max_length = max_length


    def build(
        self,
        documents
    ):

        context_parts = []
        sources = []

        current_length = 0


        for item in documents:

            content = item.get(
                "content",
                ""
            )

            metadata = item.get(
                "metadata",
                {}
            )


            if current_length + len(content) > self.max_length:
                break


            context_parts.append(
                content
            )

            sources.append(
                metadata
            )

            current_length += len(content)


        return {
            "context": "\n\n".join(
                context_parts
            ),
            "sources": sources,
            "document_count": len(
                context_parts
            )
        }
