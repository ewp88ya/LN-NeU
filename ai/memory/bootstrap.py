from .manager import MemoryManager
from .persistent_adapter import PersistentMemoryAdapter
from .short_term import ShortTermMemory
from .conversation import ConversationMemory
from .long_term import LongTermMemory

def create_memory_manager():

    manager = MemoryManager()

    manager.register(
        "persistent",
        PersistentMemoryAdapter()
    )

    manager.register(
        "short_term",
        ShortTermMemory()
    )

    manager.register(
        "conversation",
        ConversationMemory()
    )

    manager.register(
         "long_term",
         LongTermMemory()
    )
    return manager
