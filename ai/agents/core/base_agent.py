from abc import ABC, abstractmethod

from contracts.agent_contract import (
    AgentTask,
    AgentResult,
)


class BaseAgent(ABC):

    name = "base-agent"

    def __init__(self):

        self.runtime = None
        self.selector = None

    def get_memory(
        self,
        task: AgentTask
    ):

        return task.context or {}

    def get_shared_state(
        self,
        task: AgentTask
    ):

        return getattr(
            task,
            "shared_state",
            None
        )

    def save_state(
        self,
        task: AgentTask,
        key,
        value
    ):

        state = self.get_shared_state(task)

        if state:

            state.set(
                key,
                value
            )

    async def execute_tool(
        self,
        task: AgentTask,
        **kwargs
    ):

        if self.runtime is None:

            return None

        if self.selector is None:

            return None

        tool = self.selector.select(
            task
        )

        if tool is None:

            return None

        return await self.runtime.execute(
            self.name,
            tool,
            **kwargs
        )

    def success(
        self,
        output=None,
        metadata=None
    ):

        return AgentResult(

            agent=self.name,

            status="completed",

            output=output,

            metadata=metadata or {}

        )

    def failed(
        self,
        error,
        metadata=None
    ):

        return AgentResult(

            agent=self.name,

            status="failed",

            error=str(error),

            metadata=metadata or {}

        )

    @abstractmethod
    async def run(
        self,
        task: AgentTask
    ) -> AgentResult:

        pass
