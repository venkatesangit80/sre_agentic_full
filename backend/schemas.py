from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    sessionId: str
    message: str

class ChatResponse(BaseModel):
    response: str
    logs: List[str] = []

class SessionResponse(BaseModel):
    sessionId: str