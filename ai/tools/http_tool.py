import httpx

from tools.base import BaseTool



class HTTPTool(BaseTool):


    name = "http_check"



    async def run(
        self,
        host="https://google.com"
    ):


        if not host.startswith(
            "http"
        ):

            host = (
                "https://"
                +
                host
            )


        async with httpx.AsyncClient(
            timeout=5
        ) as client:


            response = await client.get(
                host
            )


            return {

                "url": host,

                "status_code":
                    response.status_code

            }
