from app.state_types import AgentState

def forecast_agent(state: AgentState) -> AgentState:
    contract = state.agent_plan[state.current_step]
    input_value = contract.get("input_value", "")
    input_instruction = contract.get("input_instruction", "")

    # Mocked logic
    forecast_result = f"[ForecastAgent] Forecasted spike in CPU usage for servers mentioned in: {input_value}"

    log = f"Forecast executed with input: '{input_value}' → {forecast_result}"

    return {
        **state,
        "current_step": state.current_step + 1,
        "logs": state.logs + [log],
        "response": forecast_result
    }