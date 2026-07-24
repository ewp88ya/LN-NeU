from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult,
)


class NetworkAgent(BaseAgent):

    name = "network-agent"


    def __init__(
        self,
        selector=None,
        runtime=None,
    ):

        super().__init__()

        self.selector = selector

        self.runtime = runtime



    async def run(
        self,
        task: AgentTask,
    ) -> AgentResult:


        try:


            if (
                self.selector is None
                or self.runtime is None
            ):

                return self.failed(

                    "Network runtime not configured",

                    metadata={

                        "task_id": getattr(
                            task,
                            "taskId",
                            None
                        ),

                        "agent": self.name

                    }

                )



            #
            # Dynamic Multiple Tool Selection
            #

            tools = self.selector.select(
                task
            )


            if not tools:

                return self.failed(

                    "No tools selected",

                    metadata={

                        "agent": self.name

                    }

                )



            #
            # Normalize Input
            #

            if isinstance(
                task.input,
                dict
            ):

                host = (

                    task.input.get("host")

                    or task.input.get("text")

                    or task.input.get("message")

                    or "google.com"

                )

            else:

                host = str(
                    task.input
                )



            #
            # Execute Multiple Tools
            #

            results = await self.runtime.execute_all(

                self.name,

                tools,

                host=host

            )



            task_id = getattr(

                task,

                "taskId",

                getattr(
                    task,
                    "task_id",
                    None
                )

            )



            return self.success(

                output={

                    "tool_results": results

                },

                metadata={

                    "task_id": task_id,

                    "agent": self.name,

                    "tools": tools

                }

            )



        except Exception as error:


            task_id = getattr(

                task,

                "taskId",

                getattr(
                    task,
                    "task_id",
                    None
                )

            )


            return self.failed(

                error,

                metadata={

                    "task_id": task_id,

                    "agent": self.name

                }

            )
