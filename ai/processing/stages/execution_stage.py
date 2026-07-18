async def run(self, context):

    task = context.task

    task.shared_state = context.shared_state


    for agent_name in context.plan.agents:

        result = await self.agent_manager.execute(
            agent_name,
            task
        )


        context.add_agent_result(
            result
        )


    return context
