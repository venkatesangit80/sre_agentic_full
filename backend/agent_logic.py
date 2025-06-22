import google.generativeai as genai
import json

# Setup Gemini
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Mock Agent Functions ---
def planner_agent(prompt):
    plan_prompt = f"""
    User query: "{prompt}"
    Available agents: planner, health, forecast, anomaly
    
    Determine which agents are required based on the prompt.
    Return only the necessary agent names in a Python list in correct order.
    Do NOT include agents like forecast/anomaly unless clearly implied.
    
    Respond with a Python list of strings. Example: ['health']
    """
    prompt_response = call_gemini(plan_prompt)
    return prompt_response

def health_agent(prompt):
    return "Health: 3 servers are showing high CPU usage."

def forecast_agent(prompt):
    return "Forecast: CPU usage is expected to breach the threshold in the next 30 minutes."

def anomaly_agent(prompt):
    return "Anomaly: Detected response time spikes on 2 nodes."

AGENT_MAP = {
    "planner": planner_agent,
    "health": health_agent,
    "forecast": forecast_agent,
    "anomaly": anomaly_agent,
}

def call_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "[Gemini Error] " + str(e)

# --- Core Logic ---
def agent_logic_generate_response(session_id, user_query, history=None):
    logs = []
    executed_agents = []

    # Step 1: Ask Gemini to plan the agent sequence
    planning_prompt = f"""
    Given the user query: "{user_query}"

    Choose only the necessary agents to execute from this list:
    ['planner', 'health', 'forecast', 'anomaly']

    Return a Python list of agent names in correct order. 
    Only include agents that are clearly needed. 
    Do NOT return Python code — just the list.
    """
    plan_raw = call_gemini(planning_prompt)

    try:
        agent_sequence = eval(plan_raw)
        print("Executed")
    except Exception as e:
        print("[Gemini Error] " + str(e))
        agent_sequence = ["planner", "health", "forecast"]  # fallback
        logs.append("Using fallback agent sequence due to eval failure.")

    # Step 2: Execute agents in order
    agent_titles = []
    if len(agent_sequence) > 0:
        for agent in agent_sequence:
            if agent in AGENT_MAP:
                output = AGENT_MAP[agent](user_query)
                logs.append(f"{agent.title()}Agent executed: {output}")
                executed_agents.append(output)
                agent_titles.append(agent.title())
            else:
                logs.append(f"Agent '{agent}' not found.")
    else:
        logs.append("No agents were selected for execution.")
        return "I’m here to help with system analysis like health checks, forecasts, or anomaly detection. Let me know how I can assist you in those areas!", logs

    # Step 3: Ask Gemini to generate final answer
    summary_prompt = f"""
    Given the following outputs from system agents, summarize a final technical response to the user query.
    
    User query: "{user_query}"
    Agent outputs:
    {json.dumps(executed_agents, indent=2)}
    
    Write a clean, helpful reply for the user.
    """
    final_response = call_gemini(summary_prompt)
    final_response = f"Agents Executed : {','.join(agent_titles)} \n Results:  {final_response}"
    logs.append("Gemini summary generated.")

    return final_response, logs