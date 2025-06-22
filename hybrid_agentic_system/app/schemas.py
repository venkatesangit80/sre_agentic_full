from pydantic import BaseModel
from typing import List, Dict

class AgentPlanRequest(BaseModel):
    prompt: str
    history: List[Dict[str, str]]
    thread_id: str

class AgentExecutionResult(BaseModel):
    response: str
    logs: List[str]
    agent_plan: List[Dict]