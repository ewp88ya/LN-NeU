class ToolSelector:


    def select(
        self,
        task
    ):

        action = task.action.lower()


        if action in [
            "network",
            "analysis"
        ]:

            return [

                "ping_server",

                "dns_lookup",

                "http_check"

            ]


        if action == "ping":

            return [

                "ping_server"

            ]


        return []
