from typing import Dict, Any


class ResultAggregator:


    def aggregate(
        self,
        context
    ):

        agents = {}
        tools = {}
        metrics = {}


        for result in context.agent_results:

            if not isinstance(result, dict):
                continue


            agent_name = result.get(
                "agent",
                "unknown"
            )


            agents[agent_name] = result


            if "tool" in result:

                tools[agent_name] = {
                    "tool": result.get("tool"),
                    "result": result.get("result")
                }


        if hasattr(
            context,
            "runtime"
        ):

            metrics = context.runtime.snapshot()


        aggregated = {

            "summary": {

                "status": "completed",

                "total_agents": len(
                    agents
                ),

                "total_tools": len(
                    tools
                )

            },


            "agents": agents,


            "tools": tools,


            "metrics": metrics

        }


        context.metadata[
            "aggregated_result"
        ] = aggregated


        return context
