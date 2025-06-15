from typing import Tuple, List
from agent_planner import plan_agent_sequence
from agent_executor import run_agent_plan
from agent_contract import AgentContract

def run_agentic_pipeline(user_query: str, user_prompt: str, session_id:str, context_value: str = "APP1") -> Tuple[str, List[str]]:
    logs: List[str] = []

    # Step 1: Get the structured agent plan
    plan: List[AgentContract] = plan_agent_sequence(user_query, session_id)
    logs.append(f"Gemini returned plan with {len(plan)} agent(s): {[p['agent'] for p in plan]}")

    if not plan:
        gentle_msg = (
            "I’m here to help with system analysis like health checks, forecasts, or anomaly detection. "
            "Let me know how I can assist you in those areas!"
        )
        logs.append("No relevant agents found.")
        return gentle_msg, logs

    # Step 2: Run the agent plan
    results = run_agent_plan(plan, initial_input=context_value, user_query=user_prompt)

    # Step 3: Build final summary from outputs
    summary_lines = [r["output"] for r in results]
    final_summary = "\n".join(summary_lines)
    logs.extend([f"{r['agent'].title()} output: {r['output']}" for r in results])

    return final_summary, logs