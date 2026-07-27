from datetime import datetime, timezone


def create_metadata(
    document_id,
    source,
    stage
):

    return {
        "document_id": document_id,
        "source": source,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "processing_stage": stage,
    }
