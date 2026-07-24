import time
from datetime import datetime


class HealthMonitor:


    def __init__(self):

        self.started_at = time.time()

        self.services = {

            "memory": "unknown",

            "security": "unknown",

            "tools": "unknown",

            "agents": "unknown",

            "processing": "unknown"

        }



    def register(
        self,
        service,
        status
    ):

        self.services[service] = status



    def healthy(self):

        return all(

            value == "healthy"

            for value in self.services.values()

            if value != "unknown"

        )



    def status(self):

        return {

            "status":
                "healthy"
                if self.healthy()
                else "degraded",

            "service":
                "LN-NeU",

            "uptime":
                time.time() - self.started_at,

            "started_at":
                datetime.fromtimestamp(
                    self.started_at
                ).isoformat(),

            "components":
                self.services,

            "timestamp":
                time.time()

        }



    def check(self):

        return self.status()
