import chromadb
from chromadb.config import Settings
from datetime import datetime
from typing import List, Dict

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=".chroma_memory")
collection = chroma_client.get_or_create_collection("agent_memory")

# Store a past interaction

def store_memory(session_id: str, user_query: str, agent_outputs: List[str], agent_names: List[str]):
    timestamp = datetime.utcnow().isoformat()
    doc_id = f"{session_id}_{timestamp}"
    full_text = f"User: {user_query}\nAgents: {', '.join(agent_names)}\nOutput: {' | '.join(agent_outputs)}"

    collection.add(
        documents=[full_text],
        metadatas=[{
            "session_id": session_id,
            "timestamp": timestamp,
            "agents": ', '.join(agent_names)
        }],
        ids=[doc_id]
    )

# Retrieve related memory

def search_memory(query: str, n_results: int = 3) -> List[Dict]:
    results = collection.query(query_texts=[query], n_results=n_results)
    memories = []
    for doc, meta in zip(results["documents"], results["metadatas"]):
        memories.append({
            "session_id": meta.get("session_id"),
            "timestamp": meta.get("timestamp"),
            "agents": meta.get("agents"),
            "content": doc[0]
        })
    return memories