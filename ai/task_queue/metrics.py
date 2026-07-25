import os
import redis


class QueueMetrics:


    def __init__(
        self,
        redis_url=None
    ):


        redis_url = (
            redis_url
            or os.getenv(
                "REDIS_URL",
                "redis://localhost:6379"
            )
        )


        self.redis = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )


        self.prefix = "ln-neu-metrics"



    def _key(
        self,
        name
    ):

        return f"{self.prefix}:{name}"



    # =========================
    # Increment Metrics
    # =========================


    def increment(
        self,
        metric,
        value=1
    ):

        self.redis.incrby(
            self._key(metric),
            value
        )



    # =========================
    # Queue Events
    # =========================


    def record_enqueue(
        self
    ):

        self.increment(
            "queued"
        )



    def record_processed(
        self
    ):

        self.increment(
            "processed"
        )



    def record_failed(
        self
    ):

        self.increment(
            "failed"
        )



    def record_retry(
        self
    ):

        self.increment(
            "retry"
        )



    def record_latency(
        self,
        seconds
    ):

        self.redis.set(
            self._key(
                "last_latency"
            ),
            seconds
        )



    # =========================
    # Dashboard Snapshot
    # =========================


    def stats(
        self
    ):


        try:

            result = {}


            for key in [

                "queued",

                "processed",

                "failed",

                "retry",

                "last_latency"

            ]:


                value = self.redis.get(
                    self._key(key)
                )


                result[key] = float(
                    value or 0
                )


            result["redis"] = "online"


            return result



        except Exception:


            return {

                "queued": 0.0,

                "processed": 0.0,

                "failed": 0.0,

                "retry": 0.0,

                "last_latency": 0.0,

                "redis": "offline"

            }



    # =========================
    # Cleanup
    # =========================


    def clear(
        self
    ):


        keys = self.redis.keys(
            f"{self.prefix}:*"
        )


        if keys:

            self.redis.delete(
                *keys
            )
