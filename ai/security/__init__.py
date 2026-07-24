from security.authentication import Authentication
from security.authorization import Authorization
from security.rate_limit import RateLimiter
from security.secret_manager import SecretManager


try:
    from security.prompt_guard import PromptGuard
except ImportError:

    class PromptGuard:

        def inspect(
            self,
            text
        ):

            return {
                "allowed": True,
                "reason": None
            }



try:
    from security.agent_isolation import AgentIsolation
except ImportError:

    class AgentIsolation:

        def validate(
            self,
            agent_name,
            task
        ):

            return True



__all__ = [

    "Authentication",

    "Authorization",

    "RateLimiter",

    "SecretManager",

    "PromptGuard",

    "AgentIsolation",

]
