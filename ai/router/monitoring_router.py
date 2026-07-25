from fastapi import APIRouter

from observability.health_monitor import HealthMonitor
from observability.queue_monitor import QueueMonitor
from observability.error_tracker import ErrorTracker
from observability.dashboard import Dashboard


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)


# ======================================
# Monitoring Components
# ======================================

health = HealthMonitor()

queue = QueueMonitor()

errors = ErrorTracker()

dashboard = Dashboard()


# ======================================
# Health
# ======================================

@router.get("/health")
async def monitoring_health():

    return health.check_all()


# ======================================
# Queue Metrics
# ======================================

@router.get("/metrics")
async def monitoring_metrics():

    return queue.snapshot()


# ======================================
# Error Tracker
# ======================================

@router.get("/errors")
async def monitoring_errors():

    return {

        "total": errors.total(),

        "recent": errors.recent()

    }


# ======================================
# Dashboard
# ======================================

@router.get("/dashboard")
async def monitoring_dashboard():

    return dashboard.snapshot()
