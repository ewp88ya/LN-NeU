from .manager import MemoryManager

from .persistent_adapter import PersistentMemoryAdapter
from .short_term import ShortTermMemory
from .conversation import ConversationMemory
from .long_term import LongTermMemory

from memory.vector.store import VectorStore


def create_memory_manager():

    manager = MemoryManager()


    # Persistent memory

    manager.register(
        "persistent",
        PersistentMemoryAdapter()
    )


    # Short term

    manager.register(
        "short_term",
        ShortTermMemory()
    )


    # Conversation

    manager.register(
        "conversation",
        ConversationMemory()
    )


    # Long term

    manager.register(
        "long_term",
        LongTermMemory()
    )


    # Vector Memory

    manager.register(
        "vector",
        VectorStore()
    )


    return manager
