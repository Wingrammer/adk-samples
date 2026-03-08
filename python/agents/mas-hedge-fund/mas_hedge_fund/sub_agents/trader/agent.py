# python/agents/mas-hedge-fund/sub_agents/trader/agent.py
from google.adk import Agent
from . import prompt

MODEL = "gemini-2.5-pro"

trader_agent = Agent(
    model=MODEL,
    name="trader_agent",
    instruction=prompt.TRADER_PROMPT,
    output_key="trade_intent",
)