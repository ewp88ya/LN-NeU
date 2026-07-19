from agents.core.base_agent import BaseAgent

from contracts.agent_contract import (
    AgentTask,
    AgentResult
)



class OptimizerAgent(BaseAgent):

    name = "optimizer-agent"



    async def run(
        self,
        task: AgentTask
    ) -> AgentResult:


        try:

            memory = self.get_memory(
                task
            )


            optimization = {

                "type": "optimization",

                "recommendation":
                    "Analyze bottleneck and apply optimization strategy",

                "context": memory

            }


            return self.success(

                output=optimization,

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
