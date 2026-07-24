import asyncio

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Dict
from contextlib import asynccontextmanager

from router.task_router import TaskRouter

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
    Worker dijalankan sebagai service/container terpisah.
    AI Engine tidak menjalankan worker internal.
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
# FASTAPI APP
# =========================

app = FastAPI(
    title="LN-NeU AI Engine",
    version="0.1.0",
    lifespan=lifespan
)

router = TaskRouter()

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "LN-NeU AI Engine",
        "version": "0.1.0"
    }

# =========================
# EXECUTION API
# =========================

@app.post("/execute")
async def execute(task: AITask):

    return await router.route(task)
