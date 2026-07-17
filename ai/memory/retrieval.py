class MemoryRetrieval:

    def __init__(
        self,
        manager
    ):
        self.manager = manager


    def retrieve_context(
        self,
        task_id: str,
        query: str
    ):

        context = {
            "short_term": None,
            "conversation": [],
            "long_term": [],
            "persistent": []
        }


        short_term = self.manager.get(
            "short_term"
        )

        if short_term:
            context["short_term"] = (
                short_term.retrieve(task_id)
            )


        conversation = self.manager.get(
            "conversation"
        )

        if conversation:
            context["conversation"] = (
                conversation.retrieve(task_id)
            )


        long_term = self.manager.get(
            "long_term"
        )

        if long_term:
            context["long_term"] = (
                long_term.search(query)
            )


        persistent = self.manager.get(
            "persistent"
        )

        if persistent:
            context["persistent"] = (
                persistent.retrieve(query)
            )


        return context
