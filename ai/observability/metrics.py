import time


class MetricsCollector:


    def __init__(self):

        self.metrics = {

            "tasks_total": 0,

            "tasks_completed": 0,

            "tasks_failed": 0,

            "agents_executed": 0,

            "tools_used": 0,

            "total_execution_time": 0

        }



    def task_started(self):

        self.metrics["tasks_total"] += 1



    def task_completed(
        self,
        execution_time
    ):

        self.metrics["tasks_completed"] += 1

        self.metrics["total_execution_time"] += execution_time



    def task_failed(self):

        self.metrics["tasks_failed"] += 1



    def agent_used(self):

        self.metrics["agents_executed"] += 1



    def tool_used(self):

        self.metrics["tools_used"] += 1



    def average_execution_time(self):

        completed = self.metrics[
            "tasks_completed"
        ]

        if completed == 0:

            return 0


        return (
            self.metrics["total_execution_time"]
            /
            completed
        )



    def snapshot(self):

        return {

            **self.metrics,

            "average_execution_time":
                self.average_execution_time(),

            "timestamp":
                time.time()

        }
