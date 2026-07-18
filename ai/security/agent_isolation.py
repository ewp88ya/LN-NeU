from agents.core.permission import AgentPermissionBoundary


class AgentIsolation:


    def __init__(self):

        self.boundary = AgentPermissionBoundary()



    def validate(
        self,
        agent_name,
        task
    ):

        return self.boundary.can_execute(
            agent_name,
            task.action
        )
