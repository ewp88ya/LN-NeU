import pytest

from processing.orchestrator import ProcessingOrchestrator
from processing.runtime import RuntimeMetadata


class MockTask:

    taskId = "processing-test-001"

    input = "network security architecture"



class MockRuntime:

    def __init__(self):

        self.task = MockTask()
        self.processing = {}



@pytest.mark.asyncio
async def test_processing_pipeline_flow():

    orchestrator = ProcessingOrchestrator()

    runtime = MockRuntime()

    result = await orchestrator.run(
        runtime
    )

    assert result.processing is not None

    assert "document" in result.processing

    assert "etl" in result.processing

    assert "embedding" in result.processing

    assert "retrieval" in result.processing
