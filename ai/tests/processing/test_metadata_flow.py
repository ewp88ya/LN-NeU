import pytest

from processing.orchestrator import ProcessingOrchestrator


class MockTask:

    taskId = "metadata-test-001"

    input = "security architecture"



class MockRuntime:

    def __init__(self):

        self.task = MockTask()
        self.processing = {}



@pytest.mark.asyncio
async def test_metadata_flow():

    orchestrator = ProcessingOrchestrator()

    runtime = MockRuntime()

    result = await orchestrator.run(
        runtime
    )


    assert "retrieval" in result.processing

    assert len(result.processing["retrieval"]) > 0

    metadata = (
        result.processing["retrieval"][0]["metadata"]
    )


    assert "document_id" in metadata
    assert "source" in metadata
    assert "created_at" in metadata
    assert "processing_stage" in metadata
