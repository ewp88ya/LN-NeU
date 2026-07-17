from .interface import MemoryInterface
from .persistent import PersistentMemory


class PersistentMemoryAdapter(MemoryInterface):

    def __init__(self):
        self.memory = PersistentMemory()


    def save(
        self,
        key,
        value,
        metadata=None
    ):
        return self.memory.store(
            task_id=key,
            action=metadata.get("action") if metadata else "memory",
            input_text=value.get("input") if isinstance(value, dict) else str(value),
            response=value.get("response") if isinstance(value, dict) else str(value)
        )


    def retrieve(
        self,
        query,
        limit=5
    ):
        return self.memory.retrieve_context(query)


    def delete(
        self,
        key
    ):
        # PersistentMemory saat ini belum menyediakan delete.
        # Akan ditambahkan saat database layer upgrade.
        raise NotImplementedError(
            "Delete operation is not implemented yet"
        )
