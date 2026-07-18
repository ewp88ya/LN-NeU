class InputValidator:

    def validate(self, task):

        if not task.taskId:
            raise ValueError("taskId is required")

        if not task.action:
            raise ValueError("action is required")

        if not task.input:
            raise ValueError("input is required")

        return task
