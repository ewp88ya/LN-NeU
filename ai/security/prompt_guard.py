class PromptGuard:

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "system prompt",
        "reveal prompt",
        "bypass",
        "jailbreak",
        "developer message",
    ]

    def inspect(self, text: str):

        lower = text.lower()

        for pattern in self.BLOCKED_PATTERNS:
            if pattern in lower:
                return {
                    "allowed": False,
                    "reason": pattern,
                }

        return {
            "allowed": True,
            "reason": None,
        }
