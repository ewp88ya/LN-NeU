import time
import uuid

from collections import deque


class TraceSpan:


    def __init__(
        self,
        task_id,
        action
    ):

        self.trace_id = str(
            uuid.uuid4()
        )

        self.task_id = task_id

        self.action = action

        self.started_at = time.time()

        self.finished_at = None



    def finish(self):

        self.finished_at = time.time()


        return (
            self.finished_at
            -
            self.started_at
        )



    def snapshot(self):

        return {

            "trace_id":
                self.trace_id,

            "task_id":
                self.task_id,

            "action":
                self.action,

            "started_at":
                self.started_at,

            "finished_at":
                self.finished_at

        }



class TraceManager:



    def __init__(self):

        self.traces = deque(
            maxlen=1000
        )


    def start(
        self,
        task_id,
        action
    ):


        trace = TraceSpan(
            task_id,
            action
        )


        self.traces.append(
            trace
        )


        return trace



    def active(self):

        return len(
            self.traces
        )



    def snapshot(self):

        return [

            trace.snapshot()

            for trace in self.traces

        ]
