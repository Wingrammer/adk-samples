# python/agents/mas-hedge-fund/sub_agents/news_analyst/agent.py
from google.adk import Agent
from ...tools import news_tools
from . import prompt

MODEL = "gemini-2.5-pro"

news_analyst_agent = Agent(
    model=MODEL,
    name="news_analyst_agent",
    instruction=prompt.NEWS_ANALYST_PROMPT,
    output_key="news_brief",
    tools=[news_tools.fetch_googlenews_rss],
)