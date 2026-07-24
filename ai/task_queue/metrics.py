import time
import redis


class QueueMetrics:

    def __init__(
        self,
        url=None,
        redis_url=None
    ):

        if redis_url:
            url = redis_url

        if url is None:
            import os

            url = os.getenv(
                "REDIS_URL",
                "redis://localhost:6379"
            )

        self.redis = redis.Redis.from_url(
            url,
            decode_responses=True
        )

        self.prefix = "ln-neu-metrics"


    def _key(
        self,
        name
    ):
        return f"{self.prefix}:{name}"


    def increment(
        self,
        metric,
        value=1
    ):

        self.redis.incrby(
            self._key(metric),
            value
        )


    def record_enqueue(self):

        self.increment(
            "queued"
        )


    def record_processed(self):

        self.increment(
            "processed"
        )


    def record_failed(self):

        self.increment(
            "failed"
        )


    def record_retry(self):

        self.increment(
            "retry"
        )


    def record_latency(
        self,
        seconds
    ):

        self.redis.set(
            self._key("last_latency"),
            seconds
        )


    def stats(self):

        metrics = [
            "queued",
            "processed",
            "failed",
            "retry",
            "last_latency"
        ]

        result = {}

        for metric in metrics:

            value = self.redis.get(
                self._key(metric)
            )

            if value is None:
                value = 0

            result[metric] = float(value)


        return result


    def clear(self):

        keys = self.redis.keys(
            f"{self.prefix}:*"
        )

        if keys:
            self.redis.delete(
                *keys
            )
