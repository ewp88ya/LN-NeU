from providers.factory import get_provider


class EmbeddingService:


    def __init__(self):

        self.provider = get_provider()



    async def create_embeddings(
        self,
        chunks
    ):

        results = []


        for index, chunk in enumerate(chunks):


            vector = await self.provider.embed(
                chunk
            )


            results.append({

                "id": index,

                "text": chunk,

                "embedding": vector

            })


        return results
