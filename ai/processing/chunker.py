class TextChunker:

    def __init__(
        self,
        chunk_size=500
    ):
        self.chunk_size = chunk_size


    def split(
        self,
        text: str
    ):

        return [

            text[i:i+self.chunk_size]

            for i in range(
                0,
                len(text),
                self.chunk_size
            )

        ]
