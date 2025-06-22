from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from app.planner import generate_agent_plan
from app.graph_executor import build_and_run_graph

app = FastAPI()

class AgentPlanRequest(BaseModel):
    prompt: str
    history: List[Dict]
    thread_id: str

class AgentExecutionResult(BaseModel):
    response: str
    logs: List[str]
    agent_plan: List[Dict]

@app.post("/plan")
def plan_agents(req: AgentPlanRequest):
    try:
        plan = generate_agent_plan(req.prompt, req.history)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute", response_model=AgentExecutionResult)
def execute_agents(req: AgentPlanRequest):
    try:
        result = build_and_run_graph(req.prompt, req.history, req.thread_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))