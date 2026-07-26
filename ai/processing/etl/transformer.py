class Transformer:


    def transform(
        self,
        data: dict
    ) -> dict:

        return {
            "id": data["id"],
            "content": data["content"],
            "metadata": data.get(
                "metadata",
                {}
            ),
            "processed": True
        }
