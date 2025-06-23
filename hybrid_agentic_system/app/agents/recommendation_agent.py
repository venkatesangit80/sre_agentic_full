from app.state_types import AgentState

def recommendation_agent(state: AgentState) -> AgentState:
    contract = state["agent_plan"][state["current_step"]]
    input_value = contract.get("input_value", "")
    input_instruction = contract.get("input_instruction", "")

    recommendation = "Scale up compute resources or optimize background tasks."
    result = f"[RecommendationAgent] Based on {input_value}, recommendation: {recommendation}"

    log = f"Recommendation executed with input: '{input_value}' → {recommendation}"

    print("Recomendation Response")
    print(state.get("responses", []))

    return {
        **state,
        "current_step": state["current_step"] + 1,
        "logs": state["logs"] + [log],
        "response": result,
        "responses": state.get("responses", []) + [result],
        "executed_agents": state.get("executed_agents", []) + ["recommendation"]
    }