from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Req(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "AI Service OK 🤖"}

@app.post("/ask")
def ask(req: Req):
    return {
        "response": f"AI: {req.prompt}"
    }

