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
