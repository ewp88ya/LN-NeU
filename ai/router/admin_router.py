from fastapi import APIRouter

from task_queue.metrics import QueueMetrics
from observability.audit import AuditLogger


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


metrics = QueueMetrics()
audit = AuditLogger()


@router.get("/metrics")
async def metrics_status():

    return metrics.stats()



@router.get("/audit")
async def audit_status():

    return {
        "events": audit.events
    }



@router.get("/health")
async def admin_health():

    return {
        "status":"ok",
        "service":"ln-neu-ai"
    }
