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
        return self.stores.get(name)


    def save(
        self,
        memory_type,
        *args,
        **kwargs
    ):
        store = self.get(memory_type)

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
        store = self.get(memory_type)

        if not store:
            raise ValueError(
                f"Memory '{memory_type}' not registered"
            )

        return store.retrieve(
            *args,
            **kwargs
        )
