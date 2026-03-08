# python/agents/mas-hedge-fund/sub_agents/execution/agent.py
from google.adk import Agent
from ...tools import alpaca_tools
from . import prompt

MODEL = "gemini-2.5-pro"


def guarded_submit_order(
    user_id: str,
    session_id: str,
    client_request_id: str,
    order: dict,
):
    """
    order dict fields:
      symbol, qty, side, type, limit_price?
    """
    def _do():
        if order["type"] == "market":
            return alpaca_tools.submit_market_order(order["symbol"], order["qty"], order["side"])
        return alpaca_tools.submit_limit_order(order["symbol"], order["qty"], order["side"], order["limit_price"])

    return _do()

execution_agent = Agent(
    model=MODEL,
    name="execution_agent",
    instruction=prompt.EXECUTION_PROMPT,
    output_key="execution_result",
    tools=[
        alpaca_tools.get_account,
        guarded_submit_order,
    ],
)