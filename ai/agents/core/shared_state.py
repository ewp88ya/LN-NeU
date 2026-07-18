from typing import Dict, Any, List
import time


class SharedAgentState:
    """
    Shared runtime state between agents.

    All agents can read/write information
    during one workflow execution.
    """


    def __init__(self):

        self.data: Dict[str, Any] = {

            "context": {},

            "agents": {},

            "tools": {},

            "metrics": {},

            "events": []

        }


        self.created_at = time.time()



    def set(
        self,
        key: str,
        value: Any
    ):

        self.data[key] = value



    def get(
        self,
        key: str,
        default=None
    ):

        return self.data.get(
            key,
            default
        )



    def update_agent_result(
        self,
        agent_name: str,
        result: Dict[str, Any]
    ):

        self.data["agents"][agent_name] = result



    def add_tool_result(
        self,
        tool_name: str,
        result: Any
    ):

        self.data["tools"][tool_name] = result



    def add_event(
        self,
        event: Dict[str, Any]
    ):

        event["timestamp"] = time.time()

        self.data["events"].append(
            event
        )



    def snapshot(self):

        return {

            **self.data,

            "runtime": {

                "created_at": self.created_at,

                "age": time.time() - self.created_at

            }

        }
