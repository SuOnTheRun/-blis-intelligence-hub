# ============================================================================
# ULTIMATE STRATEGIC INTELLIGENCE COMMAND CENTER v3.0
# LUXURY ENTERPRISE-GRADE OSINT PLATFORM
# Maximum Sophistication • Ultimate Control • Zero Compromises
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import feedparser
import praw
import yfinance as yf
from datetime import datetime, timedelta, timezone
import time
import json
import re
from textblob import TextBlob
import warnings
import base64
from io import BytesIO
import folium
from folium import plugins
warnings.filterwarnings('ignore')

# ============================================================================
# LUXURY DESIGN SYSTEM
# ============================================================================

st.set_page_config(
    page_title="Strategic Intelligence Command Center",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ULTIMATE LUXURY STYLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@200;300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
        --luxury-black: #0D0D0D;
        --luxury-charcoal: #1A1A1A;
        --luxury-graphite: #2D2D2D;
        --luxury-platinum: #E8E8E8;
        --luxury-silver: #C4C4C4;
        --luxury-gold: #D4AF37;
        --luxury-bronze: #CD7F32;
        --luxury-navy: #1E3A8A;
        --luxury-blue: #3B82F6;
        --luxury-accent: #6366F1;
        --luxury-emerald: #10B981;
        --luxury-amber: #F59E0B;
        --luxury-rose: #E11D48;
        --luxury-border: #404040;
        --luxury-shadow: rgba(0,0,0,0.4);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--luxury-black) 0%, var(--luxury-charcoal) 100%);
        color: var(--luxury-platinum);
        font-family: 'Inter', sans-serif;
    }
    
    .luxury-header {
        background: linear-gradient(135deg, var(--luxury-charcoal) 0%, var(--luxury-graphite) 50%, var(--luxury-charcoal) 100%);
        border: 2px solid var(--luxury-border);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        box-shadow: 0 20px 40px var(--luxury-shadow);
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, var(--luxury-gold), var(--luxury-accent), var(--luxury-emerald), var(--luxury-gold));
        background-size: 400% 100%;
        animation: shimmer 8s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .luxury-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 4px;
        color: var(--luxury-gold);
        text-transform: uppercase;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(212, 175, 55, 0.3);
        line-height: 1.1;
    }
    
    .luxury-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: var(--luxury-silver);
        margin-top: 1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .classification-banner {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, var(--luxury-rose), #DC2626);
        color: white;
        text-align: center;
        padding: 0.8rem;
        font-weight: 900;
        font-size: 0.9rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .luxury-card {
        background: linear-gradient(135deg, var(--luxury-charcoal) 0%, var(--luxury-graphite) 100%);
        border: 1px solid var(--luxury-border);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .luxury-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--luxury-gold);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .luxury-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: var(--luxury-gold);
    }
    
    .luxury-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-luxury {
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--luxury-gold);
        line-height: 1;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: var(--luxury-silver);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .status-operational { color: var(--luxury-emerald); }
    .status-elevated { color: var(--luxury-amber); }
    .status-critical { color: var(--luxury-rose); animation: pulse-glow 2s infinite; }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 1; text-shadow: 0 0 10px currentColor; }
        50% { opacity: 0.7; text-shadow: 0 0 20px currentColor; }
    }
    
    .intelligence-section {
        background: var(--luxury-charcoal);
        border: 1px solid var(--luxury-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--luxury-gold);
        transition: all 0.3s ease;
    }
    
    .intelligence-section:hover {
        border-left-color: var(--luxury-accent);
        background: linear-gradient(135deg, var(--luxury-charcoal) 0%, var(--luxury-graphite) 100%);
        transform: translateX(4px);
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--luxury-gold);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .intelligence-item {
        background: rgba(45, 45, 45, 0.6);
        border: 1px solid var(--luxury-border);
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .intelligence-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: var(--luxury-blue);
        transition: all 0.3s ease;
    }
    
    .intelligence-item:hover {
        background: rgba(212, 175, 55, 0.05);
        border-color: var(--luxury-gold);
        transform: translateX(6px);
    }
    
    .intelligence-item:hover::before {
        background: var(--luxury-gold);
        width: 6px;
    }
    
    .priority-critical::before { background: var(--luxury-rose) !important; }
    .priority-high::before { background: var(--luxury-amber) !important; }
    .priority-medium::before { background: var(--luxury-blue) !important; }
    .priority-low::before { background: var(--luxury-emerald) !important; }
    
    .tag-luxury {
        display: inline-block;
        background: rgba(212, 175, 55, 0.15);
        color: var(--luxury-gold);
        padding: 0.3rem 0.8rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .tag-critical { background: rgba(225, 29, 72, 0.15); color: var(--luxury-rose); border-color: rgba(225, 29, 72, 0.3); }
    .tag-high { background: rgba(245, 158, 11, 0.15); color: var(--luxury-amber); border-color: rgba(245, 158, 11, 0.3); }
    .tag-medium { background: rgba(59, 130, 246, 0.15); color: var(--luxury-blue); border-color: rgba(59, 130, 246, 0.3); }
    .tag-low { background: rgba(16, 185, 129, 0.15); color: var(--luxury-emerald); border-color: rgba(16, 185, 129, 0.3); }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.8rem;
        background: linear-gradient(45deg, var(--luxury-rose), #DC2626);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
        animation: pulse-glow 3s infinite;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.4);
    }
    
    .trend-chart {
        background: var(--luxury-charcoal);
        border: 1px solid var(--luxury-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .interactive-button {
        background: linear-gradient(45deg, var(--luxury-gold), var(--luxury-bronze));
        color: var(--luxury-black);
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    
    .interactive-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
        background: linear-gradient(45deg, var(--luxury-bronze), var(--luxury-gold));
    }
    
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .route-analysis {
        background: var(--luxury-charcoal);
        border: 1px solid var(--luxury-border);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid var(--luxury-accent);
    }
    
    .sentiment-score {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .sentiment-positive { color: var(--luxury-emerald); }
    .sentiment-negative { color: var(--luxury-rose); }
    .sentiment-neutral { color: var(--luxury-silver); }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--luxury-charcoal) 0%, var(--luxury-black) 100%);
        border-right: 2px solid var(--luxury-border);
    }
    
    div[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--luxury-charcoal);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--luxury-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--luxury-silver);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
        padding: 1rem 1.5rem;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(212, 175, 55, 0.1);
        color: var(--luxury-gold);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(45deg, var(--luxury-gold), var(--luxury-bronze));
        color: var(--luxury-black);
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ENHANCED DATA COLLECTION SYSTEM
# ============================================================================

class UltimateIntelligenceCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Ultimate-Intelligence-Platform/3.0 (Luxury-Enterprise)'
        })
        
        # Initialize Reddit
        try:
            self.reddit = praw.Reddit(
                client_id="gPAQFk1IFWSkMEVMXFMMCQ",
                client_secret="2LoxxZ8c-Cr-Y0rrE9CmwvQQuHdskw",
                user_agent="StrategicWarRoom/1.0 by u/Quick_Shower_6934"
            )
        except:
            self.reddit = None
        
        # PREMIUM INTELLIGENCE SOURCES
        self.elite_sources = {
            'geopolitical_intelligence': {
                'Reuters World': 'https://feeds.reuters.com/reuters/worldNews',
                'AP International': 'https://feeds.apnews.com/rss/apf-topnews',
                'BBC Global': 'http://feeds.bbci.co.uk/news/world/rss.xml',
                'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
                'Financial Times': 'https://www.ft.com/news-feed.rss'
            },
            'defense_military': {
                'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
                'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
                'Breaking Defense': 'https://breakingdefense.com/feed/',
                'War on the Rocks': 'https://warontherocks.com/feed/',
                'Institute for War': 'https://www.understandingwar.org/rss.xml'
            },
            'economic_warfare': {
                'Bloomberg Markets': 'https://feeds.bloomberg.com/markets/news.rss',
                'MarketWatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
                'Economic Times': 'https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms',
                'Nikkei Asia': 'https://asia.nikkei.com/rss/feed/nar'
            },
            'conflict_monitoring': {
                'LiveUAMap': 'https://liveuamap.com/rss',
                'Crisis Group': 'https://www.crisisgroup.org/rss.xml',
                'ACLED Data': 'https://acleddata.com/rss'
            }
        }
        
        # COMPREHENSIVE SUBREDDIT NETWORK
        self.intelligence_subreddits = {
            'worldnews': {'weight': 1.0, 'region': 'Global', 'category': 'Breaking News'},
            'geopolitics': {'weight': 1.0, 'region': 'Global', 'category': 'Strategic Analysis'},
            'UkraineConflict': {'weight': 0.9, 'region': 'Eastern Europe', 'category': 'Active Conflict'},
            'syriancivilwar': {'weight': 0.8, 'region': 'Middle East', 'category': 'Regional Conflict'},
            'china': {'weight': 0.9, 'region': 'Asia Pacific', 'category': 'Superpower Dynamics'},
            'russia': {'weight': 0.9, 'region': 'Eastern Europe', 'category': 'Superpower Dynamics'},
            'investing': {'weight': 0.7, 'region': 'Global', 'category': 'Market Intelligence'},
            'security': {'weight': 0.8, 'region': 'Global', 'category': 'Security Analysis'},
            'intelligence': {'weight': 1.0, 'region': 'Global', 'category': 'OSINT'},
            'CombatFootage': {'weight': 0.7, 'region': 'Global', 'category': 'Tactical Intelligence'}
        }
        
        # COMPREHENSIVE MARKET TARGETS
        self.market_targets = {
            # Global Indices
            '^GSPC': {'name': 'S&P 500', 'type': 'index', 'region': 'North America', 'importance': 'Critical'},
            '^DJI': {'name': 'Dow Jones', 'type': 'index', 'region': 'North America', 'importance': 'Critical'},
            '^IXIC': {'name': 'NASDAQ', 'type': 'index', 'region': 'North America', 'importance': 'Critical'},
            '^NSEI': {'name': 'Nifty 50', 'type': 'index', 'region': 'India', 'importance': 'High'},
            '^N225': {'name': 'Nikkei 225', 'type': 'index', 'region': 'Japan', 'importance': 'High'},
            '^FTSE': {'name': 'FTSE 100', 'type': 'index', 'region': 'UK', 'importance': 'High'},
            
            # Defense & Aerospace
            'LMT': {'name': 'Lockheed Martin', 'type': 'defense', 'region': 'North America', 'importance': 'Critical'},
            'RTX': {'name': 'Raytheon Technologies', 'type': 'defense', 'region': 'North America', 'importance': 'Critical'},
            'NOC': {'name': 'Northrop Grumman', 'type': 'defense', 'region': 'North America', 'importance': 'Critical'},
            'GD': {'name': 'General Dynamics', 'type': 'defense', 'region': 'North America', 'importance': 'Critical'},
            'BA': {'name': 'Boeing', 'type': 'aerospace', 'region': 'North America', 'importance': 'High'},
            
            # Risk Indicators
            '^VIX': {'name': 'VIX Fear Index', 'type': 'volatility', 'region': 'Global', 'importance': 'Critical'},
            'GLD': {'name': 'Gold ETF', 'type': 'safe_haven', 'region': 'Global', 'importance': 'High'},
            'TLT': {'name': 'US Treasury Bonds', 'type': 'safe_haven', 'region': 'Global', 'importance': 'High'},
            
            # Commodities
            'CL=F': {'name': 'Crude Oil', 'type': 'commodity', 'region': 'Global', 'importance': 'Critical'},
            'NG=F': {'name': 'Natural Gas', 'type': 'commodity', 'region': 'Global', 'importance': 'High'},
            
            # Regional Powers
            'RELIANCE.NS': {'name': 'Reliance Industries', 'type': 'energy', 'region': 'India', 'importance': 'High'},
            'TCS.NS': {'name': 'Tata Consultancy', 'type': 'technology', 'region': 'India', 'importance': 'Medium'},
            'TSLA': {'name': 'Tesla', 'type': 'technology', 'region': 'North America', 'importance': 'Medium'}
        }

    @st.cache_data(ttl=300)
    def collect_comprehensive_reddit_intelligence(_self):
        """Comprehensive Reddit OSINT with detailed analysis"""
        if not _self.reddit:
            return []
        
        intelligence = []
        
        for subreddit_name, config in _self.intelligence_subreddits.items():
            try:
                subreddit = _self.reddit.subreddit(subreddit_name)
                posts = list(subreddit.hot(limit=20))
                
                for post in posts:
                    # Enhanced text analysis
                    full_text = f"{post.title} {post.selftext[:1000]}"
                    sentiment = TextBlob(full_text).sentiment
                    
                    # Geopolitical keyword detection
                    keywords = _self._detect_keywords(full_text)
                    
                    # Enhanced intelligence scoring
                    base_score = (post.score * 0.4 + post.num_comments * 0.3 + post.upvote_ratio * 50)
                    keyword_bonus = len(keywords) * 15
                    sentiment_factor = abs(sentiment.polarity) * 20
                    intelligence_score = (base_score + keyword_bonus + sentiment_factor) * config['weight']
                    
                    # Advanced priority classification
                    if intelligence_score > 800 or any(kw in ['war', 'nuclear', 'crisis'] for kw in keywords):
                        priority = 'CRITICAL'
                    elif intelligence_score > 400 or any(kw in ['military', 'sanctions', 'conflict'] for kw in keywords):
                        priority = 'HIGH'
                    elif intelligence_score > 150:
                        priority = 'MEDIUM'
                    else:
                        priority = 'LOW'
                    
                    # Enhanced metadata
                    created_time = datetime.fromtimestamp(post.created_utc)
                    time_relevance = max(0, 1 - (datetime.now() - created_time).total_seconds() / 86400)  # Decay over 24h
                    
                    intelligence.append({
                        'source': f'Reddit r/{subreddit_name}',
                        'category': config['category'],
                        'title': post.title,
                        'content_preview': post.selftext[:300] if post.selftext else 'Link post',
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'upvote_ratio': post.upvote_ratio,
                        'author': str(post.author) if post.author else 'Unknown',
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_subjectivity': sentiment.subjectivity,
                        'keywords': keywords,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': config['region'],
                        'timestamp': created_time,
                        'time_relevance': time_relevance,
                        'engagement_rate': post.num_comments / max(1, post.score),
                        'type': 'social_intelligence',
                        'clickable': True
                    })
                    
            except Exception as e:
                continue
        
        return sorted(intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_comprehensive_news_intelligence(_self):
        """Comprehensive news intelligence with full analysis"""
        news_intelligence = []
        
        for category, sources in _self.elite_sources.items():
            for source_name, url in sources.items():
                try:
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:15]:
                        # Enhanced content analysis
                        full_content = f"{entry.title} {entry.get('summary', '')} {entry.get('description', '')}"
                        sentiment = TextBlob(full_content).sentiment
                        
                        # Advanced keyword detection
                        keywords = _self._detect_keywords(full_content)
                        
                        # Source credibility scoring
                        credibility = _self._calculate_credibility(source_name)
                        
                        # Geographic detection
                        regions = _self._detect_regions(full_content)
                        
                        # Enhanced intelligence scoring
                        base_score = credibility * 0.4
                        keyword_score = len(keywords) * 12
                        sentiment_score = abs(sentiment.polarity) * 15
                        recency_score = 20  # Assume recent for RSS
                        intelligence_score = base_score + keyword_score + sentiment_score + recency_score
                        
                        # Priority classification
                        if intelligence_score > 85 or 'BREAKING' in entry.title.upper():
                            priority = 'CRITICAL'
                        elif intelligence_score > 65:
                            priority = 'HIGH'
                        elif intelligence_score > 45:
                            priority = 'MEDIUM'
                        else:
                            priority = 'LOW'
                        
                        # Enhanced metadata
                        published_time = entry.get('published_parsed')
                        if published_time:
                            published_dt = datetime(*published_time[:6])
                        else:
                            published_dt = datetime.now()
                        
                        news_intelligence.append({
                            'source': source_name,
                            'category': category,
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:500],
                            'full_content': full_content[:1000],
                            'url': entry.link,
                            'published': entry.get('published', ''),
                            'published_dt': published_dt,
                            'author': entry.get('author', 'Staff'),
                            'sentiment_polarity': sentiment.polarity,
                            'sentiment_subjectivity': sentiment.subjectivity,
                            'keywords': keywords,
                            'regions_detected': regions,
                            'credibility_score': credibility,
                            'intelligence_score': intelligence_score,
                            'priority': priority,
                            'timestamp': datetime.now(),
                            'type': 'news_intelligence',
                            'clickable': True
                        })
                        
                except Exception as e:
                    continue
        
        return sorted(news_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_comprehensive_market_intelligence(_self):
        """Comprehensive market intelligence with detailed analysis"""
        market_intelligence = []
        
        for ticker, config in _self.market_targets.items():
            try:
                stock = yf.Ticker(ticker)
                
                # Get multiple timeframes
                hist_1d = stock.history(period="1d", interval="1h")
                hist_5d = stock.history(period="5d")
                hist_1m = stock.history(period="1mo")
                
                info = stock.info
                
                if not hist_5d.empty:
                    current_price = hist_5d['Close'].iloc[-1]
                    
                    # Enhanced calculations
                    day_change = ((hist_5d['Close'].iloc[-1] - hist_5d['Close'].iloc[-2]) / hist_5d['Close'].iloc[-2]) * 100 if len(hist_5d) > 1 else 0
                    week_change = ((hist_5d['Close'].iloc[-1] - hist_5d['Close'].iloc[0]) / hist_5d['Close'].iloc[0]) * 100 if len(hist_5d) > 1 else 0
                    # Volatility calculations
                   daily_volatility = hist_5d['Close'].pct_change().std() * 100
                   intraday_volatility = (hist_5d['High'] - hist_5d['Low']).mean() / hist_5d['Close'].mean() * 100
                   
                   # Volume analysis
                   avg_volume = hist_5d['Volume'].mean()
                   current_volume = hist_5d['Volume'].iloc[-1]
                   volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                   
                   # Risk assessment
                   risk_factors = []
                   if abs(day_change) > 5:
                       risk_factors.append('HIGH_VOLATILITY')
                   if volume_ratio > 2:
                       risk_factors.append('UNUSUAL_VOLUME')
                   if config['type'] == 'defense' and day_change > 3:
                       risk_factors.append('DEFENSE_SURGE')
                   
                   # Overall risk classification
                   if len(risk_factors) >= 2 or abs(day_change) > 7:
                       risk_level = 'CRITICAL'
                   elif len(risk_factors) >= 1 or abs(day_change) > 3:
                       risk_level = 'HIGH'
                   elif abs(day_change) > 1:
                       risk_level = 'MEDIUM'
                   else:
                       risk_level = 'LOW'
                   
                   # Technical indicators
                   rsi = _self._calculate_rsi(hist_5d['Close']) if len(hist_5d) >= 14 else 50
                   
                   market_intelligence.append({
                       'ticker': ticker,
                       'name': config['name'],
                       'type': config['type'],
                       'region': config['region'],
                       'importance': config['importance'],
                       'current_price': current_price,
                       'day_change_pct': day_change,
                       'week_change_pct': week_change,
                       'daily_volatility': daily_volatility,
                       'intraday_volatility': intraday_volatility,
                       'volume': current_volume,
                       'volume_ratio': volume_ratio,
                       'market_cap': info.get('marketCap', 'N/A'),
                       'sector': info.get('sector', 'N/A'),
                       'risk_level': risk_level,
                       'risk_factors': risk_factors,
                       'rsi': rsi,
                       'timestamp': datetime.now(),
                       'clickable': True
                   })
                   
           except Exception as e:
               continue
       
       return market_intelligence

   @st.cache_data(ttl=600)
   def collect_advanced_mobility_intelligence(_self):
       """Advanced mobility intelligence with route analysis"""
       try:
           url = "https://opensky-network.org/api/states/all"
           response = _self.session.get(url, timeout=25)
           
           if response.status_code == 200:
               data = response.json()
               mobility_intelligence = []
               
               if 'states' in data and data['states']:
                   for state in data['states'][:150]:
                       if state[5] and state[6]:  # Has coordinates
                           callsign = state[1].strip() if state[1] else 'UNKNOWN'
                           
                           # Enhanced aircraft classification
                           aircraft_type = _self._classify_aircraft_advanced(callsign)
                           threat_level = _self._assess_threat_advanced(callsign, state[7], state[9])
                           origin_country = state[2] if state[2] else 'Unknown'
                           
                           # Route analysis (simplified)
                           route_category = _self._analyze_route(state[6], state[5], origin_country)
                           
                           mobility_intelligence.append({
                               'callsign': callsign,
                               'country': origin_country,
                               'longitude': state[5],
                               'latitude': state[6],
                               'altitude': state[7] if state[7] else 0,
                               'velocity': state[9] if state[9] else 0,
                               'heading': state[10] if state[10] else 0,
                               'on_ground': state[8],
                               'aircraft_type': aircraft_type,
                               'threat_level': threat_level,
                               'route_category': route_category,
                               'last_contact': state[4] if state[4] else time.time(),
                               'timestamp': datetime.now(),
                               'clickable': True
                           })
               
               return mobility_intelligence
           else:
               return []
               
       except Exception as e:
           return []

   def _detect_keywords(self, text):
       """Enhanced keyword detection"""
       keyword_categories = {
           'conflict': ['war', 'battle', 'conflict', 'fighting', 'combat', 'invasion', 'attack', 'strike'],
           'military': ['military', 'army', 'navy', 'air force', 'troops', 'soldiers', 'weapons', 'missile'],
           'nuclear': ['nuclear', 'atomic', 'reactor', 'uranium', 'plutonium', 'warhead'],
           'economic': ['sanctions', 'embargo', 'trade', 'tariff', 'economy', 'market', 'inflation'],
           'diplomatic': ['summit', 'treaty', 'agreement', 'negotiation', 'alliance', 'embassy'],
           'security': ['terrorism', 'intelligence', 'surveillance', 'cyber', 'hacking', 'breach'],
           'crisis': ['crisis', 'emergency', 'disaster', 'evacuation', 'refugee', 'humanitarian']
       }
       
       detected = []
       text_lower = text.lower()
       
       for category, keywords in keyword_categories.items():
           if any(keyword in text_lower for keyword in keywords):
               detected.append(category)
       
       return detected

   def _detect_regions(self, text):
       """Detect geographical regions mentioned"""
       regions_map = {
           'ukraine': 'Eastern Europe',
           'russia': 'Eastern Europe',
           'china': 'Asia Pacific',
           'taiwan': 'Asia Pacific',
           'israel': 'Middle East',
           'iran': 'Middle East',
           'syria': 'Middle East',
           'iraq': 'Middle East',
           'afghanistan': 'Central Asia',
           'india': 'South Asia',
           'pakistan': 'South Asia',
           'north korea': 'Asia Pacific',
           'south korea': 'Asia Pacific',
           'japan': 'Asia Pacific'
       }
       
       detected_regions = []
       text_lower = text.lower()
       
       for country, region in regions_map.items():
           if country in text_lower and region not in detected_regions:
               detected_regions.append(region)
       
       return detected_regions

   def _calculate_credibility(self, source_name):
       """Calculate source credibility score"""
       credibility_scores = {
           'Reuters': 95, 'AP': 95, 'BBC': 92, 'Financial Times': 90,
           'Wall Street Journal': 88, 'Bloomberg': 87, 'Al Jazeera': 85,
           'Defense News': 82, 'Military Times': 80, 'Breaking Defense': 78,
           'War on the Rocks': 85, 'Institute for War': 88, 'Crisis Group': 87,
           'Economic Times': 75, 'Nikkei Asia': 80, 'ACLED': 90
       }
       
       for source, score in credibility_scores.items():
           if source.lower() in source_name.lower():
               return score
       
       return 60  # Default credibility

   def _classify_aircraft_advanced(self, callsign):
       """Advanced aircraft classification"""
       military_patterns = {
           'FORTE': 'Military Drone',
           'REAPER': 'Military Drone',
           'HAWK': 'Military Aircraft',
           'ARMY': 'Military Transport',
           'NAVY': 'Naval Aviation',
           'USAF': 'US Air Force',
           'RAF': 'Royal Air Force'
       }
       
       commercial_patterns = {
           'DL': 'Delta Airlines',
           'AA': 'American Airlines',
           'UA': 'United Airlines',
           'BA': 'British Airways',
           'LH': 'Lufthansa',
           'AF': 'Air France'
       }
       
       callsign_upper = callsign.upper()
       
       for pattern, classification in military_patterns.items():
           if pattern in callsign_upper:
               return classification
       
       for pattern, classification in commercial_patterns.items():
           if callsign_upper.startswith(pattern):
               return classification
       
       return 'Unknown Aircraft'

   def _assess_threat_advanced(self, callsign, altitude, velocity):
       """Advanced threat assessment"""
       callsign_upper = callsign.upper()
       
       # Critical threats
       if any(pattern in callsign_upper for pattern in ['FORTE', 'REAPER', 'DRONE']):
           return 'CRITICAL'
       
       # High threats
       if any(pattern in callsign_upper for pattern in ['MILITARY', 'ARMY', 'NAVY', 'USAF']):
           return 'HIGH'
       
       # Altitude-based assessment
       if altitude and altitude > 45000:  # Very high altitude
           return 'MEDIUM'
       
       # Velocity-based assessment
       if velocity and velocity > 250:  # High speed
           return 'MEDIUM'
       
       return 'LOW'

   def _analyze_route(self, lat, lon, country):
       """Analyze flight route category"""
       # Simplified route analysis based on coordinates
       if 35 <= lat <= 55 and 20 <= lon <= 40:  # Europe/Middle East
           return 'Strategic Corridor'
       elif 20 <= lat <= 35 and 100 <= lon <= 140:  # Asia Pacific
           return 'Pacific Routes'
       elif 25 <= lat <= 50 and -130 <= lon <= -70:  # North America
           return 'Continental Routes'
       else:
           return 'International Routes'

   def _calculate_rsi(self, prices, period=14):
       """Calculate Relative Strength Index"""
       if len(prices) < period:
           return 50
       
       delta = prices.diff()
       gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
       loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
       
       rs = gain / loss
       rsi = 100 - (100 / (1 + rs))
       
       return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

# ============================================================================
# ADVANCED ANALYTICS ENGINE
# ============================================================================

class UltimateAnalyticsEngine:
   def __init__(self):
       pass
   
   def generate_comprehensive_assessment(self, reddit_data, news_data, market_data, mobility_data):
       """Generate comprehensive strategic assessment"""
       
       # Enhanced metrics calculation
       total_sources = len(reddit_data) + len(news_data)
       critical_items = len([item for item in reddit_data + news_data if item.get('priority') == 'CRITICAL'])
       high_priority_items = len([item for item in reddit_data + news_data if item.get('priority') == 'HIGH'])
       
       # Advanced sentiment analysis
       all_sentiment = [item.get('sentiment_polarity', 0) for item in reddit_data + news_data]
       avg_sentiment = np.mean(all_sentiment) if all_sentiment else 0
       sentiment_volatility = np.std(all_sentiment) if all_sentiment else 0
       
       # Enhanced regional analysis
       regional_activity = self._analyze_regional_activity_advanced(reddit_data + news_data)
       
       # Comprehensive market analysis
       market_stress = self._calculate_market_stress_advanced(market_data)
       defense_sector_status = self._analyze_defense_sector(market_data)
       
       # Advanced mobility assessment
       mobility_assessment = self._assess_mobility_patterns_advanced(mobility_data)
       
       # Multi-factor threat calculation
       threat_level = self._calculate_comprehensive_threat(
           critical_items, high_priority_items, market_stress, 
           mobility_assessment, sentiment_volatility
       )
       
       # Trend analysis
       trend_analysis = self._analyze_trends(reddit_data, news_data, market_data)
       
       return {
           'total_sources': total_sources,
           'critical_items': critical_items,
           'high_priority_items': high_priority_items,
           'avg_sentiment': avg_sentiment,
           'sentiment_volatility': sentiment_volatility,
           'regional_activity': regional_activity,
           'market_stress': market_stress,
           'defense_sector_status': defense_sector_status,
           'mobility_assessment': mobility_assessment,
           'threat_level': threat_level,
           'trend_analysis': trend_analysis,
           'timestamp': datetime.now(),
           'confidence_score': self._calculate_confidence_score(total_sources, critical_items)
       }
   
   def _analyze_regional_activity_advanced(self, data):
       """Advanced regional activity analysis"""
       regional_data = {}
       
       for item in data:
           regions = item.get('regions_detected', [item.get('region', 'Global')])
           if not regions:
               regions = ['Global']
           
           for region in regions:
               if region not in regional_data:
                   regional_data[region] = {
                       'total': 0, 'critical': 0, 'high': 0, 'medium': 0, 'low': 0,
                       'avg_sentiment': 0, 'sentiment_data': [],
                       'categories': {}, 'keywords': [],
                       'trend_direction': 'stable'
                   }
               
               regional_data[region]['total'] += 1
               regional_data[region][item.get('priority', 'low').lower()] += 1
               
               if 'sentiment_polarity' in item:
                   regional_data[region]['sentiment_data'].append(item['sentiment_polarity'])
               
               # Category tracking
               category = item.get('category', 'Unknown')
               if category not in regional_data[region]['categories']:
                   regional_data[region]['categories'][category] = 0
               regional_data[region]['categories'][category] += 1
               
               # Keyword aggregation
               if 'keywords' in item:
                   regional_data[region]['keywords'].extend(item['keywords'])
       
       # Calculate averages and trends
       for region, data in regional_data.items():
           if data['sentiment_data']:
               data['avg_sentiment'] = np.mean(data['sentiment_data'])
           
           # Simple trend calculation based on critical/high ratio
           total_items = data['total']
           if total_items > 0:
               risk_ratio = (data['critical'] * 2 + data['high']) / total_items
               if risk_ratio > 0.6:
                   data['trend_direction'] = 'escalating'
               elif risk_ratio < 0.2:
                   data['trend_direction'] = 'de-escalating'
               else:
                   data['trend_direction'] = 'stable'
       
       return regional_data
   
   def _calculate_market_stress_advanced(self, market_data):
       """Advanced market stress calculation"""
       if not market_data:
           return {'overall_stress': 0, 'components': {}}
       
       df = pd.DataFrame(market_data)
       
       # VIX component
       vix_data = df[df['name'].str.contains('VIX', na=False)]
       vix_stress = (vix_data.iloc[0]['current_price'] / 40 * 100) if not vix_data.empty else 25
       
       # Volatility component
       avg_volatility = df['daily_volatility'].mean()
       volatility_stress = min(100, avg_volatility * 5)
       
       # Defense sector component
       defense_stocks = df[df['type'] == 'defense']
       defense_performance = defense_stocks['day_change_pct'].mean() if not defense_stocks.empty else 0
       defense_stress = min(100, abs(defense_performance) * 10)
       
       # Safe haven component
       safe_haven_stocks = df[df['type'] == 'safe_haven']
       safe_haven_performance = safe_haven_stocks['day_change_pct'].mean() if not safe_haven_stocks.empty else 0
       safe_haven_stress = max(0, safe_haven_performance * 5)  # Positive movement in safe havens = stress
       
       # Overall calculation
       overall_stress = (vix_stress * 0.4 + volatility_stress * 0.3 + 
                        defense_stress * 0.2 + safe_haven_stress * 0.1)
       
       return {
           'overall_stress': min(100, overall_stress),
           'components': {
               'vix_stress': min(100, vix_stress),
               'volatility_stress': min(100, volatility_stress),
               'defense_stress': min(100, defense_stress),
               'safe_haven_stress': min(100, safe_haven_stress)
           }
       }
   
   def _analyze_defense_sector(self, market_data):
       """Analyze defense sector specifically"""
       if not market_data:
           return {}
       
       df = pd.DataFrame(market_data)
       defense_stocks = df[df['type'] == 'defense']
       
       if defense_stocks.empty:
           return {}
       
       return {
           'sector_performance': defense_stocks['day_change_pct'].mean(),
           'top_performer': defense_stocks.loc[defense_stocks['day_change_pct'].idxmax()]['name'],
           'worst_performer': defense_stocks.loc[defense_stocks['day_change_pct'].idxmin()]['name'],
           'avg_volatility': defense_stocks['daily_volatility'].mean(),
           'total_companies': len(defense_stocks),
           'risk_assessment': 'HIGH' if defense_stocks['day_change_pct'].mean() > 3 else 'MEDIUM' if defense_stocks['day_change_pct'].mean() > 1 else 'LOW'
       }
   
   def _assess_mobility_patterns_advanced(self, mobility_data):
       """Advanced mobility pattern analysis"""
       if not mobility_data:
           return {
               'total_aircraft': 0, 'military_aircraft': 0, 'commercial_aircraft': 0,
               'threat_assessment': 'LOW', 'critical_threats': 0,
               'route_analysis': {}, 'country_distribution': {}
           }
       
       df = pd.DataFrame(mobility_data)
       
       # Basic counts
       total_aircraft = len(df)
       military_aircraft = len(df[df['aircraft_type'].str.contains('Military', na=False)])
       commercial_aircraft = len(df[df['aircraft_type'].str.contains('Airlines', na=False)])
       
       # Threat analysis
       critical_threats = len(df[df['threat_level'] == 'CRITICAL'])
       high_threats = len(df[df['threat_level'] == 'HIGH'])
       
       # Overall threat assessment
       if critical_threats > 10:
           threat_assessment = 'CRITICAL'
       elif critical_threats > 5 or high_threats > 20:
           threat_assessment = 'HIGH'
       elif critical_threats > 0 or high_threats > 10:
           threat_assessment = 'MEDIUM'
       else:
           threat_assessment = 'LOW'
       
       # Route analysis
       route_analysis = df['route_category'].value_counts().to_dict()
       
       # Country distribution
       country_distribution = df['country'].value_counts().head(10).to_dict()
       
       return {
           'total_aircraft': total_aircraft,
           'military_aircraft': military_aircraft,
           'commercial_aircraft': commercial_aircraft,
           'threat_assessment': threat_assessment,
           'critical_threats': critical_threats,
           'high_threats': high_threats,
           'route_analysis': route_analysis,
           'country_distribution': country_distribution,
           'average_altitude': df['altitude'].mean() if 'altitude' in df.columns else 0,
           'average_velocity': df['velocity'].mean() if 'velocity' in df.columns else 0
       }
   
   def _calculate_comprehensive_threat(self, critical_items, high_priority_items, 
                                     market_stress, mobility_assessment, sentiment_volatility):
       """Comprehensive threat level calculation"""
       threat_score = 0
       
       # Intelligence threat component
       threat_score += critical_items * 15
       threat_score += high_priority_items * 8
       
       # Market stress component
       threat_score += market_stress.get('overall_stress', 0) * 0.8
       
       # Mobility threat component
       mobility_threat_scores = {'CRITICAL': 60, 'HIGH': 35, 'MEDIUM': 20, 'LOW': 5}
       threat_score += mobility_threat_scores.get(mobility_assessment.get('threat_assessment', 'LOW'), 5)
       
       # Sentiment volatility component
       threat_score += sentiment_volatility * 50
       
       # Classification
       if threat_score > 200:
           return 'CRITICAL'
       elif threat_score > 120:
           return 'HIGH'
       elif threat_score > 60:
           return 'MEDIUM'
       else:
           return 'LOW'
   
   def _analyze_trends(self, reddit_data, news_data, market_data):
       """Analyze trends across all data sources"""
       trends = {
           'intelligence_trends': {},
           'market_trends': {},
           'emerging_topics': [],
           'risk_factors': []
       }
       
       # Intelligence trends
       all_keywords = []
       for item in reddit_data + news_data:
           all_keywords.extend(item.get('keywords', []))
       
       if all_keywords:
           keyword_counts = pd.Series(all_keywords).value_counts()
           trends['emerging_topics'] = keyword_counts.head(10).to_dict()
       
       # Market trends
       if market_data:
           df = pd.DataFrame(market_data)
           trends['market_trends'] = {
               'avg_performance': df['day_change_pct'].mean(),
               'volatility_trend': 'HIGH' if df['daily_volatility'].mean() > 3 else 'NORMAL',
               'risk_assets_performance': df[df['type'].isin(['defense', 'commodity'])]['day_change_pct'].mean()
           }
       
       return trends
   
   def _calculate_confidence_score(self, total_sources, critical_items):
       """Calculate confidence score for the assessment"""
       base_confidence = min(100, total_sources * 2)  # More sources = more confidence
       critical_adjustment = min(20, critical_items * 5)  # Critical items add confidence
       
       return min(100, base_confidence + critical_adjustment)

# ============================================================================
# LUXURY DASHBOARD ENGINE
# ============================================================================

def create_luxury_map(mobility_data):
   """Create luxury map with route lines"""
   if not mobility_data:
       return None
   
   # Create base map
   center_lat = np.mean([item['latitude'] for item in mobility_data])
   center_lon = np.mean([item['longitude'] for item in mobility_data])
   
   m = folium.Map(
       location=[center_lat, center_lon],
       zoom_start=4,
       tiles='CartoDB dark_matter'
   )
   
   # Add aircraft markers with route lines
   for i, aircraft in enumerate(mobility_data[:100]):
       # Color based on threat level
       color_map = {
           'CRITICAL': 'red',
           'HIGH': 'orange', 
           'MEDIUM': 'yellow',
           'LOW': 'lightblue'
       }
       
       color = color_map.get(aircraft['threat_level'], 'lightblue')
       
       # Add marker
       folium.CircleMarker(
           location=[aircraft['latitude'], aircraft['longitude']],
           radius=8 if aircraft['threat_level'] in ['CRITICAL', 'HIGH'] else 5,
           popup=f"""
           <b>{aircraft['callsign']}</b><br>
           Type: {aircraft['aircraft_type']}<br>
           Country: {aircraft['country']}<br>
           Altitude: {aircraft['altitude']:,}m<br>
           Speed: {aircraft['velocity']:.0f}m/s<br>
           Threat: {aircraft['threat_level']}
           """,
           color=color,
           fill=True,
           fillColor=color,
           fillOpacity=0.8
       ).add_to(m)
       
       # Add route line (simplified - connecting to next aircraft)
       if i < len(mobility_data) - 1 and aircraft['threat_level'] in ['CRITICAL', 'HIGH']:
           next_aircraft = mobility_data[i + 1]
           folium.PolyLine(
               locations=[
                   [aircraft['latitude'], aircraft['longitude']],
                   [next_aircraft['latitude'], next_aircraft['longitude']]
               ],
               color=color,
               weight=2,
               opacity=0.6
           ).add_to(m)
   
   # Add legend
   legend_html = '''
   <div style="position: fixed; 
               top: 10px; right: 10px; width: 150px; height: 120px; 
               background-color: rgba(0,0,0,0.8); border:2px solid grey; z-index:9999; 
               font-size:14px; color: white; padding: 10px">
   <h4>Threat Levels</h4>
   <i class="fa fa-circle" style="color:red"></i> Critical<br>
   <i class="fa fa-circle" style="color:orange"></i> High<br>
   <i class="fa fa-circle" style="color:yellow"></i> Medium<br>
   <i class="fa fa-circle" style="color:lightblue"></i> Low
   </div>
   '''
   m.get_root().html.add_child(folium.Element(legend_html))
   
   return m

def create_pdf_report(assessment, reddit_data, news_data, market_data):
   """Create downloadable PDF report"""
   from io import BytesIO
   
   # Create a simple HTML report
   html_content = f"""
   <!DOCTYPE html>
   <html>
   <head>
       <title>Strategic Intelligence Report</title>
       <style>
           body {{ font-family: Arial, sans-serif; margin: 40px; }}
           .header {{ text-align: center; margin-bottom: 30px; }}
           .section {{ margin-bottom: 25px; }}
           .metric {{ background: #f5f5f5; padding: 15px; margin: 10px 0; }}
           .critical {{ color: #e11d48; font-weight: bold; }}
           .high {{ color: #f59e0b; font-weight: bold; }}
       </style>
   </head>
   <body>
       <div class="header">
           <h1>STRATEGIC INTELLIGENCE REPORT</h1>
           <p>Classification: SENSITIVE</p>
           <p>Generated: {assessment['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
       </div>
       
       <div class="section">
           <h2>EXECUTIVE SUMMARY</h2>
           <div class="metric">Overall Threat Level: <span class="{assessment['threat_level'].lower()}">{assessment['threat_level']}</span></div>
           <div class="metric">Total Intelligence Sources: {assessment['total_sources']}</div>
           <div class="metric">Critical Priority Items: {assessment['critical_items']}</div>
           <div class="metric">Market Stress Level: {assessment['market_stress']['overall_stress']:.1f}/100</div>
           <div class="metric">Aircraft Tracked: {assessment['mobility_assessment']['total_aircraft']}</div>
       </div>
       
       <div class="section">
           <h2>REGIONAL ACTIVITY</h2>
           {''.join([f'<p><b>{region}:</b> {data["total"]} items ({data["critical"]} critical)</p>' 
                    for region, data in assessment['regional_activity'].items()])}
       </div>
       
       <div class="section">
           <h2>TOP CRITICAL INTELLIGENCE</h2>
           {''.join([f'<p class="critical">• {item["title"][:100]}...</p>' 
                    for item in (reddit_data + news_data)[:10] if item.get('priority') == 'CRITICAL'])}
       </div>
       
       <div class="section">
           <p><i>This report contains sensitive intelligence information. Handle according to security protocols.</i></p>
       </div>
   </body>
   </html>
   """
   
   return html_content

def main():
   # LUXURY HEADER
   st.markdown("""
   <div class="luxury-header">
       <div class="classification-banner">⬛ CLASSIFIED - STRATEGIC INTELLIGENCE OPERATIONS ⬛</div>
       <h1 class="luxury-title">STRATEGIC INTELLIGENCE COMMAND CENTER</h1>
       <p class="luxury-subtitle">ULTIMATE OSINT • GEOPOLITICAL WARFARE • THREAT ASSESSMENT</p>
       <div class="live-indicator">
           <span>●</span> LIVE INTELLIGENCE ACTIVE
       </div>
   </div>
   """, unsafe_allow_html=True)
   
   # LUXURY SIDEBAR
   st.sidebar.markdown("## ⬛ COMMAND CONTROLS")
   st.sidebar.markdown("---")
   
   # Enhanced filters
   st.sidebar.markdown("### 🌍 GEOGRAPHIC INTELLIGENCE")
   regions = ['Global', 'North America', 'Europe', 'Asia Pacific', 'Middle East', 'Africa', 'Eastern Europe', 'South Asia', 'Central Asia']
   selected_regions = st.sidebar.multiselect("Active Regions:", regions, default=['Global', 'Middle East', 'Asia Pacific'])
   
   st.sidebar.markdown("### 🎯 PRIORITY MATRIX")
   priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
   selected_priorities = st.sidebar.multiselect("Priority Classification:", priorities, default=priorities)
   
   st.sidebar.markdown("### 📡 SOURCE CATEGORIES")
   source_categories = ['Social Intelligence', 'News Intelligence', 'Market Intelligence', 'Mobility Intelligence']
   selected_sources = st.sidebar.multiselect("Intelligence Sources:", source_categories, default=source_categories)
   
   st.sidebar.markdown("### ⚡ SYSTEM CONTROLS")
   auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=True)
   show_detailed_analysis = st.sidebar.checkbox("Show detailed analysis", value=True)
   
   if st.sidebar.button("🔄 FORCE REFRESH", use_container_width=True):
       st.cache_data.clear()
       st.rerun()
   
   # Initialize systems
   collector = UltimateIntelligenceCollector()
   analyzer = UltimateAnalyticsEngine()
   
   # ENHANCED DATA COLLECTION
   with st.container():
       st.markdown("### 📡 INTELLIGENCE COLLECTION MATRIX")
       
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           with st.spinner("Reddit OSINT..."):
           reddit_data = collector.collect_comprehensive_reddit_intelligence()
           st.markdown(f"""
           <div class="luxury-card metric-luxury">
               <div class="metric-value">{len(reddit_data)}</div>
               <div class="metric-label">Reddit OSINT</div>
               <div class="metric-delta status-operational">OPERATIONAL</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           with st.spinner("News Intelligence..."):
               news_data = collector.collect_comprehensive_news_intelligence()
           st.markdown(f"""
           <div class="luxury-card metric-luxury">
               <div class="metric-value">{len(news_data)}</div>
               <div class="metric-label">News Sources</div>
               <div class="metric-delta status-operational">ACTIVE</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           with st.spinner("Market Intelligence..."):
               market_data = collector.collect_comprehensive_market_intelligence()
           st.markdown(f"""
           <div class="luxury-card metric-luxury">
               <div class="metric-value">{len(market_data)}</div>
               <div class="metric-label">Market Assets</div>
               <div class="metric-delta status-operational">TRACKED</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col4:
           with st.spinner("Mobility Tracking..."):
               mobility_data = collector.collect_advanced_mobility_intelligence()
           st.markdown(f"""
           <div class="luxury-card metric-luxury">
               <div class="metric-value">{len(mobility_data)}</div>
               <div class="metric-label">Aircraft Tracked</div>
               <div class="metric-delta status-operational">LIVE</div>
           </div>
           """, unsafe_allow_html=True)
   
   # COMPREHENSIVE ASSESSMENT
   assessment = analyzer.generate_comprehensive_assessment(reddit_data, news_data, market_data, mobility_data)
   
   # COMMAND METRICS DASHBOARD
   st.markdown("### ⬛ STRATEGIC COMMAND METRICS")
   
   col1, col2, col3, col4, col5, col6 = st.columns(6)
   
   with col1:
       threat_class = "status-critical" if assessment['threat_level'] == 'CRITICAL' else "status-elevated" if assessment['threat_level'] in ['HIGH', 'MEDIUM'] else "status-operational"
       if st.button(f"🔺 {assessment['threat_level']}", key="threat_btn", use_container_width=True):
           st.info(f"**Threat Level: {assessment['threat_level']}**\n\nBased on {assessment['critical_items']} critical items, market stress of {assessment['market_stress']['overall_stress']:.1f}/100, and {assessment['mobility_assessment']['critical_threats']} mobility threats.")
   
   with col2:
       if st.button(f"📊 {assessment['total_sources']}", key="sources_btn", use_container_width=True):
           st.info(f"**Intelligence Sources Active**\n\nReddit: {len(reddit_data)} posts\nNews: {len(news_data)} articles\nMarket: {len(market_data)} assets\nMobility: {len(mobility_data)} aircraft")
   
   with col3:
       critical_class = "status-critical" if assessment['critical_items'] > 10 else "status-elevated" if assessment['critical_items'] > 5 else "status-operational"
       if st.button(f"🚨 {assessment['critical_items']}", key="critical_btn", use_container_width=True):
           critical_items = [item for item in reddit_data + news_data if item.get('priority') == 'CRITICAL'][:5]
           critical_text = "\n".join([f"• {item['title'][:80]}..." for item in critical_items])
           st.info(f"**Critical Priority Items**\n\n{critical_text}")
   
   with col4:
       sentiment_class = "status-critical" if assessment['avg_sentiment'] < -0.3 else "status-elevated" if assessment['avg_sentiment'] < 0 else "status-operational"
       if st.button(f"📈 {assessment['avg_sentiment']:.3f}", key="sentiment_btn", use_container_width=True):
           st.info(f"**Sentiment Analysis**\n\nAverage: {assessment['avg_sentiment']:.3f}\nVolatility: {assessment['sentiment_volatility']:.3f}\nConfidence: {assessment['confidence_score']:.0f}%")
   
   with col5:
       stress_class = "status-critical" if assessment['market_stress']['overall_stress'] > 70 else "status-elevated" if assessment['market_stress']['overall_stress'] > 40 else "status-operational"
       if st.button(f"💹 {assessment['market_stress']['overall_stress']:.0f}", key="market_btn", use_container_width=True):
           components = assessment['market_stress']['components']
           st.info(f"**Market Stress Components**\n\nVIX: {components['vix_stress']:.0f}\nVolatility: {components['volatility_stress']:.0f}\nDefense: {components['defense_stress']:.0f}\nSafe Haven: {components['safe_haven_stress']:.0f}")
   
   with col6:
       mobility_class = "status-critical" if assessment['mobility_assessment']['threat_assessment'] == 'CRITICAL' else "status-elevated" if assessment['mobility_assessment']['threat_assessment'] == 'HIGH' else "status-operational"
       if st.button(f"✈️ {assessment['mobility_assessment']['total_aircraft']}", key="mobility_btn", use_container_width=True):
           mob = assessment['mobility_assessment']
           st.info(f"**Mobility Intelligence**\n\nTotal Aircraft: {mob['total_aircraft']}\nMilitary: {mob['military_aircraft']}\nCritical Threats: {mob['critical_threats']}\nThreat Level: {mob['threat_assessment']}")
   
   # MAIN INTELLIGENCE DASHBOARD
   tab1, tab2, tab3, tab4, tab5 = st.tabs([
       "🎯 STRATEGIC OVERVIEW",
       "📊 INTELLIGENCE OPERATIONS", 
       "💰 ECONOMIC WARFARE",
       "✈️ MOBILITY & ROUTES",
       "📋 THREAT ANALYSIS"
   ])
   
   with tab1:
       st.markdown("## 🎯 STRATEGIC INTELLIGENCE OVERVIEW")
       
       # Regional Intelligence Matrix
       st.markdown("### 🌍 REGIONAL INTELLIGENCE MATRIX")
       
       col1, col2 = st.columns([2, 1])
       
       with col1:
           regional_data = assessment['regional_activity']
           
           if regional_data:
               # Create enhanced regional chart
               regions_list = []
               for region, data in regional_data.items():
                   regions_list.append({
                       'Region': region,
                       'Critical': data['critical'],
                       'High': data['high'],
                       'Medium': data['medium'],
                       'Total': data['total'],
                       'Avg_Sentiment': data['avg_sentiment'],
                       'Trend': data['trend_direction']
                   })
               
               regions_df = pd.DataFrame(regions_list)
               
               fig = px.bar(
                   regions_df, 
                   x='Region', 
                   y=['Critical', 'High', 'Medium'], 
                   title="Intelligence Activity by Region",
                   color_discrete_map={
                       'Critical': '#e11d48', 
                       'High': '#f59e0b', 
                       'Medium': '#3b82f6'
                   },
                   height=500
               )
               
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='#e8e8e8',
                   title_font_size=16,
                   title_font_color='#d4af37',
                   xaxis=dict(title_font_color='#c4c4c4'),
                   yaxis=dict(title_font_color='#c4c4c4'),
                   legend=dict(font_color='#c4c4c4')
               )
               
               st.plotly_chart(fig, use_container_width=True)
       
       with col2:
           st.markdown("### 📊 THREAT ASSESSMENT GAUGE")
           
           # Enhanced threat gauge
           threat_values = {'CRITICAL': 100, 'HIGH': 75, 'MEDIUM': 50, 'LOW': 25}
           threat_value = threat_values[assessment['threat_level']]
           
           fig = go.Figure(go.Indicator(
               mode = "gauge+number+delta",
               value = threat_value,
               domain = {'x': [0, 1], 'y': [0, 1]},
               title = {'text': "THREAT LEVEL", 'font': {'color': '#d4af37', 'size': 16}},
               delta = {'reference': 50, 'font': {'color': '#e8e8e8'}},
               gauge = {
                   'axis': {'range': [None, 100], 'tickcolor': '#c4c4c4'},
                   'bar': {'color': "#e11d48"},
                   'steps': [
                       {'range': [0, 25], 'color': "#10b981"},
                       {'range': [25, 50], 'color': "#3b82f6"},
                       {'range': [50, 75], 'color': "#f59e0b"},
                       {'range': [75, 100], 'color': "#e11d48"}
                   ],
                   'threshold': {
                       'line': {'color': "#dc2626", 'width': 4},
                       'thickness': 0.75,
                       'value': 90
                   }
               }
           ))
           
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font_color='#e8e8e8',
               height=400
           )
           
           st.plotly_chart(fig, use_container_width=True)
       
       # Executive Intelligence Brief
       st.markdown("### 📋 EXECUTIVE INTELLIGENCE BRIEF")
       
       st.markdown(f"""
       <div class="intelligence-section">
           <div class="section-header">CLASSIFICATION: SENSITIVE</div>
           
           <p><strong>ASSESSMENT TIME:</strong> {assessment['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
           <p><strong>OVERALL THREAT LEVEL:</strong> <span class="{'status-critical' if assessment['threat_level'] == 'CRITICAL' else 'status-elevated' if assessment['threat_level'] in ['HIGH', 'MEDIUM'] else 'status-operational'}">{assessment['threat_level']}</span></p>
           <p><strong>CONFIDENCE SCORE:</strong> {assessment['confidence_score']:.0f}%</p>
           
           <h4>KEY FINDINGS:</h4>
           <ul>
               <li>Total Intelligence Sources: <strong>{assessment['total_sources']}</strong></li>
               <li>Critical Priority Items: <strong>{assessment['critical_items']}</strong></li>
               <li>High Priority Items: <strong>{assessment['high_priority_items']}</strong></li>
               <li>Average Sentiment Index: <strong>{assessment['avg_sentiment']:.3f}</strong></li>
               <li>Market Stress Level: <strong>{assessment['market_stress']['overall_stress']:.1f}/100</strong></li>
               <li>Aircraft Tracked: <strong>{assessment['mobility_assessment']['total_aircraft']}</strong></li>
               <li>Military Aircraft: <strong>{assessment['mobility_assessment']['military_aircraft']}</strong></li>
           </ul>
           
           <h4>REGIONAL HOTSPOTS:</h4>
       </div>
       """, unsafe_allow_html=True)
       
       for region, data in assessment['regional_activity'].items():
           if data['critical'] > 0:
               st.markdown(f"🔴 **{region}**: {data['critical']} critical, {data['high']} high priority items | Trend: {data['trend_direction'].upper()}")
           elif data['high'] > 3:
               st.markdown(f"🟡 **{region}**: {data['high']} high priority items | Trend: {data['trend_direction'].upper()}")
       
       # Emerging Topics Analysis
       if assessment['trend_analysis']['emerging_topics']:
           st.markdown("### 🔍 EMERGING TOPICS ANALYSIS")
           
           topics_df = pd.DataFrame(list(assessment['trend_analysis']['emerging_topics'].items()), 
                                  columns=['Topic', 'Frequency'])
           
           fig = px.bar(topics_df, x='Frequency', y='Topic', orientation='h',
                       title="Top Emerging Keywords",
                       color='Frequency',
                       color_continuous_scale='Reds')
           
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font_color='#e8e8e8',
               title_font_color='#d4af37',
               height=400
           )
           
           st.plotly_chart(fig, use_container_width=True)
   
   with tab2:
       st.markdown("## 📊 LIVE INTELLIGENCE OPERATIONS")
       
       # Filter controls
       col1, col2, col3 = st.columns(3)
       
       with col1:
           time_filter = st.selectbox("Time Range", ["Last 1 Hour", "Last 6 Hours", "Last 24 Hours", "All Time"])
       
       with col2:
           source_filter = st.selectbox("Source Filter", ["All Sources", "Reddit Only", "News Only", "High Credibility Only"])
       
       with col3:
           keyword_filter = st.text_input("Keyword Filter", placeholder="Enter keywords...")
       
       # Combine and filter intelligence data
       all_intelligence = []
       
       # Add Reddit data with filtering
       if 'Social Intelligence' in selected_sources:
           for item in reddit_data:
               if (item['priority'] in selected_priorities and 
                   item['region'] in selected_regions and
                   (not keyword_filter or keyword_filter.lower() in item['title'].lower())):
                   all_intelligence.append(item)
       
       # Add news data with filtering
       if 'News Intelligence' in selected_sources:
           for item in news_data:
               if (item['priority'] in selected_priorities and
                   (not keyword_filter or keyword_filter.lower() in item['title'].lower())):
                   all_intelligence.append(item)
       
       # Sort by intelligence score
       all_intelligence.sort(key=lambda x: x['intelligence_score'], reverse=True)
       
       st.markdown(f"### 📡 LIVE INTELLIGENCE FEED ({len(all_intelligence)} items)")
       
       # Category Intelligence Sections
       categories = {}
       for item in all_intelligence[:100]:  # Show top 100
           category = item.get('category', 'Unknown')
           if category not in categories:
               categories[category] = []
           categories[category].append(item)
       
       for category, items in categories.items():
           if items:
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-header">{category.upper()} INTELLIGENCE</div>
               """, unsafe_allow_html=True)
               
               for item in items[:10]:  # Show top 10 per category
                   priority_class = f"priority-{item['priority'].lower()}"
                   
                   # Enhanced item display
                   keywords_display = ', '.join(item.get('keywords', [])[:5])
                   sentiment_class = ("sentiment-positive" if item['sentiment_polarity'] > 0.1 else 
                                    "sentiment-negative" if item['sentiment_polarity'] < -0.1 else 
                                    "sentiment-neutral")
                   
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <div style="margin-bottom: 0.8rem;">
                           <span class="tag-luxury tag-{item['priority'].lower()}">{item['priority']}</span>
                           <span class="tag-luxury">Score: {item['intelligence_score']:.0f}</span>
                           <span class="tag-luxury">Source: {item['source']}</span>
                           {f'<span class="tag-luxury">Credibility: {item["credibility_score"]}</span>' if 'credibility_score' in item else ''}
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #d4af37;">{item['title']}</h4>
                       
                       {f'<p style="margin-bottom: 0.5rem; color: #c4c4c4;">{item["content_preview"]}</p>' if item.get('content_preview') else ''}
                       {f'<p style="margin-bottom: 0.5rem; color: #c4c4c4;">{item["summary"][:200]}...</p>' if item.get('summary') else ''}
                       
                       <div style="margin-bottom: 0.5rem;">
                           <span style="color: #e8e8e8;"><strong>Sentiment:</strong></span>
                           <span class="sentiment-score {sentiment_class}">{item['sentiment_polarity']:.3f}</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Region:</strong> {item.get('region', 'Global')}</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Time:</strong> {item['timestamp'].strftime('%H:%M')}</span>
                           {f'<span style="color: #e8e8e8; margin-left: 1rem;"><strong>Engagement:</strong> {item["score"]} ↑ {item["comments"]} 💬</span>' if 'score' in item else ''}
                       </div>
                       
                       {f'<p style="margin-bottom: 0.5rem;"><strong>Keywords:</strong> <span style="color: #f59e0b;">{keywords_display}</span></p>' if keywords_display else ''}
                       
                       <div style="margin-top: 0.8rem;">
                           <a href="{item['url']}" target="_blank" style="color: #d4af37; text-decoration: none; font-weight: 600;">🔗 VIEW SOURCE</a>
                           {f' | <span style="color: #c4c4c4;">Author: {item["author"]}</span>' if item.get('author') and item['author'] != 'Unknown' else ''}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
   
   with tab3:
       st.markdown("## 💰 ECONOMIC WARFARE INTELLIGENCE")
       
       if market_data:
           df_market = pd.DataFrame(market_data)
           
           # Market Performance Overview
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("### 📈 MARKET PERFORMANCE MATRIX")
               
               # Enhanced market performance chart
               colors = ['#e11d48' if x < -2 else '#f59e0b' if x < 0 else '#10b981' if x > 2 else '#3b82f6' for x in df_market['day_change_pct']]
               
               fig = go.Figure()
               fig.add_trace(go.Bar(
                   x=df_market['name'],
                   y=df_market['day_change_pct'],
                   marker_color=colors,
                   text=[f"{x:.2f}%" for x in df_market['day_change_pct']],
                   textposition='auto',
                   hovertemplate='<b>%{x}</b><br>Change: %{y:.2f}%<br>Risk: %{customdata}<extra></extra>',
                   customdata=df_market['risk_level']
               ))
               
               fig.update_layout(
                   title="Market Performance (%)",
                   xaxis_title="Assets",
                   yaxis_title="Change %",
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='#e8e8e8',
                   title_font_color='#d4af37',
                   height=500
               )
               fig.update_xaxis(tickangle=45)
               st.plotly_chart(fig, use_container_width=True)
           
           with col2:
               st.markdown("### 🛡️ DEFENSE SECTOR ANALYSIS")
               
               defense_sector = assessment['defense_sector_status']
               if defense_sector:
                   st.markdown(f"""
                   <div class="route-analysis">
                       <h4>Defense Sector Performance</h4>
                       <p><strong>Sector Performance:</strong> {defense_sector['sector_performance']:.2f}%</p>
                       <p><strong>Top Performer:</strong> {defense_sector['top_performer']}</p>
                       <p><strong>Worst Performer:</strong> {defense_sector['worst_performer']}</p>
                       <p><strong>Average Volatility:</strong> {defense_sector['avg_volatility']:.2f}%</p>
                       <p><strong>Risk Assessment:</strong> <span class="status-{'critical' if defense_sector['risk_assessment'] == 'HIGH' else 'elevated' if defense_sector['risk_assessment'] == 'MEDIUM' else 'operational'}">{defense_sector['risk_assessment']}</span></p>
                   </div>
                   """, unsafe_allow_html=True)
               
               # Market stress components
               st.markdown("### 🌡️ MARKET STRESS COMPONENTS")
               
               stress_components = assessment['market_stress']['components']
               stress_df = pd.DataFrame(list(stress_components.items()), columns=['Component', 'Stress Level'])
               
               fig = px.pie(stress_df, values='Stress Level', names='Component',
                          title="Market Stress Breakdown",
                          color_discrete_sequence=['#e11d48', '#f59e0b', '#3b82f6', '#10b981'])
               
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='#e8e8e8',
                   title_font_color='#d4af37'
               )
               
               st.plotly_chart(fig, use_container_width=True)
           
           # Detailed Market Intelligence
           st.markdown("### 📊 DETAILED MARKET INTELLIGENCE")
           
           # Market categories
           market_categories = df_market.groupby('type')
           
           for category, group in market_categories:
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-header">{category.upper().replace('_', ' ')} ASSETS</div>
               """, unsafe_allow_html=True)
               
               for _, asset in group.iterrows():
                   risk_class = f"tag-{asset['risk_level'].lower()}"
                   change_class = "sentiment-negative" if asset['day_change_pct'] < 0 else "sentiment-positive"
                   
                   st.markdown(f"""
                   <div class="intelligence-item">
                       <div style="margin-bottom: 0.8rem;">
                           <span class="tag-luxury {risk_class}">{asset['risk_level']} RISK</span>
                           <span class="tag-luxury">{asset['importance'].upper()}</span>
                           <span class="tag-luxury">{asset['region']}</span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #d4af37;">{asset['name']} ({asset['ticker']})</h4>
                       
                       <div style="margin-bottom: 0.5rem;">
                           <span style="color: #e8e8e8;"><strong>Current Price:</strong> ${asset['current_price']:.2f}</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Day Change:</strong></span>
                           <span class="sentiment-score {change_class}">{asset['day_change_pct']:.2f}%</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Week Change:</strong></span>
                           <span class="sentiment-score {change_class}">{asset['week_change_pct']:.2f}%</span>
                       </div>
                       
                       <div style="margin-bottom: 0.5rem;">
                           <span style="color: #e8e8e8;"><strong>Volatility:</strong> {asset['daily_volatility']:.2f}%</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Volume Ratio:</strong> {asset['volume_ratio']:.2f}x</span>
                           <span style="color: #e8e8e8; margin-left: 1rem;"><strong>RSI:</strong> {asset['rsi']:.0f}</span>
                       </div>
                       
                       {f'<p style="margin-bottom: 0.5rem;"><strong>Risk Factors:</strong> <span style="color: #f59e0b;">{", ".join(asset["risk_factors"])}</span></p>' if asset['risk_factors'] else ''}
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
       else:
           st.warning("⚠️ Market intelligence temporarily unavailable")
   
   with tab4:
       st.markdown("## ✈️ MOBILITY & ROUTE INTELLIGENCE")
       
       if mobility_data:
           # Mobility overview metrics
           mobility_stats = assessment['mobility_assessment']
           
           col1, col2, col3, col4 = st.columns(4)
           
           with col1:
               if st.button(f"✈️ {mobility_stats['total_aircraft']}", key="total_aircraft", use_container_width=True):
                   st.info(f"**Total Aircraft Tracked**\n\nCommercial: {mobility_stats['commercial_aircraft']}\nMilitary: {mobility_stats['military_aircraft']}\nOther: {mobility_stats['total_aircraft'] - mobility_stats['commercial_aircraft'] - mobility_stats['military_aircraft']}")
           
           with col2:
               if st.button(f"🚁 {mobility_stats['military_aircraft']}", key="military_aircraft", use_container_width=True):
                   military_aircraft = [a for a in mobility_data if 'Military' in a['aircraft_type']][:10]
                   military_text = "\n".join([f"• {a['callsign']} ({a['country']})" for a in military_aircraft])
                   st.info(f"**Military Aircraft**\n\n{military_text}")
           
           with col3:
               if st.button(f"🔺 {mobility_stats['critical_threats']}", key="critical_threats", use_container_width=True):
                   critical_aircraft = [a for a in mobility_data if a['threat_level'] == 'CRITICAL'][:5]
                   critical_text = "\n".join([f"• {a['callsign']} - {a['aircraft_type']}" for a in critical_aircraft])
                   st.info(f"**Critical Threats**\n\n{critical_text if critical_text else 'No critical threats detected'}")
           
           with col4:
               threat_color = "🔴" if mobility_stats['threat_assessment'] == 'CRITICAL' else "🟡" if mobility_stats['threat_assessment'] == 'HIGH' else "🟢"
               if st.button(f"{threat_color} {mobility_stats['threat_assessment']}", key="threat_assessment", use_container_width=True):
                   st.info(f"**Mobility Threat Assessment**\n\nLevel: {mobility_stats['threat_assessment']}\nAvg Altitude: {mobility_stats['average_altitude']:,.0f}m\nAvg Velocity: {mobility_stats['average_velocity']:.0f}m/s")
           
           # Enhanced route analysis
           st.markdown("### 🗺️ ADVANCED ROUTE INTELLIGENCE")
           
           # Create luxury map
           luxury_map = create_luxury_map(mobility_data)
           if luxury_map:
               st.components.v1.html(luxury_map._repr_html_(), height=700)
           
           # Route analysis sections
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("### 🛤️ ROUTE CATEGORY ANALYSIS")
               
               route_analysis = mobility_stats['route_analysis']
               if route_analysis:
                   route_df = pd.DataFrame(list(route_analysis.items()), columns=['Route Category', 'Aircraft Count'])
                   
                   fig = px.pie(route_df, values='Aircraft Count', names='Route Category',
                              title="Aircraft Distribution by Route",
                              color_discrete_sequence=['#d4af37', '#e11d48', '#3b82f6', '#10b981'])
                   
                   fig.update_layout(
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='#e8e8e8',
                       title_font_color='#d4af37'
                   )
                   
                   st.plotly_chart(fig, use_container_width=True)
           
           with col2:
               st.markdown("### 🌍 COUNTRY DISTRIBUTION")
               
               country_dist = mobility_stats['country_distribution']
               if country_dist:
                   country_df = pd.DataFrame(list(country_dist.items()), columns=['Country', 'Aircraft Count'])
                   
                   fig = px.bar(country_df, x='Aircraft Count', y='Country', orientation='h',
                              title="Top Countries by Aircraft",
                              color='Aircraft Count',
                              color_continuous_scale='Reds')
                   
                   fig.update_layout(
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='#e8e8e8',
                       title_font_color='#d4af37',
                       height=400
                   )
                   
                   st.plotly_chart(fig, use_container_width=True)
           
           # Detailed aircraft intelligence
           st.markdown("### 📊 DETAILED AIRCRAFT INTELLIGENCE")
           
           # Group by threat level
           threat_groups = {}
           for aircraft in mobility_data:
               threat = aircraft['threat_level']
               if threat not in threat_groups:
                   threat_groups[threat] = []
                   threat_groups[threat].append(aircraft)
           
           for threat_level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
               if threat_level in threat_groups:
                   aircraft_list = threat_groups[threat_level]
                   
                   st.markdown(f"""
                   <div class="intelligence-section">
                       <div class="section-header">{threat_level} THREAT AIRCRAFT ({len(aircraft_list)})</div>
                   """, unsafe_allow_html=True)
                   
                   for aircraft in aircraft_list[:15]:  # Show top 15 per threat level
                       threat_class = f"priority-{threat_level.lower()}"
                       
                       st.markdown(f"""
                       <div class="intelligence-item {threat_class}">
                           <div style="margin-bottom: 0.8rem;">
                               <span class="tag-luxury tag-{threat_level.lower()}">{threat_level}</span>
                               <span class="tag-luxury">{aircraft['aircraft_type']}</span>
                               <span class="tag-luxury">{aircraft['route_category']}</span>
                               <span class="tag-luxury">{'AIRBORNE' if not aircraft['on_ground'] else 'GROUNDED'}</span>
                           </div>
                           
                           <h4 style="margin-bottom: 0.5rem; color: #d4af37;">{aircraft['callsign']} - {aircraft['country']}</h4>
                           
                           <div style="margin-bottom: 0.5rem;">
                               <span style="color: #e8e8e8;"><strong>Position:</strong> {aircraft['latitude']:.4f}°, {aircraft['longitude']:.4f}°</span>
                               <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Altitude:</strong> {aircraft['altitude']:,}m</span>
                           </div>
                           
                           <div style="margin-bottom: 0.5rem;">
                               <span style="color: #e8e8e8;"><strong>Velocity:</strong> {aircraft['velocity']:.0f}m/s</span>
                               <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Heading:</strong> {aircraft['heading']:.0f}°</span>
                               <span style="color: #e8e8e8; margin-left: 1rem;"><strong>Last Contact:</strong> {datetime.fromtimestamp(aircraft['last_contact']).strftime('%H:%M:%S')}</span>
                           </div>
                       </div>
                       """, unsafe_allow_html=True)
                   
                   st.markdown("</div>", unsafe_allow_html=True)
       else:
           st.warning("⚠️ Mobility intelligence temporarily unavailable")
   
   with tab5:
       st.markdown("## 📋 COMPREHENSIVE THREAT ANALYSIS")
       
       # Multi-dimensional threat analysis
       col1, col2 = st.columns(2)
       
       with col1:
           st.markdown("### ⏱️ THREAT EVOLUTION TIMELINE")
           
           # Create threat timeline
           all_data_with_time = reddit_data + news_data
           all_data_with_time.sort(key=lambda x: x['timestamp'])
           
           if all_data_with_time:
               # Group by hour for timeline
               timeline_data = {}
               for item in all_data_with_time[-200:]:  # Last 200 items
                   hour_key = item['timestamp'].strftime('%Y-%m-%d %H:00')
                   if hour_key not in timeline_data:
                       timeline_data[hour_key] = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
                   timeline_data[hour_key][item['priority']] += 1
               
               timeline_df = pd.DataFrame([
                   {'Time': time, **counts} for time, counts in timeline_data.items()
               ])
               
               if not timeline_df.empty:
                   fig = px.area(
                       timeline_df, 
                       x='Time', 
                       y=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                       title="Intelligence Activity Timeline",
                       color_discrete_map={
                           'CRITICAL': '#e11d48',
                           'HIGH': '#f59e0b', 
                           'MEDIUM': '#3b82f6',
                           'LOW': '#10b981'
                       }
                   )
                   fig.update_layout(
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='#e8e8e8',
                       title_font_color='#d4af37',
                       height=400
                   )
                   fig.update_xaxis(tickangle=45)
                   st.plotly_chart(fig, use_container_width=True)
       
       with col2:
           st.markdown("### 🔗 MULTI-SOURCE CORRELATION")
           
           # Correlation analysis between different intelligence sources
           correlation_data = {
               'Reddit Activity': len(reddit_data),
               'News Volume': len(news_data),
               'Market Stress': assessment['market_stress']['overall_stress'],
               'Mobility Threats': assessment['mobility_assessment']['critical_threats'] * 10,
               'Sentiment Volatility': assessment['sentiment_volatility'] * 100
           }
           
           correlation_df = pd.DataFrame(list(correlation_data.items()), columns=['Metric', 'Value'])
           
           fig = px.bar(correlation_df, x='Metric', y='Value',
                      title="Intelligence Correlation Matrix",
                      color='Value',
                      color_continuous_scale='Reds')
           
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font_color='#e8e8e8',
               title_font_color='#d4af37',
               height=400
           )
           fig.update_xaxis(tickangle=45)
           st.plotly_chart(fig, use_container_width=True)
       
       # Advanced threat predictions
       st.markdown("### 🔮 PREDICTIVE THREAT ANALYSIS")
       
       st.markdown(f"""
       <div class="intelligence-section">
           <div class="section-header">PREDICTIVE INTELLIGENCE ASSESSMENT</div>
           
           <h4>Current Threat Trajectory: <span class="status-{'critical' if assessment['threat_level'] == 'CRITICAL' else 'elevated' if assessment['threat_level'] in ['HIGH', 'MEDIUM'] else 'operational'}">{assessment['threat_level']}</span></h4>
           
           <div class="analysis-grid">
               <div class="route-analysis">
                   <h4>📊 Statistical Analysis</h4>
                   <p><strong>Data Confidence:</strong> {assessment['confidence_score']:.0f}%</p>
                   <p><strong>Sample Size:</strong> {assessment['total_sources']} sources</p>
                   <p><strong>Critical Event Rate:</strong> {(assessment['critical_items']/max(1, assessment['total_sources'])*100):.1f}%</p>
                   <p><strong>Sentiment Stability:</strong> {'HIGH' if assessment['sentiment_volatility'] < 0.3 else 'MEDIUM' if assessment['sentiment_volatility'] < 0.6 else 'LOW'}</p>
               </div>
               
               <div class="route-analysis">
                   <h4>🎯 Risk Factors</h4>
                   <ul>
                       {'<li>High critical item volume</li>' if assessment['critical_items'] > 10 else ''}
                       {'<li>Elevated market stress</li>' if assessment['market_stress']['overall_stress'] > 60 else ''}
                       {'<li>Military aircraft activity</li>' if assessment['mobility_assessment']['military_aircraft'] > 20 else ''}
                       {'<li>Sentiment volatility</li>' if assessment['sentiment_volatility'] > 0.5 else ''}
                       {'<li>Defense sector anomalies</li>' if assessment.get('defense_sector_status', {}).get('risk_assessment') == 'HIGH' else ''}
                   </ul>
               </div>
               
               <div class="route-analysis">
                   <h4>📈 Trend Indicators</h4>
                   <p><strong>Intelligence Volume:</strong> {'INCREASING' if assessment['total_sources'] > 100 else 'STABLE'}</p>
                   <p><strong>Regional Escalation:</strong> {len([r for r, d in assessment['regional_activity'].items() if d['trend_direction'] == 'escalating'])} regions</p>
                   <p><strong>Market Correlation:</strong> {'STRONG' if assessment['market_stress']['overall_stress'] > 50 else 'WEAK'}</p>
                   <p><strong>Mobility Pressure:</strong> {assessment['mobility_assessment']['threat_assessment']}</p>
               </div>
           </div>
       </div>
       """, unsafe_allow_html=True)
       
       # Export and Action Buttons
       st.markdown("### 📤 INTELLIGENCE EXPORT & ACTIONS")
       
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           if st.button("📊 EXPORT STRATEGIC REPORT", use_container_width=True, key="export_strategic"):
               # Create comprehensive report
               report_data = {
                   'assessment': assessment,
                   'reddit_intelligence': reddit_data[:50],
                   'news_intelligence': news_data[:50],
                   'market_intelligence': market_data,
                   'mobility_intelligence': mobility_data[:100] if mobility_data else [],
                   'generated_at': datetime.now().isoformat(),
                   'classification': 'SENSITIVE'
               }
               
               json_report = json.dumps(report_data, default=str, indent=2)
               st.download_button(
                   label="📥 Download Strategic Intelligence Report",
                   data=json_report,
                   file_name=f"strategic_intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json",
                   use_container_width=True
               )
       
       with col2:
           if st.button("📋 EXPORT THREAT ASSESSMENT", use_container_width=True, key="export_threat"):
               # Create threat-focused summary
               threat_summary = {
                   'executive_summary': {
                       'threat_level': assessment['threat_level'],
                       'critical_items': assessment['critical_items'],
                       'market_stress': assessment['market_stress']['overall_stress'],
                       'mobility_threats': assessment['mobility_assessment']['critical_threats'],
                       'confidence_score': assessment['confidence_score']
                   },
                   'regional_hotspots': assessment['regional_activity'],
                   'defense_sector': assessment.get('defense_sector_status', {}),
                   'emerging_topics': assessment['trend_analysis']['emerging_topics'],
                   'timestamp': assessment['timestamp'].isoformat(),
                   'classification': 'SENSITIVE'
               }
               
               json_summary = json.dumps(threat_summary, default=str, indent=2)
               st.download_button(
                   label="📥 Download Threat Assessment",
                   data=json_summary,
                   file_name=f"threat_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json",
                   use_container_width=True
               )
       
       with col3:
           if st.button("📈 EXPORT MARKET ANALYSIS", use_container_width=True, key="export_market"):
               if market_data:
                   market_df = pd.DataFrame(market_data)
                   csv_data = market_df.to_csv(index=False)
                   st.download_button(
                       label="📥 Download Market Analysis",
                       data=csv_data,
                       file_name=f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                       mime="text/csv",
                       use_container_width=True
                   )
       
       with col4:
           if st.button("📄 EXPORT PDF REPORT", use_container_width=True, key="export_pdf"):
               # Create PDF report
               pdf_content = create_pdf_report(assessment, reddit_data, news_data, market_data)
               
               st.download_button(
                   label="📥 Download PDF Report",
                   data=pdf_content,
                   file_name=f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                   mime="text/html",
                   use_container_width=True
               )
       
       # Quick Action Buttons
       st.markdown("### ⚡ QUICK ACTIONS")
       
       col1, col2, col3 = st.columns(3)
       
       with col1:
           if st.button("🔔 SET ALERT THRESHOLD", use_container_width=True):
               st.info("Alert thresholds can be configured for:\n• Critical item count > 15\n• Market stress > 75\n• Military aircraft > 30\n• Threat level = CRITICAL")
       
       with col2:
           if st.button("📊 GENERATE BRIEFING", use_container_width=True):
               briefing_text = f"""
               **INTELLIGENCE BRIEFING - {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}**
               
               **OVERALL ASSESSMENT:** {assessment['threat_level']}
               **CONFIDENCE:** {assessment['confidence_score']:.0f}%
               
               **KEY METRICS:**
               • {assessment['critical_items']} critical intelligence items
               • {assessment['market_stress']['overall_stress']:.0f}/100 market stress
               • {assessment['mobility_assessment']['total_aircraft']} aircraft tracked
               
               **TOP PRIORITIES:**
               {chr(10).join([f"• {item['title'][:80]}..." for item in (reddit_data + news_data)[:5] if item.get('priority') == 'CRITICAL'])}
               """
               st.text_area("Intelligence Briefing", briefing_text, height=300)
       
       with col3:
           if st.button("🔄 FORCE FULL REFRESH", use_container_width=True):
               st.cache_data.clear()
               st.success("All data caches cleared. Refreshing...")
               time.sleep(2)
               st.rerun()
   
   # AUTO-REFRESH MECHANISM
   if auto_refresh:
       # Display countdown
       countdown_placeholder = st.empty()
       for remaining in range(300, 0, -1):  # 5 minutes countdown
           countdown_placeholder.info(f"⏰ Auto-refresh in {remaining//60}:{remaining%60:02d}")
           time.sleep(1)
       
       st.cache_data.clear()
       st.rerun()

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
   main()
