# MAS Hedge Fund (Demo)

Educational multi-agent trading system built with Google ADK.

It demonstrates why multi-agent systems need an execution/governance layer:
- Agents can suggest actions confidently.
- Tool calls (orders) are side-effects: they must be budgeted, deduped, and retried safely.
- Without idempotency keyed by request-id, UI double-clicks can duplicate orders.

This demo uses:
- alpaca-py for account + real market data + paper orders
- best-effort Google News headline fetcher

## Safety
- Paper trading only by default (ALPACA_PAPER=true).
- Educational demo only; not financial advice.

## Run
uv sync
adk run mas_hedge_fund
or
adk web