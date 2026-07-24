class DataNormalizer:


    def normalize(
        self,
        data
    ):

        if data is None:
            return ""


        if isinstance(data, dict):

            return {
                key: self.normalize(value)
                for key, value in data.items()
            }


        if isinstance(data, str):

            return data.strip()


        return data
