from tools.registry import ToolRegistry
from tools.permission import ToolPermission
from security.authorization import Authorization

class ToolRuntime:


    def __init__(
        self,
        metrics=None,
        audit=None
    ):


        self.registry = ToolRegistry()

        self.permission = ToolPermission()

        self.authorization = Authorization()

        self.metrics = metrics
        self.audit = audit


    async def execute_all(
        self,
        tools,
        *args,
        **kwargs
    ):


        results = []



        #
        # Support:
        #
        # "ping_server"
        #
        # atau
        #
        # [
        #   "ping_server",
        #   "dns_lookup"
        # ]
        #

        if isinstance(
            tools,
            str
        ):

            tools = [
                tools
            ]



        for tool_name in tools:


            result = await self.execute(
                tool_name,
                *args,
                **kwargs
            )


            results.append(
                result
            )



        return results



    async def execute(
        self,
        tool_name,
        agent_name=None,
        role="agent",
        *args,
        **kwargs
    ):


        tool = self.registry.get(
            tool_name
        )

        if not self.authorization.allowed(
            role,
            "execute_tool"
        ):

            if self.audit:

                self.audit.record(
                    "tool_execution_denied",
                    {
                         "reason": "authorization_failed",
                         "tool": tool_name,
                         "role": role
                    }
                )


            return {

                "status": "denied",

                "tool": tool_name,

                "reason": "authorization_failed"

            }

        if agent_name:

           if not self.permission.allowed(
               agent_name,
               tool_name
           ):

               if self.audit:

                  self.audit.record(
                      "tool_execution_denied",
                      {
                          "agent": agent_name,
                          "tool": tool_name
                      }
                  )


               return {

                   "status": "denied",

                   "tool": tool_name,

                   "reason": "permission denied"

               }


        if not tool:


            raise ValueError(
                f"Tool '{tool_name}' not found"
            )



        #
        # Metrics
        #

        if self.metrics:


            self.metrics.tool_used()



        #
        # Audit Start
        #

        if self.audit:


            self.audit.record(

                "tool_execution_started",

                {

                    "tool": tool_name

                }

            )



        try:



            result = await tool.execute(
                *args,
                **kwargs
            )



            #
            # Audit Success
            #

            if self.audit:


                self.audit.record(

                    "tool_execution_completed",

                    {

                        "tool": tool_name,

                        "status": "success"

                    }

                )



            return {


                "status": "success",


                "tool": tool_name,


                "result": result


            }




        except Exception as error:



            #
            # Metrics Failed
            #

            if self.metrics:


                self.metrics.tool_failed()



            #
            # Audit Failed
            #

            if self.audit:


                self.audit.record(

                    "tool_execution_failed",

                    {

                        "tool": tool_name,

                        "error": repr(error)

                    }

                )



            return {


                "status": "failed",


                "tool": tool_name,


                "error": repr(error)


            }
