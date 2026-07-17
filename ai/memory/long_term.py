from datetime import datetime


class LongTermMemory:

    def __init__(self):
        self.memories = {}


    def save(
        self,
        key: str,
        value,
        metadata=None
    ):

        self.memories[key] = {
            "value": value,
            "metadata": metadata or {},
            "created_at": datetime.utcnow()
        }


    def retrieve(
        self,
        key: str
    ):

        return self.memories.get(key)


    def search(
        self,
        keyword: str
    ):

        results = []

        for key, item in self.memories.items():

            if keyword.lower() in str(item).lower():
                results.append(item)

        return results


    def delete(
        self,
        key: str
    ):

        if key in self.memories:
            del self.memories[key]
