from uuid import uuid4
from typing import Dict, List

# In-memory session storage
# Maps session_id -> list of message dicts
sessions: Dict[str, List[Dict[str, str]]] = {}

def create_session() -> str:
    """Create a new session ID and initialize message history."""
    session_id = str(uuid4())
    sessions[session_id] = []
    return session_id

def get_session_history(session_id: str) -> List[Dict[str, str]]:
    """Get message history for a session."""
    return sessions.get(session_id, [])

def append_user_message(session_id: str, message: str):
    sessions.setdefault(session_id, []).append({"role": "user", "content": message})

def append_assistant_message(session_id: str, message: str):
    sessions.setdefault(session_id, []).append({"role": "assistant", "content": message})