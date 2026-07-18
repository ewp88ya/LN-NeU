import time
import uuid


class AuditLogger:


    def __init__(self):

        self.events = []



    def record(
        self,
        event_type,
        details
    ):

        event = {

            "event_id": str(
                uuid.uuid4()
            ),

            "type": event_type,

            "details": details,

            "timestamp": time.time()

        }


        self.events.append(
            event
        )


        return event



    def security_block(
        self,
        task_id,
        reason
    ):

        return self.record(
            "security_block",
            {
                "task_id": task_id,
                "reason": reason
            }
        )



    def agent_denied(
        self,
        agent,
        reason
    ):

        return self.record(
            "agent_denied",
            {
                "agent": agent,
                "reason": reason
            }
        )



    def tool_denied(
        self,
        agent,
        tool
    ):

        return self.record(
            "tool_denied",
            {
                "agent": agent,
                "tool": tool
            }
        )



    def snapshot(self):

        return self.events
