from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse, SessionResponse
from session_store import create_session, get_session_history, append_user_message, append_assistant_message
from agent_pipeline import run_agentic_pipeline
from agent_planner import plan_agent_sequence
from memory_store import store_memory
import google.generativeai as genai
import json

app = FastAPI()

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup for final summarization
genai.configure(api_key="AIzaSyCZmt2f9wUNYu1T-2PJozFd_t4N1chOv9Y")
llm = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/session", response_model=SessionResponse)
def new_session():
    session_id = create_session()
    return {"sessionId": session_id}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.sessionId
    user_msg = req.message

    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session ID")

    # Record user message
    append_user_message(session_id, user_msg)

    # Get conversation history (optional)
    history = get_session_history(session_id)

    # Run agent planner and pipeline
    try:
        agent_plan = plan_agent_sequence(user_msg, session_id)
        summary, logs = run_agentic_pipeline(user_msg, req.message, session_id)

        logs.insert(0, f"User query: {user_msg}")
        logs.insert(1, f"Agent plan: {[c['agent'] for c in agent_plan]}")

        # Generate LLM-based explanation of outputs in user-friendly format
        reasoning_prompt = f"""
You are an assistant summarizing technical agent output for an end user.

Here is the user query:
"{user_msg}"

Here is a list of agent execution steps:
{json.dumps(logs[3:], indent=2)}

Please summarize the system's behavior and key findings clearly:
- Mention what was checked (e.g., health, forecast)
- Mention any specific issues (e.g., high CPU, anomalies)
- If specific servers or thresholds are mentioned, include them

Format it like:
"The system checked the health of your servers and predicted future issues. It found..."

Do not include the raw log lines — just a clean, natural-language response.
"""
        llm_response = llm.generate_content(reasoning_prompt)
        response_summary = llm_response.text.strip()
        summary = response_summary
        logs.insert(2, f"LLM-based summary: {response_summary}")

        # Add simple line at the end listing agents and type
        executed_summary = ", ".join([f"{c['agent']} ({c['action_type']})" for c in agent_plan])
        logs.append(f"Agents executed: {executed_summary}")

        # Store to memory
        agent_outputs = [log.split(": ", 1)[1] for log in logs[3:] if ": " in log]
        agent_names = [c["agent"] for c in agent_plan]
        store_memory(session_id, user_msg, agent_outputs, agent_names)

    except Exception as e:
        print("Error during agent execution:", e)
        raise HTTPException(status_code=500, detail=str(e))

    # Record assistant reply
    append_assistant_message(session_id, summary)

    return {"response": summary, "logs": logs}