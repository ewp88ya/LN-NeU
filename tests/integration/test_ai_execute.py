import os
import urllib.request
import json
import urllib.error


def test_ai_execute():

    data = {
        "taskId": "test-001",
        "action": "echo",
        "input": "hello",
        "context": {}
    }

    req = urllib.request.Request(
        "http://localhost:8100/execute",
        data=json.dumps(data).encode(),
        headers={
            "Content-Type": "application/json",
            **({"X-LN-NeU-API-Key": os.environ["SANTOR_API_KEY"]} if os.environ.get("SANTOR_API_KEY") else {}),
        },
        method="POST"
    )

    if os.environ.get("SANTOR_API_KEY"):
        response = urllib.request.urlopen(req)
        assert response.status == 200
    else:
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as error:
            assert error.code == 401
        else:
            raise AssertionError("Expected HTTP 401 when SANTOR_API_KEY is not configured")
