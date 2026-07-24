import socket

from tools.base import BaseTool



class DNSTool(BaseTool):


    name = "dns_lookup"



    async def run(
        self,
        host="google.com"
    ):


        try:

            ip = socket.gethostbyname(
                host
            )


            return {

                "host": host,

                "ip": ip

            }


        except Exception as error:


            return {

                "error": str(error)

            }
