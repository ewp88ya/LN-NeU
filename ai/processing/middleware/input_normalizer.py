class InputNormalizer:

    def normalize(self, task):

        task.action = task.action.lower().strip()

        if isinstance(task.input, str):
            task.input = task.input.strip()

        return task
