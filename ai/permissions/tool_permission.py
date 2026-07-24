class ToolPermission:


    def __init__(self):

        self.rules = {

            "network-agent": [
                "ping",
                "network_check"
            ],

            "analysis-agent": [
                "analyze"
            ],

            "optimizer-agent": [
                "optimize"
            ]

        }



    def allowed(
        self,
        agent,
        tool
    ):

        permissions = self.rules.get(
            agent,
            []
        )


        return tool in permissions
