import urllib.request
import json


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
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    response = urllib.request.urlopen(req)

    assert response.status == 200
