from agents.core.base_agent import BaseAgent


class AgentRegistry:

    def __init__(self):
        self.agents = {}


    def register(self, agent: BaseAgent):
        self.agents[agent.name] = agent


    def get(self, name):
        return self.agents.get(name)


    def list(self):
        return list(self.agents.keys())
