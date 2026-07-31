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


        self.redis = None
        self.redis_available = False


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

            "queue_depth": 0,

            "last_latency": 0,

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
    # Increment
    # =========================

    def increment(
        self,
        metric,
        value=1
    ):


        self.local_metrics[metric] = (
            self.local_metrics.get(metric, 0)
            + value
        )


        if not self.redis_available:

            return


        try:

            self.redis.incrby(
                self._key(metric),
                value
            )

        except Exception:

            self.redis_available = False



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
    # Reliability
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


        self.local_metrics["last_latency"] = seconds


        if not self.redis_available:

            return


        try:

            self.redis.set(
                self._key(
                    "last_latency"
                ),
                seconds
            )

        except Exception:

            self.redis_available = False



    # =========================
    # Queue Depth
    # =========================

    def record_queue_depth(
        self,
        size
    ):


        self.local_metrics["queue_depth"] = size


        if not self.redis_available:

            return


        try:

            self.redis.set(
                self._key(
                    "queue_depth"
                ),
                size
            )

        except Exception:

            self.redis_available = False



    # =========================
    # Safe Redis Read
    # =========================

    def _get_metric(
        self,
        metric
    ):


        if not self.redis_available:

            return self.local_metrics.get(
                metric,
                0
            )


        try:

            value = self.redis.get(
                self._key(metric)
            )


            if value is None:

                return self.local_metrics.get(
                    metric,
                    0
                )


            return float(value)


        except Exception:

            return self.local_metrics.get(
                metric,
                0
            )



    # =========================
    # Snapshot
    # =========================

    def stats(
        self
    ):


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

            result[metric] = float(
                self._get_metric(metric)
            )


        result["redis"] = (
            "online"
            if self.redis_available
            else "offline"
        )


        return result



    # =========================
    # Cleanup
    # =========================

    def clear(
        self
    ):


        for key in self.local_metrics:

            self.local_metrics[key] = 0



        if not self.redis_available:

            return



        try:

            keys = self.redis.keys(
                f"{self.prefix}:*"
            )


            if keys:

                self.redis.delete(
                    *keys
                )


        except Exception:

            self.redis_available = False
