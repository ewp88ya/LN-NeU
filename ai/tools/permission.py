class ToolPermission:

    def __init__(self):

        self.permissions = {

            "analysis-agent": [
                "ping_server"
            ],

            "network-agent": [
                "ping_server"
            ],

            "optimizer-agent": [
                "ping_server"
            ]
        }

    def allowed(
        self,
        agent_name,
        tool_name
    ):

        return tool_name in self.permissions.get(
            agent_name,
            []
        )
