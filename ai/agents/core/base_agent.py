from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name = "base-agent"


    def get_context(self, task):

        return getattr(
            task,
            "context",
            {}
        )


    def get_memory(self, task):

        context = self.get_context(task)

        return {
            "short_term": context.get(
                "short_term"
            ),
            "conversation": context.get(
                "conversation",
                []
            ),
            "long_term": context.get(
                "long_term",
                []
            ),
            "persistent": context.get(
                "persistent",
                []
            )
        }


    @abstractmethod
    async def run(self, task):
        pass
