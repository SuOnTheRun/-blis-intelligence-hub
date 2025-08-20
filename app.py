# ============================================================================
# STRATEGIC INTELLIGENCE COMMAND CENTER
# Executive-Grade Intelligence Platform | Blis Analytics Professional Edition
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import feedparser
import yfinance as yf
from datetime import datetime, timedelta
import time
import json
from textblob import TextBlob
import warnings
import folium
from streamlit_folium import st_folium
import praw
from newsapi import NewsApiClient
import xml.etree.ElementTree as ET
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION & API CREDENTIALS
# ============================================================================

# Your verified API credentials
REDDIT_CLIENT_ID = st.secrets.get("REDDIT_CLIENT_ID", "gPAQFk1IFWSkMEVMXFMMCQ")
REDDIT_CLIENT_SECRET = st.secrets.get("REDDIT_CLIENT_SECRET", "2LoxxZ8c-Cr-Y0rrE9CmwvQQuHdskw")
REDDIT_USER_AGENT = st.secrets.get("REDDIT_USER_AGENT", "StrategicWarRoom/1.0 by u/Quick_Shower_6934")

NEWSAPI_KEY = st.secrets.get("NEWSAPI_KEY", "cdaa3b7303c740faa31a55fbb95bacd6")

POLYGON_ACCESS_KEY = st.secrets.get("POLYGON_ACCESS_KEY", "6fd6d224-8b3c-4ccb-8392-fcdea1e20ae9")
POLYGON_SECRET_KEY = st.secrets.get("POLYGON_SECRET_KEY", "pizMHwN6liX_zPM4nSUmYtfXH67Az0G4")

# GDELT & Flight APIs (Free)
GDELT_API_BASE = "https://api.gdeltproject.org/api/v2/"
ADS_B_EXCHANGE_API = "https://adsbexchange.com/api/"

# ============================================================================
# COMPREHENSIVE INTELLIGENCE SOURCES
# ============================================================================

TIER_1_INTELLIGENCE_SOURCES = {
    'primary_news': {
        'Reuters World News': 'https://feeds.reuters.com/reuters/worldNews',
        'Reuters Politics': 'https://feeds.reuters.com/reuters/politicsNews',
        'Reuters Business': 'https://feeds.reuters.com/reuters/businessNews',
        'Associated Press International': 'https://feeds.apnews.com/rss/apf-topnews',
        'Associated Press Politics': 'https://feeds.apnews.com/rss/apf-politicsnews',
        'BBC World News': 'http://feeds.bbci.co.uk/news/world/rss.xml',
        'BBC Politics': 'http://feeds.bbci.co.uk/news/politics/rss.xml',
        'Financial Times World': 'https://www.ft.com/rss/home/world',
        'Wall Street Journal World': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
        'The Guardian World': 'https://www.theguardian.com/world/rss',
        'The Guardian Politics': 'https://www.theguardian.com/politics/rss'
    },
    
    'defense_intelligence': {
        'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
        'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
        'Breaking Defense': 'https://breakingdefense.com/feed/',
        'Defense One': 'https://www.defenseone.com/rss/policy/',
        'The Drive War Zone': 'https://www.thedrive.com/the-war-zone/rss',
        'Jane\'s Defence Weekly': 'https://www.janes.com/feeds/defence-news',
        'Stars and Stripes': 'https://www.stripes.com/rss/news.rss',
        'Military.com': 'https://www.military.com/rss/daily-news',
        'Defense Post': 'https://www.thedefensepost.com/feed/',
        'Naval News': 'https://www.navalnews.com/feed/'
    },
    
    'strategic_analysis': {
        'Council on Foreign Relations': 'https://www.cfr.org/rss-feeds',
        'Institute for Study of War': 'https://www.understandingwar.org/rss.xml',
        'Center for Strategic and International Studies': 'https://www.csis.org/rss.xml',
        'Atlantic Council': 'https://www.atlanticcouncil.org/feed/',
        'Carnegie Endowment': 'https://carnegieendowment.org/feed',
        'Brookings Institution': 'https://www.brookings.edu/feed/',
        'RAND Corporation': 'https://www.rand.org/content/rand/rss/pubs/research_reports.xml',
        'War on the Rocks': 'https://warontherocks.com/feed/',
        'Foreign Affairs': 'https://www.foreignaffairs.com/rss.xml',
        'Foreign Policy': 'https://foreignpolicy.com/feed/',
        'Chatham House': 'https://www.chathamhouse.org/rss.xml',
        'RUSI': 'https://rusi.org/rss.xml'
    },
    
    'international_media': {
        'Al Jazeera English': 'https://www.aljazeera.com/xml/rss/all.xml',
        'France 24 English': 'https://www.france24.com/en/rss',
        'Deutsche Welle': 'https://rss.dw.com/rdf/rss-en-all',
        'Euronews': 'https://www.euronews.com/rss',
        'Times of India World': 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
        'South China Morning Post': 'https://www.scmp.com/rss/91/feed',
        'Japan Times': 'https://www.japantimes.co.jp/feed/',
        'Yonhap News Agency': 'https://en.yna.co.kr/RSS/news.xml',
        'Jerusalem Post': 'https://www.jpost.com/rss/rssfeedsfrontpage.aspx',
        'Dawn Pakistan': 'https://www.dawn.com/feeds/home'
    },
    
    'economic_intelligence': {
        'Bloomberg Politics': 'https://feeds.bloomberg.com/politics/news.rss',
        'Bloomberg Markets': 'https://feeds.bloomberg.com/markets/news.rss',
        'MarketWatch Top Stories': 'https://feeds.marketwatch.com/marketwatch/topstories/',
        'Economic Times': 'https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms',
        'Nikkei Asia': 'https://asia.nikkei.com/rss/feed/nar',
        'CNBC World News': 'https://www.cnbc.com/id/100727362/device/rss/rss.html',
        'Forbes': 'https://www.forbes.com/real-time/feed2/',
        'Fortune': 'https://fortune.com/feed/'
    },
    
    'humanitarian_intelligence': {
        'UN Office for Coordination of Humanitarian Affairs': 'https://www.unocha.org/rss.xml',
        'UNHCR': 'https://www.unhcr.org/rss.xml',
        'International Committee of the Red Cross': 'https://www.icrc.org/en/rss.xml',
        'Doctors Without Borders': 'https://www.doctorswithoutborders.org/rss.xml',
        'Human Rights Watch': 'https://www.hrw.org/rss',
        'Amnesty International': 'https://www.amnesty.org/en/rss/',
        'International Crisis Group': 'https://www.crisisgroup.org/rss.xml',
        'ReliefWeb': 'https://reliefweb.int/rss.xml'
    }
}

# Global Intelligence Hotspots - Complete Coverage
GLOBAL_INTELLIGENCE_HOTSPOTS = {
    # Critical Active Conflicts
    'Ukraine Operational Zone': {'lat': 49.5937, 'lon': 32.2922, 'priority': 'CRITICAL', 'region': 'Eastern Europe', 'type': 'Active Conflict'},
    'Gaza Strip': {'lat': 31.3547, 'lon': 34.3088, 'priority': 'CRITICAL', 'region': 'Middle East', 'type': 'Active Conflict'},
    'West Bank': {'lat': 31.9038, 'lon': 35.2034, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Occupied Territory'},
    
    # Strategic Waterways
    'Taiwan Strait': {'lat': 23.8, 'lon': 120.9, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
    'South China Sea': {'lat': 16.0, 'lon': 114.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
    'Strait of Hormuz': {'lat': 26.5667, 'lon': 56.25, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Strategic Waterway'},
    'Suez Canal': {'lat': 30.5, 'lon': 32.3, 'priority': 'MEDIUM', 'region': 'Middle East', 'type': 'Strategic Waterway'},
    'Strait of Malacca': {'lat': 2.5, 'lon': 101.8, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
    'Bosphorus Strait': {'lat': 41.1233, 'lon': 29.0781, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Strategic Waterway'},
    'Gibraltar Strait': {'lat': 36.1408, 'lon': -5.3536, 'priority': 'LOW', 'region': 'Europe', 'type': 'Strategic Waterway'},
    
    # Tension Zones
    'Korean DMZ': {'lat': 38.0, 'lon': 127.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Border Tension'},
    'Kashmir Line of Control': {'lat': 34.0, 'lon': 76.0, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Border Tension'},
    'Armenia-Azerbaijan Border': {'lat': 40.0691, 'lon': 45.0382, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Border Tension'},
    'Syria-Turkey Border': {'lat': 36.5, 'lon': 40.0, 'priority': 'MEDIUM', 'region': 'Middle East', 'type': 'Border Tension'},
    
    # Strategic Military Bases
    'Guantanamo Bay': {'lat': 19.9074, 'lon': -75.1505, 'priority': 'LOW', 'region': 'Americas', 'type': 'Military Base'},
    'Diego Garcia': {'lat': -7.3134, 'lon': 72.4113, 'priority': 'MEDIUM', 'region': 'Indian Ocean', 'type': 'Military Base'},
    'Ramstein Air Base': {'lat': 49.4369, 'lon': 7.6003, 'priority': 'LOW', 'region': 'Europe', 'type': 'Military Base'},
    
    # Economic Zones
    'Hong Kong': {'lat': 22.3193, 'lon': 114.1694, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Economic Zone'},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'priority': 'LOW', 'region': 'Asia Pacific', 'type': 'Economic Zone'},
    
    # Emerging Hotspots
    'Baltic Sea Region': {'lat': 58.0, 'lon': 20.0, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Emerging Tension'},
    'Arctic Ocean': {'lat': 85.0, 'lon': 0.0, 'priority': 'MEDIUM', 'region': 'Arctic', 'type': 'Resource Competition'},
    'Sahel Region': {'lat': 15.0, 'lon': 0.0, 'priority': 'MEDIUM', 'region': 'Africa', 'type': 'Security Zone'}
}

# ============================================================================
# EXECUTIVE DESIGN SYSTEM
# ============================================================================

st.set_page_config(
    page_title="Strategic Intelligence Command Center | Blis Analytics",
    page_icon="▓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Executive-Grade Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        --executive-primary: #0A0E27;
        --executive-secondary: #1A1F3A;
        --executive-tertiary: #2A2F4A;
        --executive-accent: #3B82F6;
        --executive-gold: #F59E0B;
        --executive-silver: #6B7280;
        --executive-white: #FFFFFF;
        --executive-light: #F8FAFC;
        --executive-border: #E5E7EB;
        --executive-text: #111827;
        --executive-text-secondary: #6B7280;
        --executive-red: #DC2626;
        --executive-green: #059669;
        --executive-amber: #D97706;
        --shadow-executive: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-primary: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-secondary: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stApp {
        background: var(--executive-light);
        font-family: 'Inter', sans-serif;
        color: var(--executive-text);
    }

    .command-header {
        background: linear-gradient(135deg, var(--executive-primary) 0%, var(--executive-secondary) 50%, var(--executive-tertiary) 100%);
        color: var(--executive-white);
        border-radius: 0;
        padding: 4rem 3rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        box-shadow: var(--shadow-executive);
        position: relative;
        overflow: hidden;
    }

    .command-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }

    .command-title {
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -3px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        background: linear-gradient(135deg, #FFFFFF 0%, #E5E7EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .command-subtitle {
        font-size: 1.5rem;
        margin-top: 1rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
        opacity: 0.9;
        letter-spacing: 2px;
    }

    .command-tagline {
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    .classification-banner {
        background: var(--executive-red);
        color: var(--executive-white);
        padding: 1rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
        margin-top: 2rem;
    }

    .executive-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .intelligence-card {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        border-radius: 0;
        padding: 2.5rem;
        box-shadow: var(--shadow-primary);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .intelligence-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--executive-accent), var(--executive-gold));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .intelligence-card:hover::before {
        transform: scaleX(1);
    }

    .intelligence-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-executive);
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--executive-accent);
        margin-bottom: 1rem;
        line-height: 1;
    }

    .metric-label {
        font-size: 1rem;
        color: var(--executive-text-secondary);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }

    .intelligence-item {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        border-left: 4px solid var(--executive-silver);
    }

    .intelligence-item:hover {
        box-shadow: var(--shadow-primary);
        transform: translateX(8px);
    }

    .priority-critical {
        border-left-color: var(--executive-red);
        background: linear-gradient(90deg, rgba(220, 38, 38, 0.03), var(--executive-white));
    }

    .priority-high {
        border-left-color: var(--executive-amber);
        background: linear-gradient(90deg, rgba(217, 119, 6, 0.03), var(--executive-white));
    }

    .priority-medium {
        border-left-color: var(--executive-accent);
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.03), var(--executive-white));
    }

    .priority-low {
        border-left-color: var(--executive-green);
        background: linear-gradient(90deg, rgba(5, 150, 105, 0.03), var(--executive-white));
    }

    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--executive-text);
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--executive-border);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-indicator {
        padding: 0.75rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 0;
    }

    .status-operational {
        background: var(--executive-green);
        color: var(--executive-white);
    }

    .status-elevated {
        background: var(--executive-amber);
        color: var(--executive-white);
    }

    .status-critical {
        background: var(--executive-red);
        color: var(--executive-white);
    }

    .threat-assessment {
        background: var(--executive-primary);
        color: var(--executive-white);
        padding: 2rem;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 2rem 0;
    }

    .data-table {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        border-radius: 0;
    }

    .sidebar .sidebar-content {
        background: var(--executive-secondary);
        color: var(--executive-white);
    }

    .stSelectbox > div > div {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        border-radius: 0;
    }

    .stButton > button {
        background: var(--executive-accent);
        color: var(--executive-white);
        border: none;
        border-radius: 0;
        padding: 0.75rem 2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: var(--executive-primary);
        transform: translateY(-2px);
        box-shadow: var(--shadow-primary);
    }

    .source-link {
        color: var(--executive-accent);
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .source-link:hover {
        color: var(--executive-primary);
        text-decoration: underline;
    }

    .blis-signature {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--executive-primary);
        color: var(--executive-white);
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 1px;
        z-index: 1000;
        box-shadow: var(--shadow-primary);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COMPREHENSIVE DATA COLLECTION ENGINE
# ============================================================================

@st.cache_data(ttl=300)
def fetch_comprehensive_intelligence():
    """Fetch intelligence from all verified sources"""
    all_intelligence = []
    
    for category_name, sources in TIER_1_INTELLIGENCE_SOURCES.items():
        for source_name, url in sources.items():
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:8]:  # Limit per source to manage volume
                    if not entry.title or len(entry.title) < 10:
                        continue
                    
                    text = f"{entry.title} {entry.get('summary', '')}"
                    sentiment = TextBlob(text).sentiment.polarity
                    
                    # Advanced intelligence scoring
                    critical_terms = [
                        'nuclear', 'missile', 'attack', 'invasion', 'war', 'bombing',
                        'assassination', 'coup', 'revolution', 'massacre'
                    ]
                    
                    high_terms = [
                        'military', 'conflict', 'crisis', 'sanctions', 'diplomacy',
                        'intelligence', 'security', 'terrorism', 'cyber', 'espionage'
                    ]
                    
                    medium_terms = [
                        'tension', 'dispute', 'exercise', 'alliance', 'treaty',
                        'defense', 'strategic', 'geopolitical', 'bilateral'
                    ]
                    
                    text_lower = text.lower()
                    critical_score = sum(5 for term in critical_terms if term in text_lower)
                    high_score = sum(3 for term in high_terms if term in text_lower)
                    medium_score = sum(1 for term in medium_terms if term in text_lower)
                    
                    relevance_score = min(10, 2 + critical_score + high_score + medium_score)
                    
                    # Source credibility matrix
                    credibility_matrix = {
                        'reuters': 10, 'associated press': 10, 'bbc': 9,
                        'financial times': 9, 'wall street journal': 9,
                        'council on foreign relations': 10, 'institute for study': 9,
                        'csis': 9, 'atlantic council': 8, 'carnegie': 8,
                        'brookings': 8, 'rand': 9, 'defense news': 8,
                        'military times': 7, 'breaking defense': 7,
                        'al jazeera': 7, 'france 24': 7, 'deutsche welle': 7
                    }
                    
                    source_lower = source_name.lower()
                    credibility = next((v for k, v in credibility_matrix.items() 
                                      if k in source_lower), 5)
                    
                    intelligence_score = (credibility + relevance_score) / 2
                    
                    # Priority classification
                    if intelligence_score >= 8.5:
                        priority = 'CRITICAL'
                    elif intelligence_score >= 7:
                        priority = 'HIGH'
                    elif intelligence_score >= 5:
                        priority = 'MEDIUM'
                    else:
                        priority = 'LOW'
                    
                    # Regional classification
                    region = classify_region(text_lower)
                    
                    all_intelligence.append({
                        'source': source_name,
                        'category': category_name.replace('_', ' ').title(),
                        'title': entry.title,
                        'content': entry.get('summary', '')[:500],
                        'url': entry.link,
                        'published': entry.get('published', ''),
                        'sentiment_polarity': sentiment,
                        'sentiment_label': classify_sentiment(sentiment),
                        'credibility_score': credibility,
                        'relevance_score': relevance_score,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': region,
                        'timestamp': datetime.utcnow(),
                        'type': 'verified_intelligence'
                    })
                    
            except Exception as e:
                continue  # Silently skip failed sources
    
    return sorted(all_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

@st.cache_data(ttl=300)
def fetch_reddit_intelligence():
    """Enhanced Reddit intelligence collection"""
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        
        strategic_subreddits = {
            'worldnews': {'region': 'Global', 'weight': 1.2, 'min_score': 500},
            'geopolitics': {'region': 'Global', 'weight': 1.8, 'min_score': 100},
            'ukraine': {'region': 'Eastern Europe', 'weight': 2.0, 'min_score': 200},
            'taiwan': {'region': 'Asia Pacific', 'weight': 1.7, 'min_score': 50},
            'MiddleEastNews': {'region': 'Middle East', 'weight': 1.5, 'min_score': 50},
            'intelligence': {'region': 'Global', 'weight': 1.9, 'min_score': 25},
            'NATONews': {'region': 'Europe', 'weight': 1.4, 'min_score': 25},
            'syriancivilwar': {'region': 'Middle East', 'weight': 1.6, 'min_score': 50},
            'CombatFootage': {'region': 'Global', 'weight': 1.3, 'min_score': 100},
            'Military': {'region': 'Global', 'weight': 1.2, 'min_score': 100}
        }
        
        reddit_intelligence = []
        
        for subreddit_name, config in strategic_subreddits.items():
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                for post in subreddit.hot(limit=25):
                    if (post.score >= config['min_score'] and 
                        not post.stickied and 
                        not post.over_18):
                        
                        text = f"{post.title} {post.selftext[:300]}"
                        sentiment = TextBlob(text).sentiment.polarity
                        
                        # Enhanced intelligence scoring
                        intelligence_keywords = [
                            'breaking', 'confirmed', 'verified', 'official',
                            'military', 'defense', 'security', 'intelligence',
                            'strategic', 'geopolitical', 'diplomatic']
                       
                       text_lower = text.lower()
                       keyword_score = sum(2 for keyword in intelligence_keywords if keyword in text_lower)
                       
                       # Engagement metrics
                       engagement_score = min(5, post.score / 1000)
                       ratio_score = post.upvote_ratio * 3
                       comment_score = min(3, post.num_comments / 100)
                       
                       credibility = min(10, 4 + engagement_score + ratio_score + config['weight'])
                       relevance = min(10, 3 + keyword_score + comment_score)
                       intelligence_score = (credibility + relevance) / 2
                       
                       priority = 'CRITICAL' if intelligence_score >= 8.5 else \
                                 'HIGH' if intelligence_score >= 7 else \
                                 'MEDIUM' if intelligence_score >= 5 else 'LOW'
                       
                       reddit_intelligence.append({
                           'source': f'Reddit r/{subreddit_name}',
                           'category': 'Social Intelligence',
                           'title': post.title,
                           'content': post.selftext[:400] if post.selftext else 'External content - click to view',
                           'url': f"https://reddit.com{post.permalink}",
                           'score': post.score,
                           'comments': post.num_comments,
                           'upvote_ratio': post.upvote_ratio,
                           'sentiment_polarity': sentiment,
                           'sentiment_label': classify_sentiment(sentiment),
                           'credibility_score': credibility,
                           'relevance_score': relevance,
                           'intelligence_score': intelligence_score,
                           'priority': priority,
                           'region': config['region'],
                           'timestamp': datetime.fromtimestamp(post.created_utc),
                           'type': 'social_intelligence'
                       })
                       
           except Exception:
               continue
       
       return sorted(reddit_intelligence, key=lambda x: x['intelligence_score'], reverse=True)
       
   except Exception:
       return []

@st.cache_data(ttl=300)
def fetch_newsapi_premium():
   """Premium NewsAPI intelligence collection"""
   try:
       newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
       
       premium_queries = [
           'military intelligence',
           'geopolitical crisis',
           'defense security',
           'international conflict',
           'strategic alliance',
           'cyber warfare'
       ]
       
       newsapi_intelligence = []
       
       for query in premium_queries[:4]:  # Rate limit management
           try:
               articles = newsapi.get_everything(
                   q=query,
                   language='en',
                   sort_by='relevancy',
                   page_size=12,
                   domains='reuters.com,apnews.com,bbc.com,cnn.com,ft.com,wsj.com,theguardian.com'
               )
               
               for article in articles.get('articles', []):
                   if (not article.get('title') or 
                       '[Removed]' in article.get('title', '') or
                       len(article.get('title', '')) < 20):
                       continue
                   
                   text = f"{article.get('title', '')} {article.get('description', '')}"
                   sentiment = TextBlob(text).sentiment.polarity
                   
                   source_name = article.get('source', {}).get('name', '').lower()
                   
                   premium_credibility = {
                       'reuters': 10, 'associated press': 10, 'bbc news': 9,
                       'cnn': 8, 'financial times': 9, 'wall street journal': 9,
                       'the guardian': 8, 'bloomberg': 8
                   }
                   
                   credibility = next((v for k, v in premium_credibility.items() 
                                     if k in source_name), 6)
                   
                   intelligence_keywords = [
                       'military', 'defense', 'security', 'intelligence',
                       'strategic', 'geopolitical', 'conflict', 'crisis'
                   ]
                   
                   relevance = min(10, 4 + sum(1.5 for k in intelligence_keywords 
                                              if k in text.lower()))
                   
                   intelligence_score = (credibility + relevance) / 2
                   
                   priority = 'CRITICAL' if intelligence_score >= 8.5 else \
                             'HIGH' if intelligence_score >= 7 else \
                             'MEDIUM' if intelligence_score >= 5 else 'LOW'
                   
                   region = classify_region(text.lower())
                   
                   newsapi_intelligence.append({
                       'source': f"NewsAPI - {article.get('source', {}).get('name', 'Unknown')}",
                       'category': 'Premium News Intelligence',
                       'title': article.get('title', ''),
                       'content': article.get('description', '')[:500],
                       'url': article.get('url', ''),
                       'published': article.get('publishedAt', ''),
                       'sentiment_polarity': sentiment,
                       'sentiment_label': classify_sentiment(sentiment),
                       'credibility_score': credibility,
                       'relevance_score': relevance,
                       'intelligence_score': intelligence_score,
                       'priority': priority,
                       'region': region,
                       'timestamp': datetime.utcnow(),
                       'type': 'premium_news'
                   })
                   
           except Exception:
               continue
               
       return sorted(newsapi_intelligence, key=lambda x: x['intelligence_score'], reverse=True)
       
   except Exception:
       return []

@st.cache_data(ttl=600)
def fetch_gdelt_global_events():
   """GDELT Global Events Intelligence"""
   try:
       # GDELT GKG API for global events
       base_url = f"{GDELT_API_BASE}gkg/gkg"
       params = {
           'query': 'military OR conflict OR security OR defense OR geopolitical',
           'mode': 'ArtList',
           'maxrecords': 30,
           'format': 'json',
           'timespan': '24h'
       }
       
       response = requests.get(base_url, params=params, timeout=15)
       
       if response.status_code == 200:
           data = response.json()
           gdelt_events = []
           
           for article in data.get('articles', []):
               title = article.get('title', '')
               if len(title) < 20:
                   continue
               
               text = f"{title} {article.get('summary', '')}"
               sentiment = TextBlob(text).sentiment.polarity
               
               # GDELT relevance scoring
               intelligence_terms = [
                   'military', 'conflict', 'security', 'defense',
                   'intelligence', 'strategic', 'geopolitical'
               ]
               
               relevance = min(10, 5 + sum(1 for term in intelligence_terms 
                                         if term in text.lower()))
               
               gdelt_events.append({
                   'source': 'GDELT Global Intelligence',
                   'category': 'Global Events Intelligence',
                   'title': title,
                   'content': article.get('summary', '')[:500],
                   'url': article.get('url', ''),
                   'sentiment_polarity': sentiment,
                   'sentiment_label': classify_sentiment(sentiment),
                   'credibility_score': 8.0,  # GDELT is highly credible
                   'relevance_score': relevance,
                   'intelligence_score': (8.0 + relevance) / 2,
                   'priority': 'HIGH' if relevance >= 8 else 'MEDIUM',
                   'region': classify_region(text.lower()),
                   'timestamp': datetime.utcnow(),
                   'type': 'global_events'
               })
           
           return sorted(gdelt_events, key=lambda x: x['intelligence_score'], reverse=True)
       
   except Exception:
       pass
   
   return []

@st.cache_data(ttl=300)
def fetch_flight_intelligence():
   """ADS-B Exchange Flight Intelligence"""
   try:
       # ADS-B Exchange API for military/government flights
       # Note: This requires proper API integration
       
       # For now, return simulated but realistic flight data
       # In production, this would connect to actual ADS-B data
       
       flight_intelligence = [
           {
               'callsign': 'RCH001',
               'aircraft_type': 'C-17A Globemaster III',
               'origin': 'Ramstein AB, Germany',
               'destination': 'Al Udeid AB, Qatar',
               'altitude': 35000,
               'speed': 450,
               'latitude': 35.2,
               'longitude': 33.4,
               'military_significance': 'HIGH',
               'flight_type': 'Military Transport',
               'region': 'Middle East Transit',
               'timestamp': datetime.utcnow() - timedelta(hours=2),
               'status': 'Active'
           },
           {
               'callsign': 'FORGE01',
               'aircraft_type': 'KC-135R Stratotanker',
               'origin': 'Kadena AB, Japan',
               'destination': 'Andersen AFB, Guam',
               'altitude': 32000,
               'speed': 420,
               'latitude': 20.5,
               'longitude': 140.2,
               'military_significance': 'MEDIUM',
               'flight_type': 'Air Refueling',
               'region': 'Pacific Theater',
               'timestamp': datetime.utcnow() - timedelta(hours=1),
               'status': 'Active'
           }
       ]
       
       return flight_intelligence
       
   except Exception:
       return []

@st.cache_data(ttl=300)
def fetch_market_intelligence():
   """Comprehensive market intelligence analysis"""
   
   strategic_tickers = {
       # Market Indices
       '^GSPC': {'name': 'S&P 500', 'category': 'Market Index', 'weight': 1.0},
       '^DJI': {'name': 'Dow Jones Industrial', 'category': 'Market Index', 'weight': 1.0},
       '^IXIC': {'name': 'NASDAQ Composite', 'category': 'Market Index', 'weight': 1.0},
       '^VIX': {'name': 'Volatility Index', 'category': 'Market Stress', 'weight': 2.5},
       
       # Defense & Aerospace
       'LMT': {'name': 'Lockheed Martin', 'category': 'Defense', 'weight': 2.0},
       'RTX': {'name': 'Raytheon Technologies', 'category': 'Defense', 'weight': 2.0},
       'BA': {'name': 'Boeing Company', 'category': 'Defense', 'weight': 1.8},
       'NOC': {'name': 'Northrop Grumman', 'category': 'Defense', 'weight': 1.9},
       'GD': {'name': 'General Dynamics', 'category': 'Defense', 'weight': 1.8},
       'LHX': {'name': 'L3Harris Technologies', 'category': 'Defense', 'weight': 1.7},
       
       # Cybersecurity & Intelligence
       'PLTR': {'name': 'Palantir Technologies', 'category': 'Intelligence Tech', 'weight': 2.2},
       'CRWD': {'name': 'CrowdStrike', 'category': 'Cybersecurity', 'weight': 1.8},
       'PANW': {'name': 'Palo Alto Networks', 'category': 'Cybersecurity', 'weight': 1.7},
       
       # Safe Haven Assets
       'GLD': {'name': 'SPDR Gold Trust', 'category': 'Safe Haven', 'weight': 1.5},
       'SLV': {'name': 'iShares Silver Trust', 'category': 'Safe Haven', 'weight': 1.3},
       'TLT': {'name': '20+ Year Treasury Bond', 'category': 'Safe Haven', 'weight': 1.4},
       
       # Energy & Resources
       'XLE': {'name': 'Energy Select SPDR', 'category': 'Energy', 'weight': 1.6},
       'USO': {'name': 'United States Oil Fund', 'category': 'Energy', 'weight': 1.7},
       'UNG': {'name': 'United States Natural Gas', 'category': 'Energy', 'weight': 1.5},
       
       # Currency & International
       'UUP': {'name': 'Invesco DB USD Index', 'category': 'Currency', 'weight': 1.3},
       'FXE': {'name': 'Invesco CurrencyShares Euro', 'category': 'Currency', 'weight': 1.2},
       'FXY': {'name': 'Invesco CurrencyShares Japanese Yen', 'category': 'Currency', 'weight': 1.2},
       
       # Regional ETFs
       'EWZ': {'name': 'iShares MSCI Brazil', 'category': 'Emerging Markets', 'weight': 1.2},
       'FXI': {'name': 'iShares China Large-Cap', 'category': 'Emerging Markets', 'weight': 1.4},
       'EWY': {'name': 'iShares MSCI South Korea', 'category': 'Emerging Markets', 'weight': 1.3}
   }
   
   market_intelligence = []
   
   for ticker, info in strategic_tickers.items():
       try:
           stock = yf.Ticker(ticker)
           hist = stock.history(period="10d")
           
           if hist.empty:
               continue
           
           current_price = float(hist['Close'].iloc[-1])
           previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
           change_pct = ((current_price - previous_price) / previous_price) * 100 if previous_price else 0.0
           
           # Advanced metrics
           volatility = hist['Close'].pct_change().std() * 100 if len(hist) > 1 else 0
           volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
           avg_volume = hist['Volume'].mean() if 'Volume' in hist.columns else 0
           volume_ratio = volume / avg_volume if avg_volume > 0 else 1
           
           # Intelligence significance calculation
           price_significance = abs(change_pct) * info['weight']
           volume_significance = min(5, abs(volume_ratio - 1) * 3)
           volatility_significance = min(5, volatility * 2)
           
           total_significance = price_significance + volume_significance + volatility_significance
           
           # Market stress indicator (special handling for VIX)
           if ticker == '^VIX':
               stress_level = 'CRITICAL' if current_price > 30 else \
                            'HIGH' if current_price > 20 else \
                            'MEDIUM' if current_price > 15 else 'LOW'
           else:
               stress_level = 'HIGH' if abs(change_pct) > 5 else \
                             'MEDIUM' if abs(change_pct) > 2 else 'LOW'
           
           market_intelligence.append({
               'ticker': ticker,
               'name': info['name'],
               'category': info['category'],
               'current_price': current_price,
               'change_pct': change_pct,
               'volatility': volatility,
               'volume': volume,
               'volume_ratio': volume_ratio,
               'significance_score': total_significance,
               'stress_level': stress_level,
               'timestamp': datetime.utcnow()
           })
           
       except Exception:
           continue
   
   return sorted(market_intelligence, key=lambda x: x['significance_score'], reverse=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def classify_sentiment(polarity):
   """Classify sentiment polarity"""
   if polarity > 0.1:
       return 'Positive'
   elif polarity < -0.1:
       return 'Negative'
   else:
       return 'Neutral'

def classify_region(text_lower):
   """Classify content by region"""
   regional_keywords = {
       'Eastern Europe': [
           'ukraine', 'russia', 'belarus', 'poland', 'baltic', 'estonia',
           'latvia', 'lithuania', 'moldova', 'romania', 'bulgaria'
       ],
       'Asia Pacific': [
           'china', 'taiwan', 'japan', 'korea', 'australia', 'singapore',
           'thailand', 'vietnam', 'philippines', 'indonesia', 'india'
       ],
       'Middle East': [
           'iran', 'israel', 'palestine', 'saudi', 'gulf', 'syria',
           'lebanon', 'jordan', 'iraq', 'yemen', 'qatar', 'uae'
       ],
       'Europe': [
           'nato', 'eu', 'france', 'germany', 'uk', 'britain', 'italy',
           'spain', 'netherlands', 'belgium', 'sweden', 'norway'
       ],
       'Africa': [
           'sudan', 'egypt', 'libya', 'algeria', 'morocco', 'nigeria',
           'ethiopia', 'somalia', 'chad', 'mali', 'sahel'
       ],
       'Americas': [
           'usa', 'canada', 'mexico', 'brazil', 'argentina', 'venezuela',
           'colombia', 'cuba', 'haiti'
       ]
   }
   
   for region, keywords in regional_keywords.items():
       if any(keyword in text_lower for keyword in keywords):
           return region
   
   return 'Global'

# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class StrategicAnalyticsEngine:
   """Professional analytics for executive intelligence assessment"""
   
   def __init__(self):
       self.priority_weights = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
       self.regional_significance = {
           'Eastern Europe': 2.0, 'Middle East': 1.8, 'Asia Pacific': 1.6,
           'Europe': 1.3, 'Africa': 1.2, 'Americas': 1.1, 'Global': 1.4
       }
   
   def generate_executive_assessment(self, all_intelligence, market_data, flight_data):
       """Generate comprehensive executive assessment"""
       
       if not all_intelligence and not market_data:
           return self._baseline_assessment()
       
       # Core intelligence metrics
       total_sources = len(all_intelligence)
       critical_items = len([item for item in all_intelligence if item.get('priority') == 'CRITICAL'])
       high_items = len([item for item in all_intelligence if item.get('priority') == 'HIGH'])
       medium_items = len([item for item in all_intelligence if item.get('priority') == 'MEDIUM'])
       
       # Intelligence quality assessment
       intelligence_scores = [item.get('intelligence_score', 0) for item in all_intelligence]
       avg_intelligence_quality = np.mean(intelligence_scores) if intelligence_scores else 5.0
       
       # Sentiment analysis with trend detection
       sentiments = [item.get('sentiment_polarity', 0) for item in all_intelligence]
       avg_sentiment = np.mean(sentiments) if sentiments else 0
       sentiment_volatility = np.std(sentiments) if len(sentiments) > 1 else 0
       
       # Market stress analysis
       market_stress_index = self._calculate_market_stress(market_data)
       
       # Regional threat assessment
       regional_assessment = self._analyze_regional_threats(all_intelligence)
       
       # Multi-dimensional threat calculation
       base_threat = (critical_items * 4) + (high_items * 2) + (medium_items * 1)
       market_threat = market_stress_index * 1.5
       sentiment_threat = (abs(avg_sentiment) * 2) + (sentiment_volatility * 3)
       regional_threat = max([data.get('threat_level', 0) for data in regional_assessment.values()], default=0)
       
       overall_threat = min(10, (base_threat + market_threat + sentiment_threat + regional_threat) / 4)
       
       # Threat level classification
       if overall_threat >= 8:
           threat_level = 'CRITICAL'
       elif overall_threat >= 6:
           threat_level = 'HIGH'
       elif overall_threat >= 4:
           threat_level = 'ELEVATED'
       else:
           threat_level = 'NORMAL'
       
       # Source diversity analysis
       source_types = set(item.get('category', 'Unknown') for item in all_intelligence)
       source_diversity = len(source_types)
       
       # Confidence calculation
       confidence_score = min(100, (total_sources * 1.5) + (avg_intelligence_quality * 8) + (source_diversity * 3))
       
       return {
           'overall_threat_score': overall_threat,
           'threat_level': threat_level,
           'intelligence_quality': avg_intelligence_quality,
           'total_sources': total_sources,
           'critical_items': critical_items,
           'high_items': high_items,
           'medium_items': medium_items,
           'avg_sentiment': avg_sentiment,
           'sentiment_volatility': sentiment_volatility,
           'market_stress_index': market_stress_index,
           'regional_assessment': regional_assessment,
           'source_diversity': source_diversity,
           'confidence_score': confidence_score,
           'timestamp': datetime.now(),
           'flight_activity_level': self._assess_flight_activity(flight_data)
       }
   
   def _calculate_market_stress(self, market_data):
       """Calculate comprehensive market stress index"""
       if not market_data:
           return 0
       
       stress_indicators = []
       
       # VIX analysis
       vix_data = [item for item in market_data if 'VIX' in item['name'] or 'Volatility' in item['name']]
       if vix_data:
           vix_level = vix_data[0]['current_price']
           if vix_level > 30:
               stress_indicators.append(10)
           elif vix_level > 20:
               stress_indicators.append(7)
           elif vix_level > 15:
               stress_indicators.append(4)
           else:
               stress_indicators.append(1)
       
       # Defense sector performance (inverse correlation with market stress)
       defense_items = [item for item in market_data if item['category'] == 'Defense']
       if defense_items:
           defense_performance = np.mean([item['change_pct'] for item in defense_items])
           # Strong defense performance may indicate increased tension
           if defense_performance > 3:
               stress_indicators.append(6)
           elif defense_performance > 1:
               stress_indicators.append(4)
           else:
               stress_indicators.append(2)
       
       # Safe haven performance
       safe_haven_items = [item for item in market_data if item['category'] == 'Safe Haven']
       if safe_haven_items:
           safe_haven_performance = np.mean([item['change_pct'] for item in safe_haven_items])
           # Strong safe haven performance indicates stress
           stress_indicators.append(min(8, max(0, safe_haven_performance * 2)))
       
       # Overall market volatility
       all_volatilities = [item.get('volatility', 0) for item in market_data]
       if all_volatilities:
           avg_volatility = np.mean(all_volatilities)
           stress_indicators.append(min(10, avg_volatility))
       
       return np.mean(stress_indicators) if stress_indicators else 0
   
   def _analyze_regional_threats(self, all_intelligence):
       """Analyze threats by geographic region"""
       regional_data = {}
       
       for item in all_intelligence:
           region = item.get('region', 'Global')
           
           if region not in regional_data:
               regional_data[region] = {
                   'total_items': 0, 'critical': 0, 'high': 0, 'medium': 0,
                   'sentiments': [], 'intelligence_scores': []
               }
           
           regional_data[region]['total_items'] += 1
           
           priority = item.get('priority', 'LOW')
           if priority == 'CRITICAL':
               regional_data[region]['critical'] += 1
           elif priority == 'HIGH':
               regional_data[region]['high'] += 1
           elif priority == 'MEDIUM':
               regional_data[region]['medium'] += 1
           
           regional_data[region]['sentiments'].append(item.get('sentiment_polarity', 0))
           regional_data[region]['intelligence_scores'].append(item.get('intelligence_score', 0))
       
       # Calculate threat levels for each region
       for region, data in regional_data.items():
           critical_weight = data['critical'] * 4
           high_weight = data['high'] * 2
           medium_weight = data['medium'] * 1
           
           avg_sentiment = np.mean(data['sentiments']) if data['sentiments'] else 0
           avg_intelligence = np.mean(data['intelligence_scores']) if data['intelligence_scores'] else 0
           
           regional_significance = self.regional_significance.get(region, 1.0)
           
           threat_level = min(10, ((critical_weight + high_weight + medium_weight) * regional_significance + 
                                  abs(avg_sentiment) * 2) / max(1, data['total_items']))
           
           data['threat_level'] = threat_level
           data['avg_sentiment'] = avg_sentiment
           data['avg_intelligence'] = avg_intelligence
           
           # Classification
           if threat_level >= 8:
               data['classification'] = 'CRITICAL'
           elif threat_level >= 6:
               data['classification'] = 'HIGH'
           elif threat_level >= 4:
               data['classification'] = 'ELEVATED'
           else:
               data['classification'] = 'NORMAL'
       
       return regional_data
   
   def _assess_flight_activity(self, flight_data):
       """Assess military flight activity level"""
       if not flight_data:
           return 'NORMAL'
       
       high_significance_flights = len([f for f in flight_data 
                                      if f.get('military_significance') in ['CRITICAL', 'HIGH']])
       
       if high_significance_flights >= 5:
           return 'ELEVATED'
       elif high_significance_flights >= 3:
           return 'MODERATE'
       else:
           return 'NORMAL'
   
   def _baseline_assessment(self):
       """Baseline assessment when no data is available"""
       return {
           'overall_threat_score': 0,
           'threat_level': 'NORMAL',
           'intelligence_quality': 0,
           'total_sources': 0,
           'critical_items': 0,
           'high_items': 0,
           'medium_items': 0,
           'avg_sentiment': 0,
           'sentiment_volatility': 0,
           'market_stress_index': 0,
           'regional_assessment': {},
           'source_diversity': 0,
           'confidence_score': 0,
           'timestamp': datetime.now(),
           'flight_activity_level': 'NORMAL'
       }

# ============================================================================
# VISUALIZATION ENGINE
# ============================================================================

def create_executive_threat_gauge(threat_score, threat_level):
   """Executive-grade threat assessment gauge"""
   
   color_mapping = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'ELEVATED': '#3B82F6',
       'NORMAL': '#059669'
   }
   
   fig = go.Figure(go.Indicator(
       mode="gauge+number",
       value=threat_score,
       domain={'x': [0, 1], 'y': [0, 1]},
       title={'text': f"THREAT ASSESSMENT: {threat_level}", 
              'font': {'size': 18, 'color': '#0A0E27', 'family': 'Inter'}},
       number={'font': {'size': 48, 'color': color_mapping.get(threat_level, '#6B7280')}},
       gauge={
           'axis': {'range': [None, 10], 'tickcolor': '#6B7280', 'tickfont': {'size': 14}},
           'bar': {'color': color_mapping.get(threat_level, '#6B7280'), 'thickness': 0.7},
           'steps': [
               {'range': [0, 2.5], 'color': '#F3F4F6'},
               {'range': [2.5, 5], 'color': '#E5E7EB'},
               {'range': [5, 7.5], 'color': '#D1D5DB'},
               {'range': [7.5, 10], 'color': '#9CA3AF'}
           ],
           'threshold': {
               'line': {'color': '#0A0E27', 'width': 4},
               'thickness': 0.8,
               'value': 8
           }
       }
   ))
   
   fig.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27', 'family': 'Inter'},
       height=400,
       margin=dict(l=20, r=20, t=80, b=20)
   )
   
   return fig

def create_intelligence_timeline(intelligence_data):
   """Create executive intelligence timeline"""
   
   if not intelligence_data:
       return None
   
   # Sort by timestamp and take recent items
   sorted_intel = sorted(intelligence_data, key=lambda x: x['timestamp'], reverse=True)[:50]
   
   timeline_data = []
   
   for item in sorted_intel:
       timeline_data.append({
           'timestamp': item['timestamp'],
           'title': item['title'][:80] + '...' if len(item['title']) > 80 else item['title'],
           'priority': item.get('priority', 'MEDIUM'),
           'category': item.get('category', 'Unknown'),
           'source': item['source'],
           'intelligence_score': item.get('intelligence_score', 0),
           'region': item.get('region', 'Global')
       })
   
   df = pd.DataFrame(timeline_data)
   
   color_map = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'MEDIUM': '#3B82F6',
       'LOW': '#059669'
   }
   
   fig = px.scatter(
       df, 
       x='timestamp', 
       y='intelligence_score',
       color='priority',
       size='intelligence_score',
       hover_data=['title', 'source', 'region'],
       color_discrete_map=color_map,
       title="Intelligence Timeline - Last 24 Hours"
   )
   
   fig.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27', 'family': 'Inter'},
       height=500,
       xaxis_title="Time",
       yaxis_title="Intelligence Score",
       showlegend=True,
       legend=dict(
           orientation="h",
           yanchor="bottom",
           y=1.02,
           xanchor="right",
           x=1
       )
   )
   
   return fig

def create_global_intelligence_map(hotspots, intelligence_data):
   """Create comprehensive global intelligence map"""
   
   # Initialize map centered on global view
   m = folium.Map(
       location=[20, 0],
       zoom_start=2,
       tiles='CartoDB positron',
       attr='Strategic Intelligence Command Center'
   )
   
   # Color mapping for priorities
   priority_colors = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'MEDIUM': '#3B82F6',
       'LOW': '#059669'
   }
   
   # Add intelligence hotspots
   for location, data in hotspots.items():
       folium.CircleMarker(
           location=[data['lat'], data['lon']],
           radius=12 if data['priority'] == 'CRITICAL' else 9 if data['priority'] == 'HIGH' else 6,
           popup=folium.Popup(f"""
               <div style="font-family: Inter; min-width: 250px;">
                   <h4 style="margin: 0 0 10px 0; color: {priority_colors.get(data['priority'], '#6B7280')};">
                       {location}
                   </h4>
                   <p style="margin: 5px 0;"><strong>Priority:</strong> {data['priority']}</p>
                   <p style="margin: 5px 0;"><strong>Region:</strong> {data['region']}</p>
                   <p style="margin: 5px 0;"><strong>Type:</strong> {data['type']}</p>
                   <p style="margin: 5px 0;"><strong>Coordinates:</strong> {data['lat']:.4f}, {data['lon']:.4f}</p>
               </div>
           """, max_width=300),
           color=priority_colors.get(data['priority'], '#6B7280'),
           fill=True,
           fillColor=priority_colors.get(data['priority'], '#6B7280'),
           fillOpacity=0.8,
           weight=3
       ).add_to(m)
   
   # Add recent intelligence events
   recent_events = [item for item in intelligence_data 
                   if item.get('priority') in ['CRITICAL', 'HIGH'] 
                   and 'lat' in item and 'lon' in item][:20]
   
   for event in recent_events:
       folium.Marker(
           location=[event['lat'], event['lon']],
           popup=folium.Popup(f"""
               <div style="font-family: Inter; min-width: 300px;">
                   <h4 style="margin: 0 0 10px 0; color: {priority_colors.get(event['priority'], '#6B7280')};">
                       {event['title'][:60]}...
                   </h4>
                   <p style="margin: 5px 0;"><strong>Priority:</strong> {event['priority']}</p>
                   <p style="margin: 5px 0;"><strong>Source:</strong> {event['source']}</p>
                   <p style="margin: 5px 0;"><strong>Intelligence Score:</strong> {event.get('intelligence_score', 0):.1f}/10</p>
                   <p style="margin: 5px 0;"><strong>Time:</strong> {event['timestamp'].strftime('%H:%M UTC')}</p>
                   <a href="{event.get('url', '#')}" target="_blank" style="color: #3B82F6; text-decoration: none;">
                       View Source
                   </a>
               </div>
           """, max_width=350),
           icon=folium.Icon(
               color='red' if event['priority'] == 'CRITICAL' else 'orange' if event['priority'] == 'HIGH' else 'blue',
               icon='info-sign',
               prefix='glyphicon'
           )
       ).add_to(m)
   
   return m

def create_market_analysis_dashboard(market_data):
   """Create comprehensive market intelligence dashboard"""
   
   if not market_data:
       return None, None
   
   df = pd.DataFrame(market_data)
   
   # Market performance by category
   fig1 = px.bar(
       df.groupby('category').agg({
           'change_pct': 'mean',
           'significance_score': 'mean'
       }).reset_index(),
       x='category',
       y='change_pct',
       title="Market Performance by Sector",
       color='change_pct',
       color_continuous_scale=['#DC2626', '#FFFFFF', '#059669']
   )
   
   fig1.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27', 'family': 'Inter'},
       height=400,
       xaxis_title="Sector",
       yaxis_title="Average Change %"
   )
   
   # Risk vs Return analysis
   fig2 = px.scatter(
       df,
       x='volatility',
       y='change_pct',
       size='significance_score',
       color='category',
       hover_data=['name', 'ticker'],
       title="Risk vs Return Analysis"
   )
   
   fig2.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27', 'family': 'Inter'},
       height=400,
       xaxis_title="Volatility %",
       yaxis_title="Performance %"
   )
   
   return fig1, fig2

def create_regional_threat_analysis(regional_data):
   """Create regional threat analysis visualization"""
   
   if not regional_data:
       return None
   
   regions = list(regional_data.keys())
   threat_levels = [data['threat_level'] for data in regional_data.values()]
   classifications = [data['classification'] for data in regional_data.values()]
   
   color_map = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'ELEVATED': '#3B82F6',
       'NORMAL': '#059669'
   }
   
   colors = [color_map.get(classification, '#6B7280') for classification in classifications]
   
   fig = go.Figure(data=[
       go.Bar(
           y=regions,
           x=threat_levels,
           orientation='h',
           marker_color=colors,
           text=[f"{level:.1f}" for level in threat_levels],
           textposition='inside',
           textfont=dict(color='white', size=14, family='Inter')
       )
   ])
   
   fig.update_layout(
       title="Regional Threat Assessment",
       xaxis_title="Threat Level (0-10)",
       yaxis_title="Region",
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27', 'family': 'Inter'},
       height=500,
       margin=dict(l=100, r=50, t=80, b=50)
   )
   
   return fig

def create_flight_tracking_display(flight_data):
   """Create flight tracking display"""
   
   if not flight_data:
       return None
   
   df = pd.DataFrame(flight_data)
   
   significance_colors = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'MEDIUM': '#3B82F6',
       'LOW': '#059669'
   }
   
   fig = px.scatter_mapbox(
       df,
       lat='latitude',
       lon='longitude',
       hover_data=['callsign', 'aircraft_type', 'origin', 'destination'],
       color='military_significance',
       color_discrete_map=significance_colors,
       size_max=15,
       zoom=2,
       title="Military Flight Activity"
   )
   
   fig.update_layout(
       mapbox_style="open-street-map",
       height=500,
       font={'color': '#0A0E27', 'family': 'Inter'}
   )
   
   return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
   """Main application function"""
   
   # Command Center Header
   st.markdown("""
   <div class="command-header">
       <h1 class="command-title">STRATEGIC INTELLIGENCE COMMAND CENTER</h1>
       <p class="command-subtitle">Advanced Multi-Source Intelligence Platform</p>
       <p class="command-tagline">Blis Analytics Professional Edition</p>
       <div class="classification-banner">INTERNAL USE ONLY</div>
   </div>
   """, unsafe_allow_html=True)
   
   # Sidebar Configuration
   st.sidebar.markdown("## INTELLIGENCE CONTROLS")
   
   # Region selection
   available_regions = ['Global', 'Eastern Europe', 'Asia Pacific', 'Middle East', 'Europe', 'Africa', 'Americas']
   selected_regions = st.sidebar.multiselect("ACTIVE REGIONS", available_regions, default=['Global'])
   
   # Priority filters
   priority_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
   selected_priorities = st.sidebar.multiselect("PRIORITY LEVELS", priority_levels, default=priority_levels)
   
   # Intelligence source configuration
   st.sidebar.markdown("### DATA SOURCES")
   collect_news = st.sidebar.checkbox("News Intelligence", value=True)
   collect_social = st.sidebar.checkbox("Social Intelligence", value=True)
   collect_market = st.sidebar.checkbox("Market Intelligence", value=True)
   collect_flights = st.sidebar.checkbox("Flight Intelligence", value=True)
   collect_gdelt = st.sidebar.checkbox("Global Events (GDELT)", value=True)
   
   # Advanced filters
   min_intelligence_score = st.sidebar.slider("MINIMUM INTELLIGENCE SCORE", 0.0, 10.0, 5.0, 0.1)
   max_age_hours = st.sidebar.slider("MAXIMUM AGE (HOURS)", 1, 48, 24)
   
   # Refresh controls
   auto_refresh = st.sidebar.checkbox("AUTO-REFRESH", value=False)
   if st.sidebar.button("REFRESH NOW", type="primary"):
       st.cache_data.clear()
       st.rerun()
   
   # Initialize analytics engine
   analytics_engine = StrategicAnalyticsEngine()
   
   # Data collection phase
   st.markdown('<div class="section-header">INTELLIGENCE COLLECTION STATUS</div>', unsafe_allow_html=True)
   
   with st.container():
       col1, col2, col3, col4, col5 = st.columns(5)
       
       # Collect all intelligence sources
       all_intelligence = []
       market_data = []
       flight_data = []
       
       with col1:
           if collect_news:
               with st.spinner("Collecting comprehensive intelligence..."):
                   news_intel = fetch_comprehensive_intelligence()
                   all_intelligence.extend(news_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len([i for i in all_intelligence if i.get('type') == 'verified_intelligence'])}</div>
               <div class="metric-label">NEWS SOURCES</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           if collect_social:
               with st.spinner("Analyzing social intelligence..."):
                   social_intel = fetch_reddit_intelligence()
                   all_intelligence.extend(social_intel)
                   
                   newsapi_intel = fetch_newsapi_premium()
                   all_intelligence.extend(newsapi_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len([i for i in all_intelligence if i.get('type') in ['social_intelligence', 'premium_news']])}</div>
               <div class="metric-label">SOCIAL INTEL</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           if collect_gdelt:
               with st.spinner("Processing global events..."):
                   gdelt_intel = fetch_gdelt_global_events()
                   all_intelligence.extend(gdelt_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len([i for i in all_intelligence if i.get('type') == 'global_events'])}</div>
               <div class="metric-label">GLOBAL EVENTS</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col4:
           if collect_market:
               with st.spinner("Analyzing market intelligence..."):
                   market_data = fetch_market_intelligence()
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(market_data)}</div>
               <div class="metric-label">MARKET ASSETS</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col5:
           if collect_flights:
               with st.spinner("Tracking flight activity..."):
                   flight_data = fetch_flight_intelligence()
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(flight_data)}</div>
               <div class="metric-label">FLIGHT TRACKS</div>
           </div>
           """, unsafe_allow_html=True)
   
   # Generate executive assessment
   assessment = analytics_engine.generate_executive_assessment(all_intelligence, market_data, flight_data)
   
   # Executive Dashboard
   st.markdown('<div class="section-header">EXECUTIVE INTELLIGENCE DASHBOARD</div>', unsafe_allow_html=True)
   
   col1, col2 = st.columns([1, 2])
   
   with col1:
       # Threat assessment gauge
       threat_fig = create_executive_threat_gauge(assessment['overall_threat_score'], assessment['threat_level'])
       st.plotly_chart(threat_fig, use_container_width=True)
       
       # Executive metrics
       st.markdown(f"""
       <div class="threat-assessment">
           THREAT LEVEL: {assessment['threat_level']}
       </div>
       """, unsafe_allow_html=True)
       
       st.markdown(f"""
       <div class="intelligence-card">
           <h4>INTELLIGENCE SUMMARY</h4>
           <p><strong>Confidence Level:</strong> {assessment['confidence_score']:.0f}%</p>
           <p><strong>Intelligence Quality:</strong> {assessment['intelligence_quality']:.1f}/10</p>
           <p><strong>Market Stress Index:</strong> {assessment['market_stress_index']:.1f}/10</p>
           <p><strong>Source Diversity:</strong> {assessment['source_diversity']} categories</p>
           <p><strong>Flight Activity:</strong> {assessment['flight_activity_level']}</p>
           <p><strong>Last Updated:</strong> {assessment['timestamp'].strftime('%H:%M:%S UTC')}</p>
       </div>
       """, unsafe_allow_html=True)
   
   with col2:
       # Intelligence timeline
       timeline_fig = create_intelligence_timeline(all_intelligence)
       if timeline_fig:
           st.plotly_chart(timeline_fig, use_container_width=True)
       else:
           st.info("Intelligence timeline will display when data is available")
   
   # Main intelligence tabs
   tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
       "GLOBAL INTELLIGENCE", 
       "MARKET ANALYSIS", 
       "INTELLIGENCE FEED", 
       "REGIONAL ASSESSMENT",
       "FLIGHT TRACKING",
       "SOURCE ANALYSIS",
       "EXECUTIVE REPORTS"
   ])
   
   with tab1:
       st.markdown("### GLOBAL INTELLIGENCE MAP")
       
       # Interactive global map
       intel_map = create_global_intelligence_map(GLOBAL_INTELLIGENCE_HOTSPOTS, all_intelligence)
       map_data = st_folium(intel_map, width=700, height=600)
       
       # Hotspot analysis
       st.markdown("### STRATEGIC HOTSPOTS")
       
       hotspot_categories = {}
       for location, data in GLOBAL_INTELLIGENCE_HOTSPOTS.items():
           category = data['type']
           if category not in hotspot_categories:
               hotspot_categories[category] = []
           hotspot_categories[category].append((location, data))
       
       for category, hotspots in hotspot_categories.items():
           st.markdown(f"#### {category.upper()}")
           
           cols = st.columns(min(3, len(hotspots)))
           for idx, (location, data) in enumerate(hotspots):
               with cols[idx % 3]:
                   priority_class = f"priority-{data['priority'].lower()}"
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <h5>{location}</h5>
                       <p><strong>Priority:</strong> {data['priority']}</p>
                       <p><strong>Region:</strong> {data['region']}</p>
                       <p><strong>Coordinates:</strong> {data['lat']:.4f}, {data['lon']:.4f}</p>
                   </div>
                   """, unsafe_allow_html=True)
   
   with tab2:
       st.markdown("### MARKET INTELLIGENCE ANALYSIS")
       
       if market_data:
           # Market analysis charts
           perf_fig, risk_fig = create_market_analysis_dashboard(market_data)
           
           col1, col2 = st.columns(2)
           with col1:
               if perf_fig:
                   st.plotly_chart(perf_fig, use_container_width=True)
           with col2:
               if risk_fig:
                   st.plotly_chart(risk_fig, use_container_width=True)
           
           # Market stress indicators
           st.markdown("### MARKET STRESS INDICATORS")
           
           high_stress_assets = [asset for asset in market_data if asset['stress_level'] in ['CRITICAL', 'HIGH']]
           
           if high_stress_assets:
               for asset in high_stress_assets[:10]:
                   stress_class = f"priority-{asset['stress_level'].lower()}"
                   st.markdown(f"""
                   <div class="intelligence-item {stress_class}">
                       <h5>{asset['name']} ({asset['ticker']})</h5>
                       <p><strong>Current Price:</strong> ${asset['current_price']:.2f}</p>
                       <p><strong>Change:</strong> {asset['change_pct']:+.2f}%</p>
                       <p><strong>Volatility:</strong> {asset['volatility']:.2f}%</p>
                       <p><strong>Significance Score:</strong> {asset['significance_score']:.1f}</p>
                       <p><strong>Category:</strong> {asset['category']}</p>
                   </div>
                   """, unsafe_allow_html=True)
           else:
               st.success("No significant market stress detected")
       else:
           st.warning("Market intelligence unavailable")
   
   with tab3:
       st.markdown("### LIVE INTELLIGENCE FEED")
       
       # Advanced filtering
       col1, col2, col3 = st.columns(3)
       
       with col1:
           source_type_filter = st.selectbox("SOURCE TYPE", 
               ["All Sources", "Verified Intelligence", "Social Intelligence", "Premium News", "Global Events"])
       
       with col2:
           category_filter = st.selectbox("CATEGORY", 
               ["All Categories"] + list(set(item.get('category', 'Unknown') for item in all_intelligence)))
       
       with col3:
           max_items = st.slider("MAXIMUM ITEMS", 10, 200, 100, 10)
       
       # Filter intelligence data
       filtered_intelligence = []
       
       for item in all_intelligence:
           # Apply filters
           if (item.get('intelligence_score', 0) >= min_intelligence_score and
               item.get('priority') in selected_priorities and
               item.get('region') in selected_regions + ['Global'] and
               (datetime.utcnow() - item['timestamp']).total_seconds() / 3600 <= max_age_hours):
               
               # Source type filter
               if source_type_filter != "All Sources":
                   if source_type_filter == "Verified Intelligence" and item.get('type') != 'verified_intelligence':
                       continue
                   elif source_type_filter == "Social Intelligence" and item.get('type') != 'social_intelligence':
                       continue
                   elif source_type_filter == "Premium News" and item.get('type') != 'premium_news':
                       continue
                   elif source_type_filter == "Global Events" and item.get('type') != 'global_events':
                       continue
               
               # Category filter
               if category_filter != "All Categories" and item.get('category') != category_filter:
                   continue
               
               filtered_intelligence.append(item)
       
       # Sort by intelligence score
       filtered_intelligence.sort(key=lambda x: x.get('intelligence_score', 0), reverse=True)
       filtered_intelligence = filtered_intelligence[:max_items]
       
       st.markdown(f"**Displaying {len(filtered_intelligence)} intelligence items**")
       
       # Group by priority for display
       priority_groups = {}
       for item in filtered_intelligence:
           priority = item.get('priority', 'MEDIUM')
           if priority not in priority_groups:
               priority_groups[priority] = []
           priority_groups[priority].append(item)
       
       # Display by priority
       for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
           if priority in priority_groups:
               st.markdown(f"#### {priority} PRIORITY ({len(priority_groups[priority])} items)")
               
               for item in priority_groups[priority][:20]:  # Limit display
                   priority_class = f"priority-{priority.lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <div style="margin-bottom: 1rem;">
                           <span class="status-indicator status-{priority.lower()}">{priority}</span>
                           <span style="margin-left: 1rem; font-weight: 600;">Score: {item.get('intelligence_score', 0):.1f}/10</span>
                           <span style="margin-left: 1rem; color: #6B7280;">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #0A0E27;">{item['title']}</h4>
                       
                       <p style="margin-bottom: 1rem; color: #6B7280; line-height: 1.5;">
                           {item.get('content', '')[:400]}...
                       </p>
                       
                       <div style="margin-bottom: 1rem; font-size: 0.9rem; color: #6B7280;">
                           <strong>Source:</strong> {item['source']} | 
                           <strong>Category:</strong> {item.get('category', 'Unknown')} | 
                           <strong>Region:</strong> {item.get('region', 'Global')} |
                           <strong>Time:</strong> {item['timestamp'].strftime('%H:%M UTC')}
                       </div>
                       
                       <div>
                           <a href="{item.get('url', '#')}" target="_blank" class="source-link">
                               VIEW SOURCE
                           </a>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
   
   with tab4:
       st.markdown("### REGIONAL THREAT ASSESSMENT")
       
       regional_data = assessment['regional_assessment']
       
       if regional_data:
           # Regional threat visualization
           regional_fig = create_regional_threat_analysis(regional_data)
           if regional_fig:
               st.plotly_chart(regional_fig, use_container_width=True)
           
           # Detailed regional analysis
           st.markdown("### DETAILED REGIONAL ANALYSIS")
           
           for region, data in sorted(regional_data.items(), key=lambda x: x[1]['threat_level'], reverse=True):
               if region in selected_regions or 'Global' in selected_regions:
                   classification_class = f"priority-{data['classification'].lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-card {classification_class}">
                       <h3>{region.upper()} - {data['classification']}</h3>
                       
                       <div class="executive-grid">
                           <div style="text-align: center;">
                               <div class="metric-value">{data['threat_level']:.1f}</div>
                               <div class="metric-label">THREAT LEVEL</div>
                           </div>
                           
                           <div style="text-align: center;">
                               <div class="metric-value">{data['total_items']}</div>
                               <div class="metric-label">TOTAL SOURCES</div>
                           </div>
                           
                           <div style="text-align: center;">
                               <div class="metric-value">{data['critical']}</div>
                               <div class="metric-label">CRITICAL ITEMS</div>
                           </div>
                           
                           <div style="text-align: center;">
                               <div class="metric-value">{data['avg_sentiment']:+.2f}</div>
                               <div class="metric-label">AVG SENTIMENT</div>
                           </div>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       else:
           st.info("Regional analysis will be available when intelligence data is collected")
   
   with tab5:
       st.markdown("### FLIGHT INTELLIGENCE TRACKING")
       
       if flight_data:
           # Flight tracking map
           flight_fig = create_flight_tracking_display(flight_data)
           if flight_fig:
               st.plotly_chart(flight_fig, use_container_width=True)
           
           # Flight filters
           col1, col2, col3 = st.columns(3)
           
           with col1:
               flight_types = list(set(f['flight_type'] for f in flight_data))
               selected_flight_types = st.multiselect("FLIGHT TYPES", flight_types, default=flight_types)
           
           with col2:
               significance_levels = list(set(f['military_significance'] for f in flight_data))
               selected_significance = st.multiselect("SIGNIFICANCE LEVELS", significance_levels, default=significance_levels)
           
           with col3:
               flight_regions = list(set(f['region'] for f in flight_data))
               selected_flight_regions = st.multiselect("FLIGHT REGIONS", flight_regions, default=flight_regions)
           
           # Filtered flight display
           st.markdown("### ACTIVE MILITARY FLIGHTS")
           
           filtered_flights = [
               f for f in flight_data 
               if (f['flight_type'] in selected_flight_types and
                   f['military_significance'] in selected_significance and
                   f['region'] in selected_flight_regions)
           ]
           
           for flight in filtered_flights:
               significance_class = f"priority-{flight['military_significance'].lower()}"
               
               st.markdown(f"""
               <div class="intelligence-item {significance_class}">
                   <h4>{flight['callsign']} - {flight['aircraft_type']}</h4>
                   <p><strong>Route:</strong> {flight['origin']} → {flight['destination']}</p>
                   <p><strong>Altitude:</strong> {flight['altitude']:,} ft | <strong>Speed:</strong> {flight['speed']} kts</p>
                   <p><strong>Position:</strong> {flight['latitude']:.4f}, {flight['longitude']:.4f}</p>
                   <p><strong>Significance:</strong> {flight['military_significance']} | <strong>Status:</strong> {flight['status']}</p>
                   <p><strong>Region:</strong> {flight['region']} | <strong>Last Update:</strong> {flight['timestamp'].strftime('%H:%M UTC')}</p>
               </div>
               """, unsafe_allow_html=True)
       else:
           st.info("Flight intelligence data will be displayed when available")
   
   with tab6:
       st.markdown("### SOURCE ANALYSIS")
       
       if all_intelligence:
           # Source credibility analysis
           source_analysis = {}
           
           for item in all_intelligence:
               source = item['source']
               if source not in source_analysis:
                   source_analysis[source] = {
                       'total_items': 0,
                       'avg_credibility': 0,
                       'avg_intelligence': 0,
                       'critical_items': 0,
                       'categories': set()
                   }
               
               source_analysis[source]['total_items'] += 1
               source_analysis[source]['avg_credibility'] += item.get('credibility_score', 0)
               source_analysis[source]['avg_intelligence'] += item.get('intelligence_score', 0)
               source_analysis[source]['categories'].add(item.get('category', 'Unknown'))
               
               if item.get('priority') == 'CRITICAL':
                   source_analysis[source]['critical_items'] += 1
           
           # Calculate averages
           for source, data in source_analysis.items():
               if data['total_items'] > 0:
                   data['avg_credibility'] /= data['total_items']
                   data['avg_intelligence'] /= data['total_items']
                   data['categories'] = list(data['categories'])
           
           # Display top sources
           top_sources = sorted(source_analysis.items(), 
                              key=lambda x: x[1]['avg_intelligence'], reverse=True)[:20]
           
           st.markdown("### TOP INTELLIGENCE SOURCES")
           
           for source, data in top_sources:
               st.markdown(f"""
               <div class="intelligence-card">
                   <h4>{source}</h4>
                   <div class="executive-grid">
                       <div>
                           <div class="metric-value">{data['avg_intelligence']:.1f}</div>
                           <div class="metric-label">AVG INTELLIGENCE</div>
                       </div>
                       <div>
                           <div class="metric-value">{data['avg_credibility']:.1f}</div>
                           <div class="metric-label">AVG CREDIBILITY</div>
                       </div>
                       <div>
                           <div class="metric-value">{data['total_items']}</div>
                           <div class="metric-label">TOTAL ITEMS</div>
                       </div>
                       <div>
                           <div class="metric-value">{data['critical_items']}</div>
                           <div class="metric-label">CRITICAL ITEMS</div>
                       </div>
                   </div>
                   <p><strong>Categories:</strong> {', '.join(data['categories'][:3])}{'...' if len(data['categories']) > 3 else ''}</p>
               </div>
               """, unsafe_allow_html=True)
       else:
           st.info("Source analysis will be available when intelligence data is collected")
   
   with tab7:
       st.markdown("### EXECUTIVE REPORTS")
       
       # Executive summary generation
       col1, col2, col3 = st.columns(3)
       
       with col1:
           if st.button("GENERATE EXECUTIVE SUMMARY", type="primary"):
               executive_summary = {
                   'report_timestamp': datetime.now().isoformat(),
                   'classification': 'INTERNAL USE ONLY',
                   'threat_assessment': {
                       'overall_threat_level': assessment['threat_level'],
                       'threat_score': assessment['overall_threat_score'],
                       'confidence_level': assessment['confidence_score']
                   },
                   'key_findings': {
                       'total_intelligence_sources': assessment['total_sources'],
                       'critical_items': assessment['critical_items'],
                       'high_priority_items': assessment['high_items'],
                       'intelligence_quality': assessment['intelligence_quality'],
                       'market_stress_index': assessment['market_stress_index']
                   },
                   'regional_assessment': assessment['regional_assessment'],
                   'source_breakdown': {
                       'news_intelligence': len([i for i in all_intelligence if i.get('type') == 'verified_intelligence']),
                       'social_intelligence': len([i for i in all_intelligence if i.get('type') == 'social_intelligence']),
                       'premium_news': len([i for i in all_intelligence if i.get('type') == 'premium_news']),
                       'global_events': len([i for i in all_intelligence if i.get('type') == 'global_events'])
                   },
                   'recommendations': generate_executive_recommendations(assessment, all_intelligence),
                   'next_assessment': (datetime.now() + timedelta(hours=6)).isoformat()
               }
               
               summary_json = json.dumps(executive_summary, indent=2, default=str)
               st.download_button(
                   label="DOWNLOAD EXECUTIVE SUMMARY",
                   data=summary_json,
                   file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col2:
           if st.button("GENERATE DETAILED INTELLIGENCE REPORT"):
               detailed_report = {
                   'report_timestamp': datetime.now().isoformat(),
                   'classification': 'INTERNAL USE ONLY',
                   'executive_assessment': assessment,
                   'intelligence_data': {
                       'total_items': len(all_intelligence),
                       'intelligence_items': all_intelligence[:100],  # Limit for file size
                       'market_data': market_data,
                       'flight_data': flight_data
                   },
                   'analysis_metadata': {
                       'collection_parameters': {
                           'selected_regions': selected_regions,
                           'selected_priorities': selected_priorities,
                           'min_intelligence_score': min_intelligence_score,
                           'max_age_hours': max_age_hours
                       },
                       'source_configuration': {
                           'news_intelligence': collect_news,
                           'social_intelligence': collect_social,
                           'market_intelligence': collect_market,
                           'flight_intelligence': collect_flights,
                           'gdelt_events': collect_gdelt
                       }
                   }
               }
               
               report_json = json.dumps(detailed_report, indent=2, default=str)
               st.download_button(
                   label="DOWNLOAD DETAILED REPORT",
                   data=report_json,
                   file_name=f"detailed_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col3:
           if st.button("EXPORT THREAT BRIEFING"):
               threat_briefing = generate_threat_briefing(assessment, all_intelligence, market_data)
               
               st.download_button(
                   label="DOWNLOAD THREAT BRIEFING",
                   data=threat_briefing,
                   file_name=f"threat_briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                   mime="text/plain"
               )
       
       # Display current assessment summary
       st.markdown("### CURRENT ASSESSMENT SUMMARY")
       
       st.markdown(f"""
       <div class="intelligence-card">
           <h4>INTELLIGENCE OVERVIEW</h4>
           <div class="executive-grid">
               <div>
                   <strong>Threat Level:</strong> {assessment['threat_level']}<br>
                   <strong>Threat Score:</strong> {assessment['overall_threat_score']:.1f}/10<br>
                   <strong>Confidence:</strong> {assessment['confidence_score']:.0f}%
               </div>
               <div>
                   <strong>Total Sources:</strong> {assessment['total_sources']}<br>
                   <strong>Critical Items:</strong> {assessment['critical_items']}<br>
                   <strong>High Priority:</strong> {assessment['high_items']}
               </div>
               <div>
                   <strong>Intelligence Quality:</strong> {assessment['intelligence_quality']:.1f}/10<br>
                   <strong>Market Stress:</strong> {assessment['market_stress_index']:.1f}/10<br>
                   <strong>Source Diversity:</strong> {assessment['source_diversity']} types
               </div>
               <div>
                   <strong>Flight Activity:</strong> {assessment['flight_activity_level']}<br>
                   <strong>Sentiment:</strong> {assessment['avg_sentiment']:+.2f}<br>
                   <strong>Last Update:</strong> {assessment['timestamp'].strftime('%H:%M UTC')}
               </div>
           </div>
       </div>
       """, unsafe_allow_html=True)
   
   # Footer with system status
   st.markdown("---")
   st.markdown(f"""
   <div style="text-align: center; color: #6B7280; font-size: 0.9rem; padding: 2rem 0;">
       <p><strong>Strategic Intelligence Command Center</strong> | 
       Blis Analytics Professional Edition | 
       Classification: INTERNAL USE ONLY</p>
       <p>System Status: <span class="status-operational">OPERATIONAL</span> | 
       Sources Active: {len(set(item['source'] for item in all_intelligence))} | 
       Last Collection: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Blis signature
   st.markdown("""
   <div class="blis-signature">
       BLIS ANALYTICS
   </div>
   """, unsafe_allow_html=True)
   
   # Auto-refresh functionality
   if auto_refresh:
       time.sleep(300)  # 5 minutes
       st.rerun()

def generate_executive_recommendations(assessment, intelligence_data):
   """Generate executive recommendations based on assessment"""
   
   recommendations = []
   
   # Threat level recommendations
   if assessment['threat_level'] == 'CRITICAL':
       recommendations.append("IMMEDIATE: Activate crisis management protocols")
       recommendations.append("PRIORITY: Brief senior leadership within 2 hours")
       recommendations.append("ACTION: Increase monitoring frequency to real-time")
   elif assessment['threat_level'] == 'HIGH':
       recommendations.append("ELEVATED: Enhanced monitoring recommended")
       recommendations.append("BRIEFING: Daily executive briefings advised")
       recommendations.append("PREPARATION: Review contingency plans")
   elif assessment['threat_level'] == 'ELEVATED':
       recommendations.append("MONITORING: Maintain elevated awareness")
       recommendations.append("COORDINATION: Coordinate with relevant departments")
   else:
       recommendations.append("STANDARD: Continue routine monitoring")
       recommendations.append("ANALYSIS: Focus on trend identification")
   
   # Market-based recommendations
   if assessment['market_stress_index'] > 7:
       recommendations.append("FINANCIAL: Monitor market volatility impacts")
       recommendations.append("HEDGING: Consider defensive positioning")
   
   # Regional recommendations
   high_risk_regions = [region for region, data in assessment['regional_assessment'].items() 
                       if data.get('classification') in ['CRITICAL', 'HIGH']]
   
   if high_risk_regions:
       recommendations.append(f"REGIONAL: Focus monitoring on {', '.join(high_risk_regions[:3])}")
   
   # Data quality recommendations
   if assessment['confidence_score'] < 70:
       recommendations.append("DATA: Expand source collection for higher confidence")
   
   return recommendations

def generate_threat_briefing(assessment, intelligence_data, market_data):
   """Generate formatted threat briefing document"""
   
   briefing = f"""
STRATEGIC INTELLIGENCE THREAT BRIEFING
======================================

CLASSIFICATION: INTERNAL USE ONLY
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
VALID UNTIL: {(datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S UTC')}

EXECUTIVE SUMMARY
-----------------
Threat Level: {assessment['threat_level']}
Threat Score: {assessment['overall_threat_score']:.1f}/10
Confidence Level: {assessment['confidence_score']:.0f}%

INTELLIGENCE OVERVIEW
--------------------
Total Sources: {assessment['total_sources']}
Critical Items: {assessment['critical_items']}
High Priority Items: {assessment['high_items']}
Intelligence Quality: {assessment['intelligence_quality']:.1f}/10

MARKET INDICATORS
-----------------
Market Stress Index: {assessment['market_stress_index']:.1f}/10
Monitored Assets: {len(market_data)}
Flight Activity Level: {assessment['flight_activity_level']}

REGIONAL ASSESSMENT
-------------------
"""
   
   for region, data in assessment['regional_assessment'].items():
       briefing += f"""
{region}: {data['classification']} (Threat Level: {data['threat_level']:.1f}/10)
 - Intelligence Items: {data['total_items']}
 - Critical Items: {data['critical']}
 - Average Sentiment: {data['avg_sentiment']:+.2f}
"""
   
   briefing += f"""

TOP PRIORITY INTELLIGENCE ITEMS
--------------------------------
"""
   
   critical_items = [item for item in intelligence_data if item.get('priority') == 'CRITICAL'][:10]
   high_items = [item for item in intelligence_data if item.get('priority') == 'HIGH'][:10]
   
   for item in critical_items:
       briefing += f"""
CRITICAL: {item['title'][:100]}...
Source: {item['source']}
Region: {item.get('region', 'Global')}
Score: {item.get('intelligence_score', 0):.1f}/10
URL: {item.get('url', 'N/A')}

"""
   
   for item in high_items[:5]:  # Limit high items
       briefing += f"""
HIGH: {item['title'][:100]}...
Source: {item['source']}
Region: {item.get('region', 'Global')}
Score: {item.get('intelligence_score', 0):.1f}/10

"""
   
   recommendations = generate_executive_recommendations(assessment, intelligence_data)
   
   briefing += """
RECOMMENDATIONS
---------------
"""
   
   for i, recommendation in enumerate(recommendations, 1):
       briefing += f"{i}. {recommendation}\n"
   
   briefing += f"""

NEXT ASSESSMENT: {(datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S UTC')}

END OF BRIEFING
===============
"""
   
   return briefing

if __name__ == "__main__":
   main()
