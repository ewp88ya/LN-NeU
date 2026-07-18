class FailedWorkflow:


    async def execute(
        self,
        task
    ):

        return {
            "status": "failed",
            "task_id": task.taskId,
            "error": "forced failure for DLQ test"
        }
