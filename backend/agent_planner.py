import google.generativeai as genai
import json
from typing import List
from agent_contract import AgentContract
from session_store import get_session_history

# Configure Gemini API
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")

# Agent descriptions used for planning
AGENT_DESCRIPTIONS = {
  "planner": "Determine the agent sequence from the user's query.",
  "health": "Check the health status of APP1. Detect overloaded or underutilized servers. Triggered by words like: health, status, utilization.",
  "forecast": "Predict if any metric (CPU, memory, etc.) may breach a threshold in the future. Triggered by: predict, forecast, upcoming issues.",
  "anomaly": "Detect unexpected spikes or anomalies in system metrics. Triggered by: anomaly, unusual, unexpected, spike."
}

# Prompt Gemini to generate structured plan
def plan_agent_sequence(user_query: str, session_id: str) -> List[AgentContract]:
    history = get_session_history(session_id)
    history_text = "\\n".join([f"{m['role']}: {m['content']}" for m in history])
    print("history_text")
    print(history_text)
    planning_prompt = f"""
    You are an agent planner.

    Your task is to determine the next set of agents to execute based on the full conversation context — not just the latest user input.

    Review all user and assistant messages below, including any agent responses or summaries:
    {history_text}

    The available agents and their purposes are:
    {json.dumps(AGENT_DESCRIPTIONS, indent=2)}

    Return a Python list of agent contracts (dicts). For each, provide:
    - agent name
    - description (from above)
    - input_value (e.g., 'APP1')
    - input_instruction
    - output_instruction
    - action_type: 'independent' or 'dependent'

    Respond ONLY with a Python list. Do not include explanations or comments.

    Example:
    [
      {{
        "agent": "forecast",
        "description": "...",
        "input_value": "...",
        "input_instruction": "...",
        "output_instruction": "...",
        "action_type": "dependent"
      }}
    ]
    """
    try:
        response = model.generate_content(planning_prompt)
        response_value = response.text.strip()
        response_value = response_value.replace("```", "")  # Ensure valid JSON format
        response_value = response_value.replace("python", "")  # Ensure valid JSON format
        return json.loads(response_value)
    except Exception as e:
        print("Gemini planner error:", e)
        return []