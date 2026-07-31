from datetime import datetime, UTC
import time


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
            datetime.now(UTC).isoformat()
        )

        return task

    def backoff(
        self,
        task
    ):

        retry = task.get(
            "retry_count",
            0
        )

        return min(
            2 ** retry,
            30
        )
