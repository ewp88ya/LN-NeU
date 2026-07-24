class AgentDependencyGraph:


    def build(
        self,
        agents
    ):

        steps=[]


        for index, agent in enumerate(
            agents
        ):

            steps.append({

                "id": index + 1,

                "agent": agent,

                "depends_on":
                    []
                    if index == 0
                    else [index],

            })


        return steps
