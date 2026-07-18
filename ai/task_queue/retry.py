from datetime import datetime


class RetryPolicy:


    def __init__(
        self,
        max_retry=3
    ):

        self.max_retry = max_retry



    def should_retry(
        self,
        task
    ):

        retry_count = task.get(
            "retry_count",
            0
        )

        return retry_count < self.max_retry



    def increase_retry(
        self,
        task
    ):

        task["retry_count"] = (
            task.get(
                "retry_count",
                0
            ) + 1
        )

        task["last_retry"] = (
            datetime.utcnow().isoformat()
        )

        return task
