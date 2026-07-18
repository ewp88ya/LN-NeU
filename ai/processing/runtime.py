import time


class RuntimeMetadata:


    def __init__(self):

        self.start_time = time.time()

        self.end_time = None


        self.data = {

            "execution_time": 0,

            "token_usage": {

                "input": 0,

                "output": 0

            },

            "tool_usage": [],

            "memory_usage": {},

            "planner_latency": 0,

            "agent_latency": {}

        }



    def start(self):

        self.start_time = time.time()



    def finish(self):

        self.end_time = time.time()

        self.data["execution_time"] = (
            self.end_time -
            self.start_time
        )



    def add_tool_usage(
        self,
        tool_name
    ):

        self.data["tool_usage"].append(
            tool_name
        )



    def set_memory_usage(
        self,
        usage
    ):

        self.data["memory_usage"] = usage



    def set_planner_latency(
        self,
        latency
    ):

        self.data["planner_latency"] = latency



    def set_agent_latency(
        self,
        agent,
        latency
    ):

        self.data["agent_latency"][agent] = latency



    def snapshot(self):

        return self.data
