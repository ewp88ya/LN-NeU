from typing import Any
from agents.core.shared_state import SharedAgentState

class TaskContext:

    def __init__(self, task):

        self.task = task

        self.memory = None

        self.plan = None

        self.processed = None

        self.agent_results = []

        self.tool_results = []

        self.metadata = {}

        self.errors = []

        self.execution = {}

        self.shared_state = SharedAgentState()

    def add_agent_result(self, result):

        self.agent_results.append(result)

    def add_tool_result(self, result):

        self.tool_results.append(result)

    def add_error(self, error):

        self.errors.append(error)
