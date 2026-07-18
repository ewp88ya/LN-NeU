from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class QueueTask(BaseModel):

    model_config = ConfigDict(
        extra="allow"
    )


    # ======================
    # Queue Payload
    # ======================

    taskId: str

    action: str

    input: Any


    # ======================
    # Workflow Runtime State
    # ======================

    context: Optional[Any] = None

    plan: Optional[Any] = None


    # ======================
    # Metadata
    # ======================

    metadata: dict = {}



class TaskAdapter:


    def convert(
        self,
        payload: dict
    ):

        return QueueTask(

            taskId=payload.get(
                "taskId"
            ),

            action=payload.get(
                "action"
            ),

            input=payload.get(
                "input"
            ),

            metadata=payload.get(
                "metadata",
                {}
            )
        )
