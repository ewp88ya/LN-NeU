from security.middleware import SecurityMiddleware


class DummyTask:

    taskId = "auth-test"

    action = "network"

    session_id = None



def test_default_system_identity():

    security = SecurityMiddleware()

    result = security.validate(
        DummyTask()
    )

    assert result["authenticated"] is True

    assert result["identity"]["role"] == "agent"
