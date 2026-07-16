import time


class AILogger:

    def start(self, task_id, action):

        return {
            "taskId": task_id,
            "action": action,
            "start": time.time()
        }


    def finish(self, log, result):

        duration = (
            time.time()
            - log["start"]
        )

        return {
            "taskId": log["taskId"],
            "action": log["action"],
            "duration_ms": round(
                duration * 1000,
                2
            ),
            "status": "success",
            "result": result
        }
