import time
import uuid


class AuditLogger:


    def __init__(self):

        self.events = []



    def record(
        self,
        event_type,
        details=None,
        severity="INFO",
        actor="system"
    ):


        event = {


            "event_id":

                str(
                    uuid.uuid4()
                ),



            "type":

                event_type,



            "severity":

                severity,



            "actor":

                actor,



            "details":

                details or {},



            "timestamp":

                time.time()

        }



        self.events.append(
            event
        )


        return event



    # =========================
    # Security Events
    # =========================


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

            },

            severity="WARNING"

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

            },

            severity="WARNING"

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

            },

            severity="WARNING"

        )



    # =========================
    # Runtime Events
    # =========================


    def task_event(
        self,
        task_id,
        status,
        metadata=None
    ):

        return self.record(

            "task_event",

            {

                "task_id": task_id,

                "status": status,

                "metadata": metadata or {}

            }

        )



    def tool_execution(
        self,
        agent,
        tool,
        status
    ):

        return self.record(

            "tool_execution",

            {

                "agent": agent,

                "tool": tool,

                "status": status

            }

        )



    def snapshot(
        self
    ):

        return self.events
