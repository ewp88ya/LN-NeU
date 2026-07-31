import asyncio

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

from router.task_router import TaskRouter
from router.monitoring_router import router as monitoring_router

from router.admin_router import router as admin_router

# =========================
# AI TASK CONTRACT
# =========================

class AITask(BaseModel):

    taskId: str = Field(
        alias="taskId"
    )

    action: str

    input: Any

    context: Dict[str, Any] = {}

    class Config:

        populate_by_name = True


# =========================
# WORKER PLACEHOLDER
# =========================

async def start_worker():

    """
    Worker berjalan sebagai service terpisah.
    """

    return


# =========================
# APP LIFECYCLE
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("LN-NeU AI Engine started")

    yield

    print("LN-NeU AI Engine stopped")


# =========================
# FASTAPI
# =========================

app = FastAPI(

    title="LN-NeU AI Engine",

    version="0.1.0",

    lifespan=lifespan

)


# =========================
# Router Instance
# =========================

task_router = TaskRouter()


# =========================
# Admin API
# =========================

app.include_router(
    admin_router
)


# =========================
# Monitoring API
# =========================

app.include_router(
    monitoring_router
)


# =========================
# Health
# =========================

@app.get("/health")
async def health():

    return {

        "status": "ok",

        "service": "LN-NeU AI Engine",

        "version": "0.1.0"

    }


# =========================
# Execute
# =========================

@app.post("/execute")
async def execute(task: AITask):

    return await task_router.route(task)
