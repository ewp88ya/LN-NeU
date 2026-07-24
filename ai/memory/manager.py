class MemoryManager:


    def __init__(self):

        self.stores = {}



    def register(
        self,
        name,
        store
    ):

        self.stores[name] = store



    def get(
        self,
        name
    ):

        return self.stores.get(
            name
        )



    def save(
        self,
        memory_type,
        *args,
        **kwargs
    ):

        store = self.get(
            memory_type
        )


        if not store:

            raise ValueError(
                f"Memory '{memory_type}' not registered"
            )


        return store.save(
            *args,
            **kwargs
        )



    def retrieve(
        self,
        memory_type,
        *args,
        **kwargs
    ):

        store = self.get(
            memory_type
        )


        if not store:

            raise ValueError(
                f"Memory '{memory_type}' not registered"
            )


        return store.retrieve(
            *args,
            **kwargs
        )



    def search(
        self,
        query,
        top_k=5
    ):

        vector = self.get(
            "vector"
        )


        if not vector:

            return []


        return vector.search(
            query,
            top_k
        )



    def stats(self):

        return {

            "memory_types":
                list(
                    self.stores.keys()
                ),

            "total":
                len(
                    self.stores
                )

        }
