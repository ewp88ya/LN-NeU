from security.authentication import Authentication
from security.authorization import Authorization
from security.rate_limit import RateLimiter


from observability.audit import AuditLogger



class SecurityMiddleware:


    def __init__(
        self,
        audit=None
    ):

        self.auth = Authentication()

        self.authorization = Authorization()

        self.rate_limiter = RateLimiter(
            limit=100
        )


        self.audit = (

            audit

            or

            AuditLogger()

        )



    def validate(
        self,
        task
    ):


        task_id = getattr(
            task,
            "taskId",
            None
        )


        action = getattr(
            task,
            "action",
            None
        )



        try:


            # =========================
            # Rate Limit Check
            # =========================

            allowed = self.rate_limiter.allow(
                task_id
            )


            if not allowed:


                self.audit.record(

                    "security_denied",

                    {

                        "reason":
                            "rate_limit_exceeded",

                        "task_id":
                            task_id,

                        "action":
                            action

                    }

                )


                raise PermissionError(
                    "Rate limit exceeded"
                )



            # =========================
            # System Identity
            # =========================

            session_id = getattr(
                task,
                "session_id",
                None
            )


            identity = self.auth.validate(
                session_id
            ) if session_id else None


            if not identity:

                identity = {

                    "user_id":
                    "system",

                    "role":
                    "agent"

            }


            # =========================
            # Authorization
            # =========================

            permission = self.authorization.allowed(

                identity["role"],

                "execute_task"

            )



            if not permission:


                self.audit.record(

                    "security_denied",

                    {

                        "reason":
                            "permission_denied",

                        "task_id":
                            task_id,

                        "role":
                            identity["role"]

                    }

                )


                raise PermissionError(
                    "Permission denied"
                )



            # =========================
            # Security Success Audit
            # =========================

            self.audit.record(

                "security_validated",

                {

                    "task_id":
                        task_id,

                    "action":
                        action,

                    "identity":
                        identity

                }

            )



            return {


                "authenticated":
                    True,


                "identity":
                    identity


            }



        except PermissionError:


            raise



        except Exception as error:


            self.audit.record(

                "security_error",

                {

                    "task_id":
                        task_id,

                    "error":
                        repr(error)

                }

            )


            raise
