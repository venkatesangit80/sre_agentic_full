from app.state_types import AgentState
from app.agents.health_agent import health_agent
from app.agents.forecast_agent import forecast_agent
from app.agents.recommendation_agent import recommendation_agent


def agent_router(state: AgentState):
    plan = state["agent_plan"]
    step = state["current_step"]
    if step >= len(plan):
        return "end"
    return plan[step]["agent"]


def identity(state: AgentState) -> AgentState:
    return state


def build_graph(builder):
    builder.add_node("health", health_agent)
    builder.add_node("forecast", forecast_agent)
    builder.add_node("recommendation", recommendation_agent)
    builder.add_node("end", lambda state: {
        "response": "\n\n".join(state.get("responses", [state.get("response", "Execution complete.")])),
        "logs": state["logs"],
        "executed_agents": state.get("executed_agents", [])
    })
    builder.add_node("router", identity)

    builder.set_entry_point("router")
    builder.add_conditional_edges("router", agent_router)
    builder.set_finish_point("end")

    for name in ["health", "forecast", "recommendation"]:
        builder.add_edge(name, "router")