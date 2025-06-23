from app.state_types import AgentState

def health_agent(state: AgentState) -> AgentState:
    contract = state["agent_plan"][state["current_step"]]
    input_value = contract.get("input_value", "")
    input_instruction = contract.get("input_instruction", "")

    detected_servers = ["srv1", "srv2", "srv3"]
    result = f"[HealthAgent] {input_instruction} completed. High CPU usage detected on: {', '.join(detected_servers)}."

    log = f"Health executed with input: '{input_value}' → {result}"

    print("Health Response")
    print(state.get("responses", []))
    return {
        **state,
        "current_step": state["current_step"] + 1,
        "logs": state["logs"] + [log],
        "response": result,
        "responses": state.get("responses", []) + [result],
        "executed_agents": state.get("executed_agents", []) + ["health"]
    }