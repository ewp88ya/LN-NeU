from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult
)




class NetworkAgent(BaseAgent):


    name = "network-agent"



    def __init__(
        self,
        selector,
        runtime
    ):

        self.selector = selector

        self.runtime = runtime



    async def run(
        self,
        task: AgentTask
    ) -> AgentResult:


        try:

            tool_name = self.selector.select(
                task
            )


            result = await self.runtime.execute(

                self.name,

                tool_name,

                host=task.input

            )


            return self.success(

                output={

                    "tool": tool_name,

                    "result": result

                },

                metadata={

                    "task_id": task.task_id,

                    "agent": self.name

                }

            )


        except Exception as error:


            return self.failed(

                error,

                metadata={

                    "task_id": getattr(
                        task,
                        "task_id",
                        None
                    ),

                    "agent": self.name

                }

            )
