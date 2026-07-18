class ErrorHandler:

    def handle(self, task, error):

        return {
            "status": "failed",
            "task_id": task.taskId,
            "error": str(error)
        }
