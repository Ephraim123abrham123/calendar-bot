from fastapi import FastAPI

app = FastAPI()

@app.post("/chat")
def chat(message: str):
    return {"reply": f"Received: {message}. (Demo - will book calendar soon!)"}