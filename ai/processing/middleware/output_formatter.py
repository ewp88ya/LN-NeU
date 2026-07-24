from copy import deepcopy


class OutputFormatter:
    """
    Preserve the workflow response exactly as produced by WorkflowEngine.

    The formatter only guarantees a consistent dictionary output and
    performs a deep copy so downstream code cannot mutate the original.
    """

    def format(self, response):
        if response is None:
            return {}

        if isinstance(response, dict):
            return deepcopy(response)

        if hasattr(response, "model_dump"):
            return deepcopy(response.model_dump())

        if hasattr(response, "dict"):
            return deepcopy(response.dict())

        return {
            "status": "completed",
            "result": deepcopy(response),
        }
