from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from router.task_router import TaskRouter


app = FastAPI(
    title="LN-NeU AI Engine",
    version="0.1.0"
)


router = TaskRouter()


class AITask(BaseModel):
    taskId: str
    action: str
    input: str
    context: Optional[Dict[str, Any]] = None


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "LN-NeU AI Engine"
    }


@app.post("/execute")
async def execute(task: AITask):

    return await router.route(task)
