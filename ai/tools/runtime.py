from tools.registry import ToolRegistry
from tools.permission import ToolPermission
from tools.contract import ToolResult


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

            return ToolResult(
                tool=tool_name,
                status="blocked",
                error=f"{agent_name} cannot use {tool_name}"
            )



        tool = self.registry.get(
            tool_name
        )


        if tool is None:

            return ToolResult(
                tool=tool_name,
                status="failed",
                error="Tool not found"
            )



        try:

            result = await tool.execute(
                **kwargs
            )


            return ToolResult(

                tool=tool_name,

                status="success",

                output=result

            )


        except Exception as error:


            return ToolResult(

                tool=tool_name,

                status="failed",

                error=str(error)

            )
