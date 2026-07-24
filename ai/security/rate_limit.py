import time


class RateLimiter:


    def __init__(
        self,
        limit=10,
        window=60
    ):

        self.limit = limit

        self.window = window

        self.requests = {}



    def allow(
        self,
        key="default"
    ):

        now = time.time()


        if key not in self.requests:

            self.requests[key] = []


        # remove expired requests

        self.requests[key] = [

            timestamp

            for timestamp in self.requests[key]

            if now - timestamp < self.window

        ]


        if len(self.requests[key]) >= self.limit:

            return False


        self.requests[key].append(
            now
        )


        return True



    def check(
        self,
        key="default"
    ):

        return self.allow(
            key
        )



    def reset(
        self,
        key=None
    ):

        if key:

            self.requests.pop(
                key,
                None
            )

        else:

            self.requests.clear()
