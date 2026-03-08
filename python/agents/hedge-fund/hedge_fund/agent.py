# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

# python/agents/mas-hedge-fund/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.market_analyst.agent import market_analyst_agent
from .sub_agents.news_analyst.agent import news_analyst_agent
from .sub_agents.trader.agent import trader_agent
from .sub_agents.risk_manager.agent import risk_manager_agent
from .sub_agents.execution.agent import execution_agent
from kybernis import KybernisSDK

MODEL = "gemini-2.5-flash"

mas_hedge_fund = LlmAgent(
    name="mas_hedge_fund_coordinator",
    model=MODEL,
    description=(
        "A demo multi-agent day/swing trading system. "
        "It pulls real market data (Alpaca), reads news (Google News best-effort), "
        "generates trade intent, evaluates risk, and (paper) submits orders. "
    ),
    instruction=prompt.COORDINATOR_PROMPT,
    output_key="mas_hedge_fund_output",
    tools=[
        AgentTool(agent=market_analyst_agent),
        AgentTool(agent=news_analyst_agent),
        AgentTool(agent=trader_agent),
        AgentTool(agent=risk_manager_agent),
        AgentTool(agent=execution_agent),
    ]
)

root_agent = mas_hedge_fund
KybernisSDK(root_agent)
