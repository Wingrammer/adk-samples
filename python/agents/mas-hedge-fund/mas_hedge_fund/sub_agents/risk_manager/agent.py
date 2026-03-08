# python/agents/mas-hedge-fund/sub_agents/risk_manager/agent.py
from google.adk import Agent
from . import prompt

MODEL = "gemini-2.5-pro"

risk_manager_agent = Agent(
    model=MODEL,
    name="risk_manager_agent",
    instruction=prompt.RISK_MANAGER_PROMPT,
    output_key="risk_decision",
)