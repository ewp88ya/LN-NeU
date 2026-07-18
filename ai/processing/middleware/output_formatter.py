class OutputFormatter:

    def format(self, result):

        return {
            "status": result.get("status"),
            "task_id": result.get("task_id"),
            "workflow": result.get("workflow"),
            "agents": result.get("agents", [])
        }
