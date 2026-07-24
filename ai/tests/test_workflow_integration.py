import pytest

from workflows.engine import WorkflowEngine
from models.task import AITask


@pytest.mark.asyncio
async def test_network_workflow():


    engine = WorkflowEngine()


    task = AITask(

        taskId="test-001",

        action="network",

        input="google.com"

    )


    result = await engine.execute(
        task
    )


    assert result["status"] == "completed"


    assert len(
        result["agents"]
    ) > 0



@pytest.mark.asyncio
async def test_security_layer():


    engine = WorkflowEngine()


    task = AITask(

        taskId="security-test",

        action="network",

        input="google.com"

    )


    result = await engine.execute(
        task
    )


    assert (
        result["security"]["authenticated"]
        is True
    )
