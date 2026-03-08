# python/agents/mas-hedge-fund/tools/news_tools.py
from __future__ import annotations
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from typing import Any, Dict, List

def fetch_googlenews_rss(query: str, limit: int = 7) -> Dict[str, Any]:
    """
    Best-effort RSS fetch. Can break. Use as a demo.
    """
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    root = ET.fromstring(r.text)

    items: List[Dict[str, Any]] = []
    for item in root.findall(".//item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        source = ""
        src = item.find("source")
        if src is not None and src.text:
            source = src.text.strip()
        items.append({"title": title, "link": link, "published": pub, "source": source})

    return {"query": query, "items": items, "source": "googlenews_rss"}