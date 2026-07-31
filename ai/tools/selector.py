class ToolSelector:


    def select(
        self,
        task
    ):

        action = task.action.lower()


        #
        # Network operations
        #

        if action in [
            "network",
            "network_scan",
            "ping",
            "dns_lookup",
            "http_check"
        ]:

            return [

                "ping_server",

                "dns_lookup",

                "http_check"

            ]


        #
        # Analysis operations
        #

        if action in [
            "analysis",
            "analyze"
        ]:

            return [

                "ping_server",

                "dns_lookup"

            ]


        return []
