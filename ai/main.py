import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from router.task_router import TaskRouter


from workflows.engine import WorkflowEngine



worker_task = None



async def start_worker():

    workflow = WorkflowEngine()

    worker = AsyncWorker(
        task_queue,
        workflow
    )

    await worker.start()



@asynccontextmanager
async def lifespan(app: FastAPI):

    global worker_task


    worker_task = asyncio.create_task(
        start_worker()
    )


    print("LN-NeU AI Worker started")


    yield


    if worker_task:

        worker_task.cancel()


app = FastAPI(
    title="LN-NeU AI Engine",
    version="0.1.0",
    lifespan=lifespan
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
