from providers.embedding_factory import (
    get_embedding_provider
)



class EmbeddingPreparation:


    def __init__(self):

        self.provider = get_embedding_provider()



    async def prepare(
        self,
        chunks
    ):


        embeddings = []


        for chunk in chunks:


            text = (
                chunk["text"]
                if isinstance(
                    chunk,
                    dict
                )
                else chunk
            )


            vector = await self.provider.embed(
                text
            )


            embeddings.append({

                "id":
                    chunk.get("id", len(embeddings))
                    if isinstance(chunk, dict)
                    else len(embeddings),


                "text": text,


                "vector": vector,


                "metadata":
                    chunk.get(
                        "metadata",
                        {}
                    )
                    if isinstance(chunk, dict)
                    else {}

            })


        return embeddings
