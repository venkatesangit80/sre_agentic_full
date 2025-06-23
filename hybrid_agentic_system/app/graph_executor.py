from app.planner import generate_agent_plan
from app.graph_definition import build_graph
from app.checkpointer import get_checkpointer

from langgraph.graph import StateGraph

from app.state_types import AgentState
from app.llm_summarizer import summarize_response_with_llm
from typing import List, Dict

def build_and_run_graph(prompt: str, history: List[Dict], thread_id: str):
    # Get agent plan from planner
    agent_plan = generate_agent_plan(prompt, history)

    # Initialize state
    state = {
        "prompt": prompt,
        "history": history,
        "agent_plan": agent_plan,
        "current_step": 0,
        "logs": [],
        "responses": [],
        "executed_agents": []
    }

    # Build LangGraph
    builder = StateGraph(AgentState)
    build_graph(builder)  # This will add nodes and edges
    graph = builder.compile()

    # Run graph with checkpointing
    checkpointer = get_checkpointer()
    result = graph.invoke(state, config={"thread_id": thread_id, "checkpointer": checkpointer})
    final_summary = summarize_response_with_llm(result.get("responses", []))
    return {
        "response": final_summary,
        "logs": result.get("logs", []),
        "agent_plan": agent_plan
    }