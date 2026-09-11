from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="World Tour Agent")

client = OpenAI()


class AgentRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "agent": "World Tour Agent",
        "message": "AI Agent is ready!"
    }


@app.post("/agent")
def run_agent(request: AgentRequest):
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=request.message
    )

    return {
        "status": "success",
        "response": response.output_text
    }
