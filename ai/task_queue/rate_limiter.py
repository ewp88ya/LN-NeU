import os
import redis


class RateLimiter:


    def __init__(
        self,
        url=None,
        redis_url=None
    ):


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



    def allow(
        self,
        key,
        limit,
        window
    ):


        redis_key = (
            f"rate-limit:{key}"
        )


        current = self.redis.get(
            redis_key
        )


        if current is None:


            self.redis.set(

                redis_key,

                1,

                ex=window

            )


            return True



        if int(current) >= limit:

            return False



        self.redis.incr(
            redis_key
        )


        return True



    def remaining(
        self,
        key,
        limit
    ):


        redis_key = (
            f"rate-limit:{key}"
        )


        current = self.redis.get(
            redis_key
        )


        if current is None:

            return limit


        return max(

            limit - int(current),

            0

        )



    def reset(
        self,
        key
    ):

        self.redis.delete(

            f"rate-limit:{key}"

        )
