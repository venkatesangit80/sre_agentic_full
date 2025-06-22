import google.generativeai as genai
import os
import json
from typing import List, Dict

# Initialize Gemini model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Descriptions used in prompt planning
AGENT_DESCRIPTIONS = {
    "health": "Check over and under utilized servers.",
    "forecast": "Predict resource usage trends.",
    "recommendation": "Recommend actions based on current and future health."
}

def generate_agent_plan(user_prompt: str, history: List[Dict]) -> List[Dict]:
    """
    Use Gemini to generate a structured plan of agents to run based on prompt and conversation history.
    """
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    system_prompt = f"""
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
    "description": "Predict resource usage trends.",
    "input_value": "APP1",
    "input_instruction": "Use health output to run forecast",
    "output_instruction": "Return CPU trend over next 30 mins",
    "action_type": "dependent"
  }}
]
"""

    prompt = f"{system_prompt}\n\nUser query: \"{user_prompt}\"\n"
    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
        return result
    except Exception as e:
        raise ValueError(f"Failed to parse plan: {e}\nRaw response: {response.text}")