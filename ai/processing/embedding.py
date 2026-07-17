class EmbeddingPreparation:

    def prepare(
        self,
        chunks
    ):

        embeddings = []

        for index, chunk in enumerate(chunks):

            embeddings.append({

                "id": index,
                "text": chunk

            })

        return embeddings
