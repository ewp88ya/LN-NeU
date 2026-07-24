class ToolSelector:


    def select(
        self,
        task
    ):

        action = task.action.lower()


        mapping = {

            "analyze": "ping_server",

            "analysis": "ping_server",

            "network": "ping_server",

            "optimize": "ping_server"

        }


        return mapping.get(action)
