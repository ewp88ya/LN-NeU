class EmbeddingModel:


    def __init__(
        self,
        model_name="default"
    ):

        self.model_name = model_name



    def encode(
        self,
        text
    ):

        # placeholder embedding engine
        return {
            "model": self.model_name,
            "vector": [
                float(ord(c))
                for c in text[:10]
            ]
        }
