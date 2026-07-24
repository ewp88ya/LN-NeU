class TextChunker:


    def __init__(
        self,
        chunk_size=500,
        overlap=50
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap



    def split(
        self,
        text
    ):

        if not text:

            return []



        words = text.split()


        chunks = []


        start = 0

        chunk_id = 0



        while start < len(words):


            end = start + self.chunk_size


            chunk_words = words[start:end]


            chunk_text = " ".join(
                chunk_words
            )



            chunks.append({

                "id": chunk_id,

                "text": chunk_text,

                "metadata": {

                    "start": start,

                    "end": end,

                    "size": len(chunk_words),

                    "overlap": self.overlap

                }

            })



            chunk_id += 1


            start = end - self.overlap



            if start < 0:

                start = 0



        return chunks
