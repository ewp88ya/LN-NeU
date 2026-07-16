class PromptManager:

    def build(self, action, input_text):

        return f"""
You are LN-NeU AI Engine.

Task:
{action}

Input:
{input_text}
"""
