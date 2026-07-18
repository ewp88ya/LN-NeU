import time
import uuid
import json


class AILogger:


    def __init__(self):

        self.logs = []


    def start(
        self,
        task_id,
        action
    ):

        execution_id = str(
            uuid.uuid4()
        )

        log = {

            "execution_id": execution_id,

            "task_id": task_id,

            "action": action,

            "status": "started",

            "started_at": time.time(),

            "finished_at": None,

            "duration": None,

            "agents": []

        }


        self.logs.append(log)


        return log



    def add_agent(
        self,
        log,
        agent,
        result
    ):

        log["agents"].append(

            {

                "agent": agent,

                "result": result,

                "timestamp": time.time()

            }

        )



    def finish(
        self,
        log,
        results
    ):

        finished = time.time()


        log["status"] = "completed"

        log["finished_at"] = finished

        log["duration"] = (

            finished -
            log["started_at"]

        )


        log["agents"] = results


        return log



    def error(
        self,
        task_id,
        error
    ):

        log = {

            "execution_id": str(
                uuid.uuid4()
            ),

            "task_id": task_id,

            "status": "failed",

            "error": str(error),

            "timestamp": time.time()

        }


        self.logs.append(log)


        return log



    def export(self):

        return json.dumps(
            self.logs,
            indent=2
        )
