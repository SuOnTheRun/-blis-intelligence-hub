# Open-source collectors with gentle caching. No placeholders. Auto-skip Reddit if secrets absent.

from __future__ import annotations
import os, time, math, json, datetime as dt
from typing import List, Dict
import requests, feedparser, yfinance as yf
from cachetools import TTLCache
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# --- Caches (seconds)
cache_rss = TTLCache(maxsize=256, ttl=300)
cache_quotes = TTLCache(maxsize=256, ttl=300)
cache_trends = TTLCache(maxsize=128, ttl=600)
cache_wiki = TTLCache(maxsize=256, ttl=3600)
cache_reddit = TTLCache(maxsize=128, ttl=600)

REUTERS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/technologyNews",
    "https://feeds.reuters.com/reuters/worldNews",
]

def _sentiment(text: str) -> float:
    try:
        return analyzer.polarity_scores(text or "")["compound"]
    except Exception:
        return 0.0

# ---------- RSS (Reuters)
def get_reuters_news(keywords: List[str]) -> List[Dict]:
    kkey = " ".join(sorted([k.lower() for k in keywords]))
    if kkey in cache_rss:
        return cache_rss[kkey]
    entries = []
    for url in REUTERS_FEEDS:
        try:
            fp = feedparser.parse(url)
            for e in fp.entries:
                title = e.get("title","")
                summ = e.get("summary","")
                if any(k in title.lower() or k in summ.lower() for k in keywords):
                    entries.append({
                        "title": title,
                        "summary": summ,
                        "link": e.get("link"),
                        "published": e.get("published",""),
                        "senti": _sentiment(title),
                        "source": "Reuters"
                    })
        except Exception:
            continue
    cache_rss[kkey] = entries[:50]
    return cache_rss[kkey]

# ---------- Quotes (Yahoo Finance)
def get_quotes(symbols: List[str]) -> List[Dict]:
    skey = ",".join(symbols)
    if skey in cache_quotes:
        return cache_quotes[skey]
    out = []
    for s in symbols:
        try:
            hist = yf.Ticker(s).history(period="5d")
            if len(hist) >= 2:
                last = float(hist["Close"].iloc[-1])
                prev = float(hist["Close"].iloc[-2])
                chg = last - prev
                pct = (chg/prev)*100 if prev else 0.0
                out.append({"symbol": s, "last": round(last,2), "change": round(chg,2), "pct": round(pct,2)})
        except Exception:
            continue
    cache_quotes[skey] = out
    return out

# ---------- Google Trends (pytrends via REST-friendly helper)
# We'll import pytrends lazily to avoid import cost when not used.
def get_trends_series(keywords: List[str], geo: str="") -> Dict:
    import pandas as pd
    from pytrends.request import TrendReq
    kkey = json.dumps({"kw": keywords[:5], "geo": geo})
    if kkey in cache_trends:
        return cache_trends[kkey]
    py = TrendReq(hl="en-US", tz=330)
    py.build_payload(kw_list=keywords[:5], timeframe="today 3-m", geo=geo or "")
    df = py.interest_over_time()
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])
    labels = [d.strftime("%Y-%m-%d") for d in df.index]
    datasets = []
    for col in df.columns:
        datasets.append({"label": col, "data": [int(v) if pd.notna(v) else 0 for v in df[col].tolist()]})
    payload = {"labels": labels, "datasets": datasets}
    cache_trends[kkey] = payload
    return payload

# ---------- Wikipedia Pageviews (open)
def get_wiki_pageviews(pages: List[str], project: str="en.wikipedia") -> Dict[str, List[Dict]]:
    # Daily pageviews last 90 days
    key = json.dumps({"p": pages, "proj": project})
    if key in cache_wiki:
        return cache_wiki[key]
    base = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
    end = dt.datetime.utcnow().strftime("%Y%m%d")
    start = (dt.datetime.utcnow()-dt.timedelta(days=90)).strftime("%Y%m%d")
    out = {}
    for page in pages:
        try:
            url = f"{base}/{project}/all-access/user/{requests.utils.quote(page)}/daily/{start}/{end}"
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                items = r.json().get("items", [])
                out[page] = [{"date": i["timestamp"][:8], "views": i["views"]} for i in items]
        except Exception:
            continue
    cache_wiki[key] = out
    return out

# ---------- Reddit (optional)
def get_reddit_top(subs: List[str], per_sub: int=5) -> List[Dict]:
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    if not all(os.getenv(k) for k in required):
        return []
    import praw
    key = json.dumps({"subs": subs, "n": per_sub})
    if key in cache_reddit:
        return cache_reddit[key]
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "blis-intel-hub/1.0"),
        )
        posts = []
        for s in subs:
            for p in reddit.subreddit(s).top(time_filter="day", limit=per_sub):
                posts.append({"title": p.title, "score": int(p.score), "subreddit": str(p.subreddit),
                              "url": f"https://www.reddit.com{p.permalink}"})
        cache_reddit[key] = posts[: per_sub*len(subs)]
        return cache_reddit[key]
    except Exception:
        return []
