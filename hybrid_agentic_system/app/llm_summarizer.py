import os
import google.generativeai as genai
from typing import List

# Configure Gemini
GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_response_with_llm(agent_outputs: List[str]) -> str:
    if not agent_outputs:
        return "No results available to summarize."

    joined = "\n".join(agent_outputs)
    prompt = f"""
You are a system assistant.

Based on the following technical outputs from multiple monitoring agents, write a natural, easy-to-understand summary suitable for a human decision-maker:

{joined}

Summarize concisely but completely. Avoid technical jargon unless necessary.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[LLM Summary Failed] {e}"