import os


class SecretManager:


    def __init__(self):

        self.cache = {}



    def get(
        self,
        key,
        default=None
    ):

        if key in self.cache:

            return self.cache[key]


        value = os.getenv(
            key,
            default
        )


        self.cache[key] = value


        return value


    def exists(
        self,
        key
    ):

        return self.get(
            key
        ) is not None



    def required(
         self,
         key
    ):

        value = self.get(
           key
        )

        if value is None:

            raise RuntimeError(
                f"Required secret '{key}' not found"
            )

        return value



    def clear(
        self
    ):

        self.cache.clear()

