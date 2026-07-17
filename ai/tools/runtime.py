from tools.registry import ToolRegistry
from tools.permission import ToolPermission


class ToolRuntime:

    def __init__(self):

        self.registry = ToolRegistry()

        self.permission = ToolPermission()


    async def execute(

        self,

        agent_name,
        tool_name,

        **kwargs

    ):

        if not self.permission.allowed(
            agent_name,
            tool_name
        ):

            raise PermissionError(
                f"{agent_name} cannot use {tool_name}"
            )


        tool = self.registry.get(
            tool_name
        )

        if tool is None:

            raise ValueError(
                f"Tool '{tool_name}' not found."
            )


        return await tool.execute(
            **kwargs
        )
