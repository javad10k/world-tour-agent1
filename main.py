from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="World Tour Agent")


class AgentRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "agent": "World Tour Agent",
        "message": "World Tour Agent is ready!"
    }


@app.post("/agent")
def run_agent(request: AgentRequest):
    return {
        "status": "success",
        "received": request.message,
        "response": "World Tour Agent received your request."
    }
