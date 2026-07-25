import os
import time
import httpx


class HealthMonitor:


    def __init__(self):

        self.services = {

            "ai": os.getenv(
                "AI_HEALTH_URL",
                None
            ),

            "worker": os.getenv(
                "WORKER_HEALTH_URL",
                None
            )

        }



    def check_service(
        self,
        name,
        url
    ):


        if not url:

            return {

                "service": name,

                "status": "not_configured"

            }



        try:

            response = httpx.get(

                url,

                timeout=3

            )


            return {

                "service": name,

                "status":
                    "healthy"
                    if response.status_code == 200
                    else "unhealthy",

                "latency":
                    response.elapsed.total_seconds()

            }



        except Exception as error:


            return {

                "service": name,

                "status": "down",

                "error": str(error)

            }



    def check_all(self):


        result = {


            "timestamp":
                time.time(),


            "services": []

        }



        for name, url in self.services.items():


            result["services"].append(

                self.check_service(

                    name,

                    url

                )

            )


        return result
