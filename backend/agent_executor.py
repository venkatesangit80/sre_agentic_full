from typing import List, Dict, Any
from agent_contract import AgentContract

# Mock agent execution functions
def execute_health(contract: AgentContract) -> str:
    print("Executing health check")
    print(contract['action_type'])
    return f"[Health Report] : High CPU on 3 servers srv1, srv2, srv3."

def execute_forecast(contract: AgentContract) -> str:
    print("Executing forecast")
    print(contract['action_type'])
    return f"[Forecast] CPU threshold likely breached in next 30 minutes for srv1, srv2, srv3."

def execute_anomaly(contract: AgentContract) -> str:
    print("Executing anomaly detection")
    print(contract['action_type'])
    return f"[Anomaly] Spikes detected on nodes srv1, srv2, srv3."

def execute_planner(contract: AgentContract) -> str:
    return "[Planner] Execution plan created."

AGENT_EXECUTORS = {
    "planner": execute_planner,
    "health": execute_health,
    "forecast": execute_forecast,
    "anomaly": execute_anomaly,
}

# Executes agent plan with awareness of input/output flow
def run_agent_plan(agent_plan: List[AgentContract], initial_input: str, user_query: str) -> List[Dict[str, Any]]:
    results = []
    last_output = initial_input

    for contract in agent_plan:
        # If dependent, pass last_output as input_value
        if contract["action_type"] == "dependent":
            contract["input_value"] = last_output
        else:
            contract["input_value"] = user_query

        agent_name = contract["agent"]
        executor = AGENT_EXECUTORS.get(agent_name)

        if executor:
            output = executor(contract)
            results.append({"agent": agent_name, "output": output})
            last_output = output  # update for next dependent agent
        else:
            results.append({"agent": agent_name, "output": "No executor found."})

    return results