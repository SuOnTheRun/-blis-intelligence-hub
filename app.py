import os
import time
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import requests
import feedparser
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from textblob import TextBlob
import praw
import yfinance as yf
import dash
from dash import html, dcc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css"
    ]
)
app.title = "Strategic Intelligence Command Center"

# White luxury aesthetic (inline HTML override)
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
            .lux-card {
                border-radius: 1.5rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                padding: 1.5rem;
                background: #FAFAFA;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>{%config%}{%scripts%}{%renderer%}</footer>
    </body>
</html>
"""


# -----------------------------------------------------------------------------
# Streamlit page config (WHITE THEME)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Strategic Intelligence Command Center",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Executive visual identity (white background)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
:root {
  --ink:#0A0A0A;            /* Deep Matte Black */
  --carbon:#1E1E1E;
  --onyx:#141414;
  --cobalt:#1F78FF;         /* Intelligence highlight */
  --crimson:#D72638;        /* Critical */
  --emerald:#2ECC71;        /* Stable */
  --gold:#E5C07B;           /* Exec overlay */
  --bg:#FFFFFF;             /* white */
  --subtle:#F8FAFC;         /* light gray */
  --border:#E5E7EB;
}

html, body, .stApp { background: var(--bg); color: var(--ink); }

.command-header {
  background: linear-gradient(180deg, #ffffff 0%, #f6f7fb 100%);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 32px 28px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(10,10,10,0.06);
}
.command-title {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  letter-spacing: 0.3px;
  font-weight: 800;
  font-size: 32px;
  margin: 0 0 6px 0;
}
.command-subtitle { font-weight: 500; color: #4B5563; margin: 0; }

.metric-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 6px 20px rgba(10,10,10,0.06);
}
.metric-value { font-size: 32px; font-weight: 800; }
.metric-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #6B7280; }

.section-h { font-weight: 800; font-size: 18px; margin: 16px 0 8px 0; }
.priority-CRITICAL { border-left: 4px solid var(--crimson); background: linear-gradient(90deg, rgba(215,38,56,0.05), #fff); }
.priority-HIGH { border-left: 4px solid #FD7E14; background: linear-gradient(90deg, rgba(253,126,20,0.05), #fff); }
.priority-MEDIUM { border-left: 4px solid var(--cobalt); background: linear-gradient(90deg, rgba(31,120,255,0.05), #fff); }
.priority-LOW { border-left: 4px solid var(--emerald); background: linear-gradient(90deg, rgba(46,204,113,0.05), #fff); }

.intel-item {
  border: 1px solid var(--border); border-radius: 18px; padding: 16px; margin-bottom: 12px;
  box-shadow: 0 2px 10px rgba(10,10,10,0.04);
}
a.source-link { color: var(--cobalt); text-decoration: none; font-weight: 600; }
a.source-link:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="command-header">
  <div class="command-title">Strategic Intelligence Command Center</div>
  <div class="command-subtitle">Global OSINT • Psychological • Market & Mobility • Threat Causality</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Secrets & API keys (from Render Environment)
# -----------------------------------------------------------------------------
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "StrategicWarRoom/1.0")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
POLYGON_KEY = os.getenv("POLYGON_ACCESS_KEY", "")

# -----------------------------------------------------------------------------
# Hotspots (real lat/lon; keep expanding as needed)
# -----------------------------------------------------------------------------
GLOBAL_HOTSPOTS = {
  'Ukraine Operational Zone': {'lat': 49.5937, 'lon': 32.2922, 'priority': 'CRITICAL', 'region': 'Eastern Europe', 'type': 'Active Conflict'},
  'Gaza Strip': {'lat': 31.3547, 'lon': 34.3088, 'priority': 'CRITICAL', 'region': 'Middle East', 'type': 'Active Conflict'},
  'West Bank': {'lat': 31.9038, 'lon': 35.2034, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Occupied Territory'},
  'Taiwan Strait': {'lat': 23.8, 'lon': 120.9, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
  'South China Sea': {'lat': 16.0, 'lon': 114.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
  'Strait of Hormuz': {'lat': 26.5667, 'lon': 56.25, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Strategic Waterway'},
  'Suez Canal': {'lat': 30.5, 'lon': 32.3, 'priority': 'MEDIUM', 'region': 'Middle East', 'type': 'Strategic Waterway'},
  'Strait of Malacca': {'lat': 2.5, 'lon': 101.8, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
  'Bosphorus Strait': {'lat': 41.1233, 'lon': 29.0781, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Strategic Waterway'},
  'Korean DMZ': {'lat': 38.0, 'lon': 127.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Border Tension'},
  'Armenia–Azerbaijan Border': {'lat': 40.0691, 'lon': 45.0382, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Border Tension'},
  'Diego Garcia': {'lat': -7.3134, 'lon': 72.4113, 'priority': 'MEDIUM', 'region': 'Indian Ocean', 'type': 'Military Base'},
  'Ramstein Air Base': {'lat': 49.4369, 'lon': 7.6003, 'priority': 'LOW', 'region': 'Europe', 'type': 'Military Base'},
  'Hong Kong': {'lat': 22.3193, 'lon': 114.1694, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Economic Zone'},
  'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'priority': 'LOW', 'region': 'Asia Pacific', 'type': 'Economic Zone'}
}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def classify_sentiment(p):
    if p > 0.1: return 'Positive'
    if p < -0.1: return 'Negative'
    return 'Neutral'

def classify_region(text_lower:str)->str:
    keywords = {
        'Eastern Europe':['ukraine','russia','belarus','poland','baltic','moldova'],
        'Asia Pacific':['china','taiwan','japan','korea','australia','singapore','india','indonesia','philippines','vietnam'],
        'Middle East':['iran','israel','palestine','gaza','saudi','syria','lebanon','iraq','yemen','qatar','uae','gulf'],
        'Europe':['nato','eu','france','germany','britain','italy','spain','sweden','norway','turkey'],
        'Africa':['egypt','libya','algeria','morocco','nigeria','ethiopia','somalia','sudan','sahel','mali','chad'],
        'Americas':['usa','united states','canada','mexico','brazil','argentina','venezuela','colombia']
    }
    for region, ks in keywords.items():
        if any(k in text_lower for k in ks): return region
    return 'Global'

# -----------------------------------------------------------------------------
# Data collectors (all real sources)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=300)
def collect_newsapi():
    if not NEWSAPI_KEY:
        return []
    url = "https://newsapi.org/v2/everything"
    domains = "reuters.com,apnews.com,bbc.co.uk,bbc.com,ft.com,wsj.com,theguardian.com"
    queries = ["military OR defense", "geopolitics OR conflict", "security OR intelligence", "cyber warfare"]
    all_rows = []
    for q in queries:
        params = {
            "q": q,
            "language": "en",
            "pageSize": 50,
            "sortBy": "publishedAt",
            "domains": domains,
            "apiKey": NEWSAPI_KEY
        }
        r = requests.get(url, params=params, timeout=20)
        if r.status_code != 200:
            continue
        for a in r.json().get("articles", []):
            title = a.get("title") or ""
            desc = a.get("description") or ""
            if len(title) < 20: 
                continue
            text = f"{title} {desc}"
            pol = TextBlob(text).sentiment.polarity
            all_rows.append({
                "source": f"NewsAPI - {a.get('source',{}).get('name','Unknown')}",
                "title": title,
                "summary": desc[:450],
                "url": a.get("url",""),
                "published": a.get("publishedAt",""),
                "sentiment": pol,
                "sentiment_label": classify_sentiment(pol),
                "region": classify_region(text.lower()),
                "credibility": 8.5,  # curated domains
                "category": "Premium News",
                "timestamp": datetime.utcnow()
            })
    return all_rows

@st.cache_data(ttl=300)
def collect_reddit():
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
        return []
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    subs = {
        "worldnews": {"region":"Global","min_score":400},
        "geopolitics": {"region":"Global","min_score":50},
        "ukraine": {"region":"Eastern Europe","min_score":100},
        "NATONews": {"region":"Europe","min_score":20},
        "intelligence": {"region":"Global","min_score":10}
    }
    out=[]
    for s, cfg in subs.items():
        try:
            for p in reddit.subreddit(s).hot(limit=40):
                if p.stickied or p.over_18 or p.score < cfg["min_score"]:
                    continue
                text = f"{p.title} {p.selftext[:300]}"
                pol = TextBlob(text).sentiment.polarity
                out.append({
                    "source": f"Reddit r/{s}",
                    "title": p.title,
                    "summary": (p.selftext or "")[:450],
                    "url": f"https://reddit.com{p.permalink}",
                    "published": datetime.utcfromtimestamp(p.created_utc).isoformat()+"Z",
                    "sentiment": pol,
                    "sentiment_label": classify_sentiment(pol),
                    "region": cfg["region"],
                    "credibility": min(10, 4 + (p.upvote_ratio*3)),
                    "category": "Social Intelligence",
                    "timestamp": datetime.utcnow()
                })
        except Exception:
            continue
    return out

@st.cache_data(ttl=300)
def collect_gdelt():
    params = {
        "query": "military OR conflict OR security OR defense OR geopolitical",
        "mode": "ArtList",
        "maxrecords": 40,
        "format": "json",
        "timespan": "24h"
    }
    try:
        r = requests.get("https://api.gdeltproject.org/api/v2/gkg/gkg", params=params, timeout=20)
        r.raise_for_status()
        out=[]
        for a in r.json().get("articles", []):
            title = a.get("title") or ""
            if len(title) < 20: 
                continue
            summary = a.get("summary","")
            text = f"{title} {summary}"
            pol = TextBlob(text).sentiment.polarity
            out.append({
                "source":"GDELT Global Intelligence",
                "title": title,
                "summary": summary[:450],
                "url": a.get("url",""),
                "published": a.get("seendate",""),
                "sentiment": pol,
                "sentiment_label": classify_sentiment(pol),
                "region": classify_region(text.lower()),
                "credibility": 8.0,
                "category": "Global Events",
                "timestamp": datetime.utcnow()
            })
        return out
    except Exception:
        return []

@st.cache_data(ttl=300)
def collect_markets():
    # Mix Polygon (equities/ETFs) and yfinance (for ^VIX)
    tickers = [
        ("LMT","Lockheed Martin","Defense"),
        ("RTX","Raytheon","Defense"),
        ("NOC","Northrop Grumman","Defense"),
        ("GLD","SPDR Gold Trust","Safe Haven"),
        ("XLE","Energy Select SPDR","Energy"),
        ("UUP","DB USD Index","Currency")
    ]
    rows=[]
    # polygon prev close for equities/ETFs
    if POLYGON_KEY:
        for t,name,cat in tickers:
            try:
                url = f"https://api.polygon.io/v2/aggs/ticker/{t}/prev"
                r = requests.get(url, params={"adjusted":"true","apiKey":POLYGON_KEY}, timeout=15)
                js = r.json()
                results = js.get("results", [])
                if not results: 
                    continue
                c = float(results[0]["c"])
                o = float(results[0]["o"]) if results[0].get("o") is not None else c
                change = ((c - o)/o)*100 if o else 0
                rows.append({"ticker":t,"name":name,"category":cat,"price":c,"change_pct":change,"timestamp":datetime.utcnow()})
            except Exception:
                continue
    # VIX via yfinance
    try:
        vix = yf.Ticker("^VIX").history(period="5d")
        if not vix.empty:
            c = float(vix["Close"].iloc[-1])
            p = float(vix["Close"].iloc[-2]) if len(vix)>1 else c
            change = ((c-p)/p)*100 if p else 0
            rows.append({"ticker":"^VIX","name":"Volatility Index","category":"Market Stress","price":c,"change_pct":change,"timestamp":datetime.utcnow()})
    except Exception:
        pass
    return rows

# -----------------------------------------------------------------------------
# Analytics (concise, robust)
# -----------------------------------------------------------------------------
def executive_assessment(all_items, market_rows):
    crit = sum(1 for x in all_items if "Critical" in x.get("title","") or x.get("sentiment",-1)<-0.4)
    avg_pol = np.mean([x.get("sentiment",0) for x in all_items]) if all_items else 0.0
    vix = next((r for r in market_rows if r["ticker"]=="^VIX"), {"price": 18.0})
    vix_norm = min(1.0, vix["price"]/50.0)
    base = min(10.0, (crit*0.3) + (abs(avg_pol)*4.0) + (vix_norm*6.0))
    level = "NORMAL"
    if base>=8: level="CRITICAL"
    elif base>=6: level="HIGH"
    elif base>=4: level="ELEVATED"
    return {
        "score": base,
        "level": level,
        "avg_sentiment": avg_pol,
        "vix": vix["price"]
    }

# -----------------------------------------------------------------------------
# UI Controls
# -----------------------------------------------------------------------------
st.sidebar.markdown("**Controls**")
regions_sel = st.sidebar.multiselect(
    "Active Regions",
    ["Global","Eastern Europe","Asia Pacific","Middle East","Europe","Africa","Americas"],
    default=["Global","Eastern Europe","Middle East","Asia Pacific"]
)
min_score = st.sidebar.slider("Minimum Credibility (soft filter)", 0.0, 10.0, 6.0, 0.5)
auto_refresh = st.sidebar.checkbox("Auto-refresh (60s)", value=False)

# -----------------------------------------------------------------------------
# Collect Data
# -----------------------------------------------------------------------------
with st.spinner("Collecting intelligence …"):
    newsapi_items = collect_newsapi()
    reddit_items = collect_reddit()
    gdelt_items = collect_gdelt()
    market_rows = collect_markets()

items = newsapi_items + reddit_items + gdelt_items

# Filter by region + simple credibility heuristic
filtered = []
for x in items:
    region_ok = (x["region"] in regions_sel) or ("Global" in regions_sel) or (x["region"]=="Global")
    if not region_ok: 
        continue
    # derive a soft intelligence_score from credibility + polarity magnitude
    intel = (x.get("credibility",6.0)) + (abs(x.get("sentiment",0))*4)
    if intel >= min_score:
        x["intelligence_score"] = float(intel)
        filtered.append(x)

assessment = executive_assessment(filtered, market_rows)

# -----------------------------------------------------------------------------
# Summary strip
# -----------------------------------------------------------------------------
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-label">Threat Level</div>
      <div class="metric-value" style="color:{('#D72638' if assessment['level']=='CRITICAL' else '#FD7E14' if assessment['level']=='HIGH' else '#1F78FF' if assessment['level']=='ELEVATED' else '#2ECC71')}">{assessment['level']}</div>
      <div>Score: {assessment['score']:.2f}/10</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-label">Sources</div>
      <div class="metric-value">{len(filtered)}</div>
      <div>Filtered (cred ≥ {min_score:.1f})</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-label">Avg Sentiment</div>
      <div class="metric-value">{assessment['avg_sentiment']:+.2f}</div>
      <div>From text analysis</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="metric-card">
      <div class="metric-label">VIX</div>
      <div class="metric-value">{assessment['vix']:.2f}</div>
      <div>Market stress</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-h">Threat Components</div>', unsafe_allow_html=True)
comp_fig = go.Figure(go.Bar(
    x=["News Sentiment","Market Volatility (VIX)"],
    y=[abs(assessment['avg_sentiment']), min(1.0, assessment['vix']/50.0)],
    text=[f"{abs(assessment['avg_sentiment']):.2f}", f"{min(1.0, assessment['vix']/50.0):.2f}"],
    textposition="auto",
    marker_color=[ "#D72638", "#FD7E14"]
))
comp_fig.update_layout(height=280, showlegend=False, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(comp_fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Global Overview","Intelligence Feed","Market Analysis","Map"])

with tab1:
    # timeline (last 60)
    df = pd.DataFrame(sorted(filtered, key=lambda z: z["timestamp"], reverse=True)[:60])
    if not df.empty:
        df["t"] = pd.to_datetime(df["published"], errors="coerce")
        df = df.sort_values("t")
        fig = px.scatter(
            df, x="t", y="intelligence_score", color="sentiment_label",
            hover_data=["title","source","region"],
            color_discrete_map={"Positive":"#2ECC71","Neutral":"#6B7280","Negative":"#D72638"}
        )
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No items passing current filters.")

with tab2:
    # grouped by priority derived from score
    def priority(s):
        return "CRITICAL" if s>=9 else "HIGH" if s>=7 else "MEDIUM" if s>=5 else "LOW"
    grouped = {"CRITICAL":[], "HIGH":[], "MEDIUM":[], "LOW":[]}
    for it in sorted(filtered, key=lambda z: z["intelligence_score"], reverse=True)[:120]:
        grouped[priority(it["intelligence_score"])].append(it)

    for label in ["CRITICAL","HIGH","MEDIUM","LOW"]:
        if not grouped[label]: 
            continue
        st.markdown(f"**{label} PRIORITY ({len(grouped[label])})**")
        for it in grouped[label][:20]:
            st.markdown(f"""
            <div class="intel-item priority-{label}">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><strong>{it["title"]}</strong></div>
                <div style="font-weight:700;">Score {it["intelligence_score"]:.1f}</div>
              </div>
              <div style="color:#4B5563;margin:6px 0 8px 0;">{it.get("summary","")}</div>
              <div style="font-size:12px;color:#6B7280;">
                Source: {it["source"]} • Region: {it["region"]} • Sentiment: {it["sentiment_label"]}
              </div>
              <div style="margin-top:6px;"><a class="source-link" href="{it.get("url","#")}" target="_blank">View source</a></div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    if market_rows:
        mdf = pd.DataFrame(market_rows)
        c1, c2 = st.columns(2)
        with c1:
            cat_fig = px.bar(
                mdf.groupby("category").agg(change_pct=("change_pct","mean")).reset_index(),
                x="category", y="change_pct", color="change_pct", color_continuous_scale=["#D72638","#FFFFFF","#2ECC71"],
                title="Performance by Category (prev day)"
            )
            cat_fig.update_layout(height=320, margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(cat_fig, use_container_width=True)
        with c2:
            st.dataframe(
                mdf[["ticker","name","category","price","change_pct"]].sort_values("change_pct", ascending=False),
                use_container_width=True
            )
    else:
        st.info("No market rows available.")

with tab4:
    m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB positron")
    color = {"CRITICAL":"#D72638","HIGH":"#FD7E14","MEDIUM":"#1F78FF","LOW":"#2ECC71"}
    for name,data in GLOBAL_HOTSPOTS.items():
        folium.CircleMarker(
            location=[data["lat"], data["lon"]],
            radius=10 if data["priority"]=="CRITICAL" else 8 if data["priority"]=="HIGH" else 6,
            color=color[data["priority"]], fill=True, fillOpacity=0.85,
            popup=folium.Popup(f"<b>{name}</b><br>Priority: {data['priority']}<br>Region: {data['region']}<br>Type: {data['type']}<br>Lat,Lon: {data['lat']:.4f}, {data['lon']:.4f}", max_width=300)
        ).add_to(m)
    st_folium(m, use_container_width=True, height=520)

# optional auto-refresh
if auto_refresh:
    time.sleep(60)
    st.experimental_rerun()
app = dash.Dash(__name__, ...)
server = app.server  # gunicorn entry
