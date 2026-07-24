from tools.registry import ToolRegistry
from tools.permission import ToolPermission


class ToolRuntime:


    def __init__(self):

        self.registry = ToolRegistry()

        self.permission = ToolPermission()

        self._register_default_tools()



    def _register_default_tools(self):

        from tools.network_tool import PingTool
        from tools.dns_tool import DNSTool
        from tools.http_tool import HTTPTool


        self.registry.register(
            "ping_server",
            PingTool()
        )


        self.registry.register(
            "dns_lookup",
            DNSTool()
        )


        self.registry.register(
            "http_check",
            HTTPTool()
        )



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
                f"Tool {tool_name} not found"
            )


        return await tool.execute(
            **kwargs
        )



    async def execute_all(
        self,
        agent_name,
        tools,
        **kwargs
    ):

        results = []


        for tool_name in tools:

            try:

                result = await self.execute(
                    agent_name,
                    tool_name,
                    **kwargs
                )


                results.append(
                    {
                        "tool": tool_name,
                        "status": "success",
                        "result": result
                    }
                )


            except Exception as error:

                results.append(
                    {
                        "tool": tool_name,
                        "status": "failed",
                        "error": str(error)
                    }
                )


        return results
