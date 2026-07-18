from abc import ABC, abstractmethod


class BaseAgent(ABC):


    name = "base-agent"



    def get_memory(
        self,
        task
    ):

        return getattr(
            task,
            "context",
            {}
        )



    def get_shared_state(
        self,
        task
    ):

        return getattr(
            task,
            "shared_state",
            None
        )



    def save_state(
        self,
        task,
        key,
        value
    ):

        state = self.get_shared_state(
            task
        )

        if state:

            state.set(
                key,
                value
            )



    @abstractmethod
    async def run(
        self,
        task
    ):

        pass
