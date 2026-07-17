class AgentIsolation:

    def __init__(self):

        self.permissions = {
            "analysis-agent": [
                "analysis"
            ],
            "network-agent": [
                "network"
            ],
            "optimizer-agent": [
                "optimization"
            ]
        }

    def validate(self, agent_name, task):

        allowed = self.permissions.get(
            agent_name,
            []
        )

        return task.action in allowed
