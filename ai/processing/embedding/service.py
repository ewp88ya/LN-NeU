from .model import EmbeddingModel



class EmbeddingService:


    def __init__(
        self,
        model=None
    ):

        self.model = (
            model
            or EmbeddingModel()
        )



    def embed(
        self,
        text
    ):

        return self.model.encode(
            text
        )
