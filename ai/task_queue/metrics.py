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
                "redis://redis:6379"
            )
        )


        try:

            self.redis = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=1
            )


            self.redis.ping()

            self.redis_available = True


        except Exception:

            self.redis = None

            self.redis_available = False



        self.prefix = "ln-neu-metrics"

        self.local_metrics = {
            "queued": 0,
            "processed": 0,
            "failed": 0,
            "retry": 0,
            "recovery": 0,
            "dead_letter": 0,
        }



    # =========================
    # Key Builder
    # =========================

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


        if not self.redis_available:

           self.local_metrics[metric] = (
               self.local_metrics.get(metric, 0) + value
           )

           return

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



    # =========================
    # Reliability Events
    # =========================

    def record_recovery(
        self
    ):

        self.increment(
            "recovery"
        )



    def record_dead_letter(
        self
    ):

        self.increment(
            "dead_letter"
        )



    # =========================
    # Latency
    # =========================

    def record_latency(
        self,
        seconds
    ):


        if not self.redis_available:
            return


        self.redis.set(
            self._key(
                "last_latency"
            ),
            seconds
        )



    # =========================
    # Queue Depth
    # =========================

    def record_queue_depth(
        self,
        size
    ):


        if not self.redis_available:
            return


        self.redis.set(
            self._key(
                "queue_depth"
            ),
            size
        )



    # =========================
    # Dashboard Snapshot
    # =========================

    def stats(
        self
    ):


        default = {

            "queued": 0.0,

            "processed": 0.0,

            "failed": 0.0,

            "retry": 0.0,

            "recovery": 0.0,

            "dead_letter": 0.0,

            "queue_depth": 0.0,

            "last_latency": 0.0,

            "redis": "offline"

        }



        if not self.redis_available:

            return default



        try:


            metrics = [

                "queued",

                "processed",

                "failed",

                "retry",

                "recovery",

                "dead_letter",

                "queue_depth",

                "last_latency"

            ]


            result = {}


            for metric in metrics:


                value = self.redis.get(
                    self._key(metric)
                )


                result[metric] = float(
                    value or 0
                )



            result["redis"] = "online"


            return result



        except Exception:


            return default



    # =========================
    # Cleanup
    # =========================

    def clear(
        self
    ):


        if not self.redis_available:

            return



        keys = self.redis.keys(
            f"{self.prefix}:*"
        )



        if keys:

            self.redis.delete(
                *keys
            )
