# python/agents/mas-hedge-fund/sub_agents/market_analyst/agent.py
from google.adk import Agent
from ...tools import alpaca_tools
from . import prompt

MODEL = "gemini-2.5-pro"

market_analyst_agent = Agent(
    model=MODEL,
    name="market_analyst_agent",
    instruction=prompt.MARKET_ANALYST_PROMPT,
    output_key="market_snapshot",
    tools=[
        alpaca_tools.get_account,
        alpaca_tools.get_latest_quote,
        alpaca_tools.get_recent_bars,
    ],
)