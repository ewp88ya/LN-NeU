from tools.network_tool import PingTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "ping_server": PingTool()
        }


    def get(self, name):

        return self.tools.get(name)


    def list(self):

        return list(self.tools.keys())
