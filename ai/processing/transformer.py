class DataTransformer:

    def transform(self, data):

        transformed = data.copy()

        transformed["normalized_input"] = (
            data["input"]
            .strip()
            .lower()
        )

        transformed["word_count"] = len(
            transformed["normalized_input"].split()
        )

        return transformed
