class MemoryContext:

    def __init__(self):
        self.storage = {}

    def save(self, task_id, data):
        self.storage[task_id] = data

    def get(self, task_id):
        return self.storage.get(task_id)
