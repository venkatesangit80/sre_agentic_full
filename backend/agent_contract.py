from typing import Literal, TypedDict

class AgentContract(TypedDict):
    agent: str
    description: str
    input_value: str
    input_instruction: str
    output_instruction: str
    action_type: Literal['independent', 'dependent']

# Example usage in each agent output
example_health_contract: AgentContract = {
    "agent": "health",
    "description": "Check over and under utilized servers which are the health issue",
    "input_value": "APP1",
    "input_instruction": "Check current CPU utilization",
    "output_instruction": "Identify high-load servers",
    "action_type": "independent"
}

example_forecast_contract: AgentContract = {
    "agent": "forecast",
    "description": "Predict resource breaches for problem servers",
    "input_value": "<output of health>",
    "input_instruction": "Check the forecast only for over or under utilized servers",
    "output_instruction": "Identify if there is going to be a threshold breach",
    "action_type": "dependent"
}