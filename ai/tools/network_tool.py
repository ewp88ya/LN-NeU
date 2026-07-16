import subprocess

from tools.base import BaseTool


class PingTool(BaseTool):

    name = "ping_server"


    async def run(self, host="8.8.8.8"):

        result = subprocess.run(
            ["ping", "-c", "3", host],
            capture_output=True,
            text=True
        )

        return {
            "tool": self.name,
            "host": host,
            "output": result.stdout
        }
