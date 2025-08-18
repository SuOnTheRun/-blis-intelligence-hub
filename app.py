# app.py
# BLIS LOCATION INTELLIGENCE HUB — Streamlit Edition
# Real-data dashboard for category news, ad-tech intel, market moves, and Google Trends proxies for mobility/intent

import os
import time
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import requests
import feedparser
import yfinance as yf
from pytrends.request import TrendReq
import plotly.express as px

# ----------------------------
# CONFIG & CONSTANTS
# ----------------------------
st.set_page_config(
    page_title="Blis Intelligence Hub",
    layout="wide",
)

HEADER_STYLE = """
<style>
/**** Quiet luxury / professional ****/
:root { --ink:#0f172a; --muted:#475569; --accent:#1e293b; --line:#e2e8f0; }

.block-container { padding-top: 1.2rem; }

h1,h2,h3,h4 { color: var(--ink); font-weight: 600; letter-spacing: .2px; }

div.bordered-card { border: 1px solid var(--line); border-radius: 12px; padding: 16px; }

.badge { display:inline-block; padding:2px 8px; font-size:11px; border-radius:999px; background:#0f172a; color:white; }
.badge.muted { background:#334155; }
.badge.ok { background:#166534; }
.badge.warn { background:#b45309; }
.badge.danger { background:#991b1b; }

.small { font-size:12px; color: var(--muted); }
.link a { text-decoration:none; color:#0f172a; }
.link a:hover { text-decoration:underline; }
</style>
"""

st.markdown(HEADER_STYLE, unsafe_allow_html=True)

CATEGORY_FEEDS = {
    'QSR & Restaurant': {
        'QSR Magazine': 'https://www.qsrmagazine.com/rss.xml',
        'Restaurant Business': 'https://www.restaurantbusinessonline.com/rss.xml',
        "Nation's Restaurant News": 'https://www.nrn.com/rss.xml',
        'Food & Wine': 'https://www.foodandwine.com/rss.xml',
        'Restaurant Dive': 'https://www.restaurantdive.com/rss.xml',
    },
    'Automotive': {
        'Automotive News': 'https://www.autonews.com/rss.xml',
        'Auto Remarketing': 'https://www.autoremarketing.com/rss.xml',
        'Automotive Dive': 'https://www.automotivedive.com/rss.xml',
        'Car Dealer Magazine': 'https://www.cardealermagazine.com/rss.xml',
        'Auto Finance News': 'https://www.autofinancenews.net/feed/',
    },
    'Retail & Apparel': {
        'Retail Dive': 'https://www.retaildive.com/rss.xml',
        'Chain Store Age': 'https://chainstoreage.com/rss.xml',
        'Retail TouchPoints': 'https://www.retailtouchpoints.com/rss.xml',
        'Fashion Dive': 'https://www.fashiondive.com/rss.xml',
        'RIS News': 'https://risnews.com/rss.xml',
    },
    'Travel & Hospitality': {
        'Travel Weekly': 'https://www.travelweekly.com/rss.xml',
        'Hotel News Now': 'https://www.hotelnewsnow.com/rss.xml',
        'Skift': 'https://skift.com/feed/',
        'TTG Media': 'https://www.ttgmedia.com/rss.xml',
        'Hotel Management': 'https://www.hotelmanagement.net/rss.xml',
    },
    'Financial Services': {
        'Banking Dive': 'https://www.bankingdive.com/rss.xml',
        'The Financial Brand': 'https://thefinancialbrand.com/feed/',
        'American Banker': 'https://www.americanbanker.com/rss.xml',
        'Credit Union Times': 'https://www.cutimes.com/rss.xml',
        'Fintech News': 'https://www.fintechnews.org/feed/',
    },
    'Healthcare': {
        'Healthcare Dive': 'https://www.healthcaredive.com/rss.xml',
        'Modern Healthcare': 'https://www.modernhealthcare.com/rss.xml',
        'Healthcare Finance News': 'https://www.healthcarefinancenews.com/rss.xml',
        'MM+M': 'https://www.mmm-online.com/rss.xml',
        'Healthcare IT News': 'https://www.healthcareitnews.com/rss.xml',
    },
    'Real Estate': {
        'Commercial Property Executive': 'https://www.cpexecutive.com/rss.xml',
        'Multi-Housing News': 'https://www.multihousingnews.com/rss.xml',
        'Shopping Center Business': 'https://www.shoppingcenterbusiness.com/rss.xml',
        'National RE Investor': 'https://www.nreionline.com/rss.xml',
    },
}

ADTECH_FEEDS = {
    'LBMA': 'https://www.lbma.com/feed/',
    'AdExchanger': 'https://www.adexchanger.com/feed/',
    'Mobile Marketing Magazine': 'https://mobilemarketingmagazine.com/feed',
    'Geospatial World': 'https://www.geospatialworld.net/rss-feeds/',
    'Programmatic Advertising': 'https://www.programmatic-advertising.org/feed/',
}

CATEGORY_STOCKS = {
    'QSR & Restaurant': ['MCD','SBUX','YUM','QSR','CMG'],
    'Automotive': ['TSLA','F','GM','TM','KMX'],
    'Retail & Apparel': ['WMT','TGT','HD','LOW','COST'],
    'Travel & Hospitality': ['MAR','HLT','H','IHG','EXPE'],
    'Financial Services': ['JPM','BAC','WFC','C','GS'],
    'Healthcare': ['UNH','JNJ','PFE','ABBV','CVS'],
}

ADTECH_STOCKS = {
    'Location / Ad-Tech': ['TTD','MGNI','PUBM','GOOGL','META'],
    'Mobility / Gig': ['UBER','LYFT','DASH','ABNB'],
    'Retail Tech / Payments': ['SHOP','SQ','PYPL','V'],
}

TREND_KEYWORDS = {
    'QSR & Restaurant': ["restaurants near me","food delivery","drive thru"],
    'Automotive': ["car dealership","test drive","EV charging"],
    'Retail & Apparel': ["shopping mall","fashion store","click and collect"],
    'Travel & Hospitality': ["hotel booking","airport","tourist places"],
    'Financial Services': ["bank branch","atm near me","loan"],
    'Healthcare': ["hospital","clinic near me","pharmacy"],
    'Real Estate': ["open house","property for sale","commercial real estate"],
}

# ----------------------------
# HELPERS (cached)
# ----------------------------
@st.cache_data(ttl=60*30, show_spinner=False)
def fetch_rss(feed_url: str, limit: int = 5):
    try:
        r = requests.get(feed_url, timeout=15)
        r.raise_for_status()
        parsed = feedparser.parse(r.content)
        rows = []
        for e in parsed.entries[:limit]:
            rows.append({
                'title': e.get('title',''),
                'summary': (e.get('summary') or e.get('description') or '')[:300],
                'link': e.get('link',''),
                'published': e.get('published',''),
                'source': feed_url,
            })
        return pd.DataFrame(rows)
    except Exception as ex:
        return pd.DataFrame()

@st.cache_data(ttl=60*15, show_spinner=False)
def fetch_category_news(category: str, per_feed: int = 3):
    dfs = []
    for name, url in CATEGORY_FEEDS.get(category, {}).items():
        df = fetch_rss(url, per_feed)
        if not df.empty:
            df['feed'] = name
            df['category'] = category
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

@st.cache_data(ttl=60*15, show_spinner=False)
def fetch_adtech_news(per_feed: int = 3):
    dfs = []
    for name, url in ADTECH_FEEDS.items():
        df = fetch_rss(url, per_feed)
        if not df.empty:
            df['feed'] = name
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

@st.cache_data(ttl=60*30, show_spinner=False)
def fetch_prices(tickers: list, period: str = "5d"):
    try:
        data = yf.download(tickers, period=period, group_by='ticker', progress=False, auto_adjust=True)
        rows = []
        for t in tickers:
            try:
                close = data[t]['Close']
                if len(close) >= 2:
                    last = float(close.iloc[-1])
                    prev = float(close.iloc[-2])
                    chg = ((last - prev)/prev) * 100.0
                    rows.append({'ticker': t, 'last_close': last, 'd1_change_pct': chg})
            except Exception:
                pass
        return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=60*60, show_spinner=False)
def fetch_trends(keywords: list, geo: str = 'IN', days: int = 90):
    if not keywords:
        return pd.DataFrame()
    try:
        pytrends = TrendReq(hl='en-US', tz=330)
        timeframe = f"today {days}-d"
        pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time()
        if not df.empty:
            df = df.drop(columns=['isPartial'])
            df = df.reset_index().rename(columns={'date':'Date'})
        return df
    except Exception:
        return pd.DataFrame()

# ----------------------------
# UI — SIDEBAR
# ----------------------------
st.title("BLIS LOCATION INTELLIGENCE HUB")

with st.sidebar:
    st.subheader("Controls")
    chosen_category = st.selectbox(
        "Category",
        options=["All Categories"] + list(CATEGORY_FEEDS.keys()),
        index=0,
    )
    trends_geo = st.selectbox("Google Trends Geo", options=["IN","GB","US","SG","AU","AE"], index=0)
    show_rows = st.slider("Articles per feed", 1, 8, 3)
    st.caption("Live data: RSS (news), Yahoo Finance (prices), Google Trends (intent/mobility proxy). No placeholders.")

# ----------------------------
# LAYOUT — KPI STRIP
# ----------------------------
colA, colB, colC, colD = st.columns([1,1,1,1])
with colA:
    st.metric("Intel Feeds", sum(len(v) for v in CATEGORY_FEEDS.values()) + len(ADTECH_FEEDS))
with colB:
    st.metric("Categories", len(CATEGORY_FEEDS))
with colC:
    st.metric("Ad-Tech Feeds", len(ADTECH_FEEDS))
with colD:
    st.markdown(f"**Last Refresh**  ")
    st.caption(datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))

st.markdown("---")

# ----------------------------
# TABS
# ----------------------------
news_tab, adtech_tab, market_tab, trends_tab, data_tab = st.tabs([
    "Category Intelligence", "Location Ad-Tech", "Market Performance", "Google Trends", "Data"
])

# Category Intelligence
with news_tab:
    cats = list(CATEGORY_FEEDS.keys()) if chosen_category == "All Categories" else [chosen_category]
    for c in cats:
        df = fetch_category_news(c, per_feed=show_rows)
        st.subheader(c)
        if df.empty:
            st.caption("No articles fetched.")
            continue
        for _, row in df.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['title']}**")
                st.caption(f"{row.get('feed','')} — {row.get('published','')}")
                if row['summary']:
                    st.write(row['summary'])
                st.markdown(f"[Open article]({row['link']})")

# Ad-Tech Intel
with adtech_tab:
    ad = fetch_adtech_news(per_feed=show_rows)
    if ad.empty:
        st.caption("No articles fetched.")
    else:
        for _, row in ad.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['title']}**")
                st.caption(f"{row.get('feed','')} — {row.get('published','')}")
                if row['summary']:
                    st.write(row['summary'])
                st.markdown(f"[Open article]({row['link']})")

# Market Performance
with market_tab:
    cols = st.columns(3)
    groups = [
        ("Category Benchmark", CATEGORY_STOCKS.get(chosen_category, [])[:5] if chosen_category != "All Categories" else CATEGORY_STOCKS['Retail & Apparel'][:5]),
        ("Ad-Tech", ADTECH_STOCKS['Location / Ad-Tech']),
        ("Retail Tech / Payments", ADTECH_STOCKS['Retail Tech / Payments']),
    ]
    for (label, tickers), c in zip(groups, cols):
        with c:
            st.markdown(f"**{label}**")
            if not tickers:
                st.caption("No tickers configured.")
                continue
            p = fetch_prices(tickers)
            if p.empty:
                st.caption("No price data.")
            else:
                p = p.sort_values('d1_change_pct', ascending=False)
                st.dataframe(p, hide_index=True, use_container_width=True)
                fig = px.bar(p, x='ticker', y='d1_change_pct', title=None)
                fig.update_layout(yaxis_title="% vs prev close")
                st.plotly_chart(fig, use_container_width=True)

# Google Trends — proxy for mobility/intent
with trends_tab:
    kw = []
    if chosen_category != "All Categories":
        kw = TREND_KEYWORDS.get(chosen_category, [])[:3]
    else:
        kw = ["shopping mall","restaurants near me","hotel booking"]
    st.markdown("**Keywords**: " + ", ".join(kw))
    tdf = fetch_trends(kw, geo=trends_geo, days=180)
    if tdf.empty:
        st.caption("No trends data returned.")
    else:
        tlong = tdf.melt(id_vars=['Date'], var_name='Keyword', value_name='Interest')
        fig = px.line(tlong, x='Date', y='Interest', color='Keyword', title=None)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(tdf.tail(10), use_container_width=True, hide_index=True)

# Data Tab
with data_tab:
    st.caption("Useful for export / QA.")
    if chosen_category != "All Categories":
        st.dataframe(fetch_category_news(chosen_category, per_feed=show_rows), use_container_width=True)
    st.dataframe(fetch_adtech_news(per_feed=show_rows), use_container_width=True)

st.markdown("\n")
