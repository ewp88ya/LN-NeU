class DataParser:

    def parse(self, task):

        return {
            "taskId": task.taskId,
            "action": task.action,
            "input": task.input,
            "metadata": {
                "length": len(task.input),
                "type": "text"
            }
        }
