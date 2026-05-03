# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from app.orchestrator import SoftwareTeamOrchestrator

app = FastAPI()
orchestrator = SoftwareTeamOrchestrator()

class RequestModel(BaseModel):
    idea: str

@app.post("/build")
def build_app(request: RequestModel):
    return orchestrator.run_pipeline(request.idea)