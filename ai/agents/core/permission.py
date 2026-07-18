from security.policy import SecurityPolicy


class AgentPermissionBoundary:


    def __init__(self):

        self.policy = SecurityPolicy()



    def can_use_tool(
        self,
        agent_name,
        tool_name
    ):

        return self.policy.allow_tool(
            agent_name,
            tool_name
        )



    def can_execute(
        self,
        agent_name,
        action
    ):

        return self.policy.allow_action(
            action,
            agent_name
        )



    def can_access(
        self,
        agent_name,
        capability
    ):

        return self.policy.allow_agent(
            agent_name,
            capability
        )
