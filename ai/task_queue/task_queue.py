import json
import os
import redis


from observability.logger import (
    get_logger,
    log_event
)



class TaskQueue:


    def __init__(
        self,
        url=None,
        redis_url=None
    ):


        self.logger = get_logger(
            "task_queue"
        )


        url = (

            redis_url

            or url

            or os.getenv(
                "REDIS_URL",
                "redis://redis:6379"
            )

        )


        self.redis = redis.Redis.from_url(

            url,

            decode_responses=True

        )


        self.queue_name = (
            "ln-neu-task-queue"
        )



    def push(
        self,
        task
    ):


        if (

            isinstance(task, dict)

            and "task" in task

            and "retry_count" in task

        ):

            payload = task


        else:


            if hasattr(
                task,
                "model_dump"
            ):

                task_payload = (
                    task.model_dump()
                )


            elif isinstance(
                task,
                dict
            ):

                task_payload = task


            else:

                task_payload = (
                    task.__dict__
                )



            payload = {

                "task": task_payload,

                "retry_count": 0

            }



        self.redis.lpush(

            self.queue_name,

            json.dumps(payload)

        )


        log_event(

            self.logger,

            "INFO",

            "task queued",

            event="task_enqueue",

            service="task_queue",

            metadata={

                "queue": self.queue_name

            }

        )



    def pop(
        self
    ):


        item = self.redis.rpop(

            self.queue_name

        )


        if item:


            payload = json.loads(
                item
            )


            log_event(

                self.logger,

                "INFO",

                "task dequeued",

                event="task_pop",

                service="task_queue",

                metadata={

                    "queue": self.queue_name

                }

            )


            return payload



        return None




    def peek(
        self
    ):


        item = self.redis.lindex(

            self.queue_name,

            -1

        )


        if item:

            return json.loads(
                item
            )


        return None




    def clear(
        self
    ):


        self.redis.delete(

            self.queue_name

        )


        log_event(

            self.logger,

            "INFO",

            "queue cleared",

            event="queue_clear",

            service="task_queue"

        )




    def size(
        self
    ):


        return self.redis.llen(

            self.queue_name

        )




    def empty(
        self
    ):


        return self.size() == 0
