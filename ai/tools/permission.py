class ToolPermission:


    def __init__(self):

        self.permissions = {

            "network": [
                "ping_server",
                "dns_lookup",
                "http_check"
            ],


            "analysis": [
                "ping_server",
                "dns_lookup"
            ],


            "optimizer": [
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
