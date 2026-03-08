# python/agents/mas-hedge-fund/tools/alpaca_tools.py
from __future__ import annotations
import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# Alpaca clients are per alpaca-py documentation. :contentReference[oaicite:1]{index=1}

def _trading_client() -> TradingClient:
    key = os.environ["ALPACA_API_KEY"]
    secret = os.environ["ALPACA_API_SECRET"]
    paper = os.environ.get("ALPACA_PAPER", "true").lower() == "true"
    return TradingClient(key, secret, paper=paper)

def _data_client() -> StockHistoricalDataClient:
    key = os.environ["ALPACA_API_KEY"]
    secret = os.environ["ALPACA_API_SECRET"]
    return StockHistoricalDataClient(key, secret)

def get_account() -> Dict[str, Any]:
    acct = _trading_client().get_account()
    # acct is a pydantic-like object; safe stringify fields we care about
    return {
        "id": getattr(acct, "id", None),
        "status": getattr(acct, "status", None),
        "equity": getattr(acct, "equity", None),
        "cash": getattr(acct, "cash", None),
        "buying_power": getattr(acct, "buying_power", None),
        "currency": getattr(acct, "currency", None),
        "paper": os.environ.get("ALPACA_PAPER", "true"),
    }

def get_latest_quote(symbol: str) -> Dict[str, Any]:
    req = StockLatestQuoteRequest(symbol_or_symbols=symbol)
    resp = _data_client().get_stock_latest_quote(req)
    q = resp[symbol]
    return {
        "symbol": symbol,
        "ask_price": float(q.ask_price),
        "bid_price": float(q.bid_price),
        "ask_size": int(q.ask_size),
        "bid_size": int(q.bid_size),
        "timestamp": str(q.timestamp),
    }

def get_recent_bars(symbol: str, minutes: int = 120) -> Dict[str, Any]:
    req = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        limit=max(10, min(1000, minutes)),
    )
    bars = _data_client().get_stock_bars(req).data.get(symbol, [])
    # return last N
    packed = [
        {
            "t": str(b.timestamp),
            "o": float(b.open),
            "h": float(b.high),
            "l": float(b.low),
            "c": float(b.close),
            "v": float(b.volume),
        }
        for b in bars[-minutes:]
    ]
    return {"symbol": symbol, "timeframe": "1Min", "bars": packed}

def submit_market_order(symbol: str, qty: float, side: str) -> Dict[str, Any]:
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    resp = _trading_client().submit_order(order_data=order)
    return {"id": str(resp.id), "symbol": symbol, "qty": float(qty), "side": side, "type": "market"}

def submit_limit_order(symbol: str, qty: float, side: str, limit_price: float) -> Dict[str, Any]:
    order = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
        limit_price=limit_price,
    )
    resp = _trading_client().submit_order(order_data=order)
    return {
        "id": str(resp.id),
        "symbol": symbol,
        "qty": float(qty),
        "side": side,
        "type": "limit",
        "limit_price": float(limit_price),
    }