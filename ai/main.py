from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Service OK 🤖"}

@app.post("/ask")
def ask(data: dict):
    prompt = data.get("prompt", "")

    return {
        "message": "AI Service OK 🤖",
        "prompt": prompt,
        "response": f"Echo: {prompt}"
    }
