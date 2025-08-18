# ============================================================================
# STRATEGIC INTELLIGENCE COMMAND CENTER v2.0
# ENTERPRISE-GRADE OSINT PLATFORM - ULTIMATE SOPHISTICATION
# Built for Intelligence Professionals - Zero Compromises
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
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# ELITE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Strategic Intelligence Command Center",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ULTIMATE PROFESSIONAL STYLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --command-black: #0a0a0a;
        --command-dark: #1a1a1a;
        --command-gray: #2a2a2a;
        --command-silver: #c0c0c0;
        --command-white: #ffffff;
        --command-blue: #0066ff;
        --command-red: #ff0044;
        --command-green: #00ff88;
        --command-gold: #ffcc00;
        --command-border: #333333;
    }
    
    .stApp {
        background: var(--command-black);
        color: var(--command-white);
    }
    
    .main-command-header {
        background: linear-gradient(135deg, var(--command-dark) 0%, var(--command-gray) 100%);
        border: 2px solid var(--command-border);
        border-radius: 0;
        padding: 2rem;
        margin-bottom: 1rem;
        text-align: center;
        position: relative;
        box-shadow: 0 0 20px rgba(0, 102, 255, 0.3);
    }
    
    .command-title {
        font-family: 'Inter', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: 3px;
        color: var(--command-blue);
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0 0 10px rgba(0, 102, 255, 0.5);
    }
    
    .command-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--command-silver);
        margin-top: 0.5rem;
        letter-spacing: 2px;
    }
    
    .classified-banner {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        background: var(--command-red);
        color: var(--command-white);
        text-align: center;
        padding: 0.5rem;
        font-weight: 900;
        font-size: 0.9rem;
        letter-spacing: 2px;
    }
    
    .metric-command-card {
        background: var(--command-dark);
        border: 1px solid var(--command-border);
        border-radius: 0;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--command-blue);
        transition: all 0.2s;
    }
    
    .metric-command-card:hover {
        border-left: 4px solid var(--command-gold);
        box-shadow: 0 0 15px rgba(255, 204, 0, 0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        color: var(--command-blue);
        line-height: 1;
        font-family: 'Inter', monospace;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--command-silver);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    .status-active {
        color: var(--command-green);
        font-weight: 700;
    }
    
    .status-critical {
        color: var(--command-red);
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    
    .status-warning {
        color: var(--command-gold);
        font-weight: 700;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .intelligence-item {
        background: var(--command-dark);
        border: 1px solid var(--command-border);
        border-radius: 0;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid var(--command-blue);
        transition: all 0.2s;
    }
    
    .intelligence-item:hover {
        border-left: 3px solid var(--command-gold);
        background: rgba(255, 204, 0, 0.05);
    }
    
    .source-tag {
        display: inline-block;
        background: var(--command-gray);
        color: var(--command-blue);
        padding: 0.3rem 0.8rem;
        border: 1px solid var(--command-border);
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .priority-critical { border-left-color: var(--command-red) !important; }
    .priority-high { border-left-color: var(--command-gold) !important; }
    .priority-medium { border-left-color: var(--command-blue) !important; }
    .priority-low { border-left-color: var(--command-silver) !important; }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--command-dark);
        border-bottom: 2px solid var(--command-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--command-gray);
        border: 1px solid var(--command-border);
        color: var(--command-silver);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--command-blue);
        color: var(--command-white);
    }
    
    .stSelectbox > div > div {
        background: var(--command-dark);
        border: 1px solid var(--command-border);
        color: var(--command-white);
    }
    
    .sidebar .stSelectbox > div > div {
        background: var(--command-gray);
    }
    
    .live-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--command-red);
        color: var(--command-white);
        padding: 0.5rem 1rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
    }
    
    .command-filter {
        background: var(--command-gray);
        border: 1px solid var(--command-border);
        color: var(--command-white);
        padding: 0.5rem;
        font-weight: 600;
    }
    
    div[data-testid="stSidebar"] {
        background: var(--command-dark);
    }
    
    div[data-testid="stSidebar"] > div {
        background: var(--command-dark);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ELITE DATA COLLECTION INFRASTRUCTURE
# ============================================================================

class EliteIntelligenceCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Strategic-Intelligence-Platform/2.0 (Enterprise)'
        })
        
        # Initialize Reddit with your credentials
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
            'tier_1_strategic': {
                'Reuters World': 'https://feeds.reuters.com/reuters/worldNews',
                'AP International': 'https://feeds.apnews.com/rss/apf-topnews',
                'BBC Global': 'http://feeds.bbci.co.uk/news/world/rss.xml',
                'Financial Times': 'https://www.ft.com/news-feed.rss',
                'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml'
            },
            'defense_intelligence': {
                'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
                'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
                'Breaking Defense': 'https://breakingdefense.com/feed/',
                'War on the Rocks': 'https://warontherocks.com/feed/',
                'Janes Defense': 'https://www.janes.com/feeds/news'
            },
            'geopolitical_analysis': {
                'Council Foreign Relations': 'https://www.cfr.org/rss-feeds',
                'Center Strategic Intl Studies': 'https://www.csis.org/rss.xml',
                'Atlantic Council': 'https://www.atlanticcouncil.org/feed/',
                'Foreign Policy': 'https://foreignpolicy.com/feed/',
                'Chatham House': 'https://www.chathamhouse.org/rss'
            },
            'economic_warfare': {
                'Bloomberg Markets': 'https://feeds.bloomberg.com/markets/news.rss',
                'Financial Times Markets': 'https://www.ft.com/markets?format=rss',
                'MarketWatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
                'Economic Times India': 'https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms',
                'Nikkei Asia': 'https://asia.nikkei.com/rss/feed/nar'
            },
            'conflict_monitoring': {
                'LiveUAMap': 'https://liveuamap.com/rss',
                'Syria Direct': 'https://syriadirect.org/feed/',
                'Institute for War': 'https://www.understandingwar.org/rss.xml',
                'ACLED Data': 'https://acleddata.com/rss',
                'Crisis Group': 'https://www.crisisgroup.org/rss.xml'
            }
        }
        
        # SUBREDDIT INTELLIGENCE NETWORK
        self.elite_subreddits = {
            'worldnews': {'weight': 1.0, 'region': 'Global'},
            'geopolitics': {'weight': 1.0, 'region': 'Global'},
            'UkraineConflict': {'weight': 0.9, 'region': 'Eastern Europe'},
            'syriancivilwar': {'weight': 0.8, 'region': 'Middle East'},
            'china': {'weight': 0.9, 'region': 'Asia Pacific'},
            'investing': {'weight': 0.7, 'region': 'Global'},
            'security': {'weight': 0.8, 'region': 'Global'},
            'intelligence': {'weight': 1.0, 'region': 'Global'},
            'MilitaryPorn': {'weight': 0.6, 'region': 'Global'},
            'CombatFootage': {'weight': 0.7, 'region': 'Global'}
        }
        
        # MARKET INTELLIGENCE TARGETS
        self.elite_tickers = {
            # Global Indices
            '^GSPC': {'name': 'S&P 500', 'type': 'index', 'region': 'North America'},
            '^DJI': {'name': 'Dow Jones', 'type': 'index', 'region': 'North America'},
            '^IXIC': {'name': 'NASDAQ', 'type': 'index', 'region': 'North America'},
            '^NSEI': {'name': 'Nifty 50', 'type': 'index', 'region': 'India'},
            '^N225': {'name': 'Nikkei 225', 'type': 'index', 'region': 'Japan'},
            '^FTSE': {'name': 'FTSE 100', 'type': 'index', 'region': 'UK'},
            
            # Defense Contractors
            'LMT': {'name': 'Lockheed Martin', 'type': 'defense', 'region': 'North America'},
            'RTX': {'name': 'Raytheon Tech', 'type': 'defense', 'region': 'North America'},
            'NOC': {'name': 'Northrop Grumman', 'type': 'defense', 'region': 'North America'},
            'GD': {'name': 'General Dynamics', 'type': 'defense', 'region': 'North America'},
            'BA': {'name': 'Boeing', 'type': 'defense', 'region': 'North America'},
            
            # Geopolitical Indicators
            '^VIX': {'name': 'VIX Fear Index', 'type': 'volatility', 'region': 'Global'},
            'GLD': {'name': 'Gold ETF', 'type': 'commodity', 'region': 'Global'},
            'CL=F': {'name': 'Crude Oil', 'type': 'commodity', 'region': 'Global'},
            
            # Regional Powers
            'RELIANCE.NS': {'name': 'Reliance Industries', 'type': 'energy', 'region': 'India'},
            'TCS.NS': {'name': 'Tata Consultancy', 'type': 'technology', 'region': 'India'},
            'TSLA': {'name': 'Tesla', 'type': 'technology', 'region': 'North America'}
        }

    @st.cache_data(ttl=300)
    def collect_elite_reddit_intelligence(_self):
        """Elite Reddit OSINT Collection"""
        if not _self.reddit:
            return []
        
        intelligence = []
        
        for subreddit_name, config in _self.elite_subreddits.items():
            try:
                subreddit = _self.reddit.subreddit(subreddit_name)
                posts = list(subreddit.hot(limit=15))
                
                for post in posts:
                    # Advanced sentiment analysis
                    text_content = f"{post.title} {post.selftext[:500]}"
                    sentiment = TextBlob(text_content).sentiment
                    
                    # Calculate intelligence value
                    intelligence_score = (
                        (post.score * 0.3) + 
                        (post.num_comments * 0.2) + 
                        (post.upvote_ratio * 100 * 0.3) +
                        (config['weight'] * 20)
                    )
                    
                    # Priority classification
                    if intelligence_score > 500:
                        priority = 'CRITICAL'
                    elif intelligence_score > 200:
                        priority = 'HIGH'
                    elif intelligence_score > 50:
                        priority = 'MEDIUM'
                    else:
                        priority = 'LOW'
                    
                    intelligence.append({
                        'source': f'Reddit r/{subreddit_name}',
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'upvote_ratio': post.upvote_ratio,
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_subjectivity': sentiment.subjectivity,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': config['region'],
                        'timestamp': datetime.fromtimestamp(post.created_utc),
                        'type': 'social_intelligence'
                    })
                    
            except Exception as e:
                continue
        
        return sorted(intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_elite_news_feeds(_self):
        """Elite News Feed Collection"""
        news_intelligence = []
        
        for category, sources in _self.elite_sources.items():
            for source_name, url in sources.items():
                try:
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:10]:
                        # Advanced content analysis
                        content = f"{entry.title} {entry.get('summary', '')}"
                        sentiment = TextBlob(content).sentiment
                        
                        # Geopolitical keyword detection
                        keywords_detected = _self._detect_geopolitical_keywords(content)
                        
                        # Calculate credibility score
                        credibility = _self._calculate_source_credibility(source_name)
                        
                        # Calculate intelligence value
                        intelligence_score = (
                            credibility * 30 +
                            len(keywords_detected) * 10 +
                            abs(sentiment.polarity) * 20 +
                            abs(sentiment.subjectivity) * 10
                        )
                        
                        # Priority classification
                        if intelligence_score > 80:
                            priority = 'CRITICAL'
                        elif intelligence_score > 60:
                            priority = 'HIGH'
                        elif intelligence_score > 40:
                            priority = 'MEDIUM'
                        else:
                            priority = 'LOW'
                        
                        news_intelligence.append({
                            'source': source_name,
                            'category': category,
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:400],
                            'url': entry.link,
                            'published': entry.get('published', ''),
                            'sentiment_polarity': sentiment.polarity,
                            'sentiment_subjectivity': sentiment.subjectivity,
                            'keywords': keywords_detected,
                            'credibility': credibility,
                            'intelligence_score': intelligence_score,
                            'priority': priority,
                            'timestamp': datetime.now(),
                            'type': 'news_intelligence'
                        })
                        
                except Exception as e:
                    continue
        
        return sorted(news_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_elite_market_intelligence(_self):
        """Elite Market Intelligence Collection"""
        market_intelligence = []
        
        for ticker, config in _self.elite_tickers.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                info = stock.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    # Calculate volatility
                    volatility = hist['Close'].pct_change().std() * 100
                    
                    # Risk assessment
                    if abs(change_pct) > 5:
                        risk_level = 'CRITICAL'
                    elif abs(change_pct) > 3:
                        risk_level = 'HIGH'
                    elif abs(change_pct) > 1:
                        risk_level = 'MEDIUM'
                    else:
                        risk_level = 'LOW'
                    
                    market_intelligence.append({
                        'ticker': ticker,
                        'name': config['name'],
                        'type': config['type'],
                        'region': config['region'],
                        'current_price': current_price,
                        'change_pct': change_pct,
                        'volatility': volatility,
                        'volume': hist['Volume'].iloc[-1],
                        'market_cap': info.get('marketCap', 'N/A'),
                        'risk_level': risk_level,
                        'timestamp': datetime.now()
                    })
                    
            except Exception as e:
                continue
        
        return market_intelligence

    @st.cache_data(ttl=600)
    def collect_elite_mobility_intelligence(_self):
        """Elite Mobility & Flight Intelligence"""
        try:
            url = "https://opensky-network.org/api/states/all"
            response = _self.session.get(url, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                mobility_intelligence = []
                
                if 'states' in data and data['states']:
                    for state in data['states'][:200]:
                        if state[5] and state[6]:  # Has coordinates
                            # Classify aircraft type
                            callsign = state[1].strip() if state[1] else 'UNKNOWN'
                            aircraft_type = _self._classify_aircraft(callsign)
                            
                            # Calculate threat assessment
                            threat_level = _self._assess_aircraft_threat(callsign, state[7], state[9])
                            
                            mobility_intelligence.append({
                                'callsign': callsign,
                                'country': state[2],
                                'longitude': state[5],
                                'latitude': state[6],
                                'altitude': state[7] if state[7] else 0,
                                'velocity': state[9] if state[9] else 0,
                                'heading': state[10] if state[10] else 0,
                                'on_ground': state[8],
                                'aircraft_type': aircraft_type,
                                'threat_level': threat_level,
                                'timestamp': datetime.now()
                            })
                
                return mobility_intelligence
            else:
                return []
                
        except Exception as e:
            return []

    def _detect_geopolitical_keywords(self, text):
        """Detect geopolitical keywords"""
        keywords_map = {
            'conflict': ['war', 'conflict', 'battle', 'fighting', 'combat', 'military'],
            'diplomacy': ['treaty', 'agreement', 'negotiation', 'summit', 'diplomatic'],
            'economic': ['sanctions', 'trade', 'tariff', 'embargo', 'economic'],
            'security': ['terrorism', 'security', 'intelligence', 'surveillance'],
            'nuclear': ['nuclear', 'missile', 'weapon', 'atomic'],
            'cyber': ['cyber', 'hacking', 'digital', 'internet', 'technology']
        }
        
        detected = []
        text_lower = text.lower()
        
        for category, keywords in keywords_map.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(category)
        
        return detected

    def _calculate_source_credibility(self, source_name):
        """Calculate source credibility score"""
        credibility_map = {
            'Reuters': 95, 'AP': 95, 'BBC': 90, 'Financial Times': 90,
            'Wall Street Journal': 85, 'Bloomberg': 85, 'Defense News': 80,
            'Military Times': 75, 'Breaking Defense': 75, 'CFR': 85,
            'CSIS': 80, 'Atlantic Council': 75, 'Foreign Policy': 80
        }
        
        for source, score in credibility_map.items():
            if source.lower() in source_name.lower():
                return score
        
        return 50  # Default credibility

    def _classify_aircraft(self, callsign):
        """Classify aircraft by callsign"""
        military_indicators = ['ARMY', 'NAVY', 'AF', 'USAF', 'RAF', 'FORTE', 'REAPER', 'HAWK']
        commercial_indicators = ['DL', 'AA', 'UA', 'WN', 'BA', 'LH', 'AF', 'KL']
        
        callsign_upper = callsign.upper()
        
        if any(indicator in callsign_upper for indicator in military_indicators):
            return 'MILITARY'
        elif any(indicator in callsign_upper for indicator in commercial_indicators):
            return 'COMMERCIAL'
        else:
            return 'UNKNOWN'

    def _assess_aircraft_threat(self, callsign, altitude, velocity):
        """Assess aircraft threat level"""
        if 'FORTE' in callsign.upper() or 'REAPER' in callsign.upper():
            return 'CRITICAL'
        elif self._classify_aircraft(callsign) == 'MILITARY':
            return 'HIGH'
        elif altitude and altitude > 40000:
            return 'MEDIUM'
        else:
            return 'LOW'

# ============================================================================
# ELITE ANALYTICS ENGINE
# ============================================================================

class EliteAnalyticsEngine:
    def __init__(self):
        pass
    
    def generate_strategic_assessment(self, reddit_data, news_data, market_data, mobility_data):
        """Generate comprehensive strategic assessment"""
        
        # Overall intelligence metrics
        total_sources = len(reddit_data) + len(news_data)
        critical_items = len([item for item in reddit_data + news_data if item.get('priority') == 'CRITICAL'])
        
        # Sentiment analysis
        all_sentiment = [item.get('sentiment_polarity', 0) for item in reddit_data + news_data]
        avg_sentiment = np.mean(all_sentiment) if all_sentiment else 0
        
        # Regional breakdown
        regional_activity = self._analyze_regional_activity(reddit_data + news_data)
        
        # Market stress indicators
        market_stress = self._calculate_market_stress(market_data)
        
        # Mobility assessment
        mobility_assessment = self._assess_mobility_patterns(mobility_data)
        
        # Threat level calculation
        threat_level = self._calculate_overall_threat(critical_items, market_stress, mobility_assessment)
        
        return {
            'total_sources': total_sources,
            'critical_items': critical_items,
            'avg_sentiment': avg_sentiment,
            'regional_activity': regional_activity,
            'market_stress': market_stress,
            'mobility_assessment': mobility_assessment,
            'threat_level': threat_level,
            'timestamp': datetime.now()
        }
    
    def _analyze_regional_activity(self, data):
        """Analyze activity by region"""
        regional_counts = {}
        for item in data:
            region = item.get('region', 'Unknown')
            if region not in regional_counts:
                regional_counts[region] = {'total': 0, 'critical': 0, 'high': 0}
            
            regional_counts[region]['total'] += 1
            if item.get('priority') == 'CRITICAL':
                regional_counts[region]['critical'] += 1
            elif item.get('priority') == 'HIGH':
                regional_counts[region]['high'] += 1
        
        return regional_counts
    
    def _calculate_market_stress(self, market_data):
        """Calculate market stress indicators"""
        if not market_data:
            return 0
        
        # VIX level
        vix_data = [item for item in market_data if 'VIX' in item['name']]
        vix_level = vix_data[0]['current_price'] if vix_data else 20
        
        # Defense sector performance
        defense_stocks = [item for item in market_data if item['type'] == 'defense']
        defense_performance = np.mean([item['change_pct'] for item in defense_stocks]) if defense_stocks else 0
        
        # Overall volatility
        volatilities = [item.get('volatility', 0) for item in market_data]
        avg_volatility = np.mean(volatilities) if volatilities else 0
        
        # Stress calculation
        stress_score = min(100, (vix_level / 40) * 100 + avg_volatility * 10 + abs(defense_performance) * 5)
        
        return stress_score
    
    def _assess_mobility_patterns(self, mobility_data):
        """Assess mobility and flight patterns"""
        if not mobility_data:
            return {'total_aircraft': 0, 'military_aircraft': 0, 'threat_assessment': 'LOW'}
        
        total_aircraft = len(mobility_data)
        military_aircraft = len([item for item in mobility_data if item['aircraft_type'] == 'MILITARY'])
        critical_threats = len([item for item in mobility_data if item['threat_level'] == 'CRITICAL'])
        
        if critical_threats > 5:
            threat_assessment = 'CRITICAL'
        elif critical_threats > 2 or military_aircraft > 20:
            threat_assessment = 'HIGH'
        elif military_aircraft > 10:
            threat_assessment = 'MEDIUM'
        else:
            threat_assessment = 'LOW'
        
        return {
            'total_aircraft': total_aircraft,
            'military_aircraft': military_aircraft,
            'critical_threats': critical_threats,
            'threat_assessment': threat_assessment
        }
    
    def _calculate_overall_threat(self, critical_items, market_stress, mobility_assessment):
        """Calculate overall threat level"""
        threat_score = 0
        
        # Critical intelligence items
        threat_score += critical_items * 10
        
        # Market stress contribution
        threat_score += market_stress * 0.5
        
        # Mobility threat contribution
        mobility_threat_map = {'CRITICAL': 50, 'HIGH': 30, 'MEDIUM': 15, 'LOW': 5}
        threat_score += mobility_threat_map.get(mobility_assessment.get('threat_assessment', 'LOW'), 5)
        
        # Classify overall threat
        if threat_score > 150:
            return 'CRITICAL'
        elif threat_score > 100:
            return 'HIGH'
        elif threat_score > 50:
            return 'MEDIUM'
        else:
            return 'LOW'

# ============================================================================
# ELITE DASHBOARD ENGINE
# ============================================================================

def main():
   # COMMAND CENTER HEADER
   st.markdown("""
   <div class="main-command-header">
       <div class="classified-banner">⚫ CLASSIFIED - INTELLIGENCE OPERATIONS ⚫</div>
       <h1 class="command-title">STRATEGIC INTELLIGENCE COMMAND CENTER</h1>
       <p class="command-subtitle">REAL-TIME OSINT • GEOPOLITICAL ANALYSIS • THREAT ASSESSMENT</p>
       <div class="live-status">
           <span>●</span> LIVE INTELLIGENCE FEED ACTIVE
       </div>
   </div>
   """, unsafe_allow_html=True)
   
   # ELITE SIDEBAR CONTROLS
   st.sidebar.markdown("## ⚫ COMMAND CONTROLS")
   
   # Geographic filters
   st.sidebar.markdown("### 🌍 GEOGRAPHIC FILTERS")
   regions = ['Global', 'North America', 'Europe', 'Asia Pacific', 'Middle East', 'Africa', 'Eastern Europe', 'India']
   selected_regions = st.sidebar.multiselect("Active Regions:", regions, default=['Global'])
   
   # Priority filters
   st.sidebar.markdown("### 🎯 PRIORITY CLASSIFICATION")
   priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
   selected_priorities = st.sidebar.multiselect("Priority Levels:", priorities, default=priorities)
   
   # Source type filters
   st.sidebar.markdown("### 📡 SOURCE TYPES")
   source_types = ['Social Intelligence', 'News Intelligence', 'Market Intelligence', 'Mobility Intelligence']
   selected_sources = st.sidebar.multiselect("Intelligence Sources:", source_types, default=source_types)
   
   # Auto-refresh control
   st.sidebar.markdown("### ⚡ LIVE UPDATES")
   auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=True)
   refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 60, 600, 300)
   
   if st.sidebar.button("🔄 MANUAL REFRESH", use_container_width=True):
       st.cache_data.clear()
       st.rerun()
   
   # Initialize systems
   collector = EliteIntelligenceCollector()
   analyzer = EliteAnalyticsEngine()
   
   # DATA COLLECTION WITH PROGRESS
   progress_container = st.container()
   with progress_container:
       st.markdown("### 📡 INTELLIGENCE COLLECTION STATUS")
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           with st.spinner("Reddit OSINT..."):
               reddit_data = collector.collect_elite_reddit_intelligence()
           st.success(f"✅ Reddit: {len(reddit_data)} items")
       
       with col2:
           with st.spinner("News Feeds..."):
               news_data = collector.collect_elite_news_feeds()
           st.success(f"✅ News: {len(news_data)} items")
       
       with col3:
           with st.spinner("Market Intel..."):
               market_data = collector.collect_elite_market_intelligence()
           st.success(f"✅ Markets: {len(market_data)} items")
       
       with col4:
           with st.spinner("Mobility Track..."):
               mobility_data = collector.collect_elite_mobility_intelligence()
           st.success(f"✅ Mobility: {len(mobility_data)} items")
   
   # STRATEGIC ASSESSMENT
   assessment = analyzer.generate_strategic_assessment(reddit_data, news_data, market_data, mobility_data)
   
   # COMMAND METRICS
   st.markdown("### ⚫ COMMAND METRICS")
   
   col1, col2, col3, col4, col5 = st.columns(5)
   
   with col1:
       st.markdown(f"""
       <div class="metric-command-card">
           <div class="metric-value">{assessment['total_sources']}</div>
           <div class="metric-label">TOTAL SOURCES</div>
           <div class="status-active">OPERATIONAL</div>
       </div>
       """, unsafe_allow_html=True)
   
   with col2:
       threat_class = "status-critical" if assessment['threat_level'] == 'CRITICAL' else "status-warning" if assessment['threat_level'] in ['HIGH', 'MEDIUM'] else "status-active"
       st.markdown(f"""
       <div class="metric-command-card">
           <div class="metric-value">{assessment['threat_level']}</div>
           <div class="metric-label">THREAT LEVEL</div>
           <div class="{threat_class}">ASSESSED</div>
       </div>
       """, unsafe_allow_html=True)
   
   with col3:
       critical_class = "status-critical" if assessment['critical_items'] > 10 else "status-warning" if assessment['critical_items'] > 5 else "status-active"
       st.markdown(f"""
       <div class="metric-command-card">
           <div class="metric-value">{assessment['critical_items']}</div>
           <div class="metric-label">CRITICAL ITEMS</div>
           <div class="{critical_class}">FLAGGED</div>
       </div>
       """, unsafe_allow_html=True)
   
   with col4:
       sentiment_class = "status-critical" if assessment['avg_sentiment'] < -0.3 else "status-warning" if assessment['avg_sentiment'] < 0 else "status-active"
       st.markdown(f"""
       <div class="metric-command-card">
           <div class="metric-value">{assessment['avg_sentiment']:.3f}</div>
           <div class="metric-label">SENTIMENT INDEX</div>
           <div class="{sentiment_class}">ANALYZED</div>
       </div>
       """, unsafe_allow_html=True)
   
   with col5:
       stress_class = "status-critical" if assessment['market_stress'] > 70 else "status-warning" if assessment['market_stress'] > 40 else "status-active"
       st.markdown(f"""
       <div class="metric-command-card">
           <div class="metric-value">{assessment['market_stress']:.0f}</div>
           <div class="metric-label">MARKET STRESS</div>
           <div class="{stress_class}">MONITORED</div>
       </div>
       """, unsafe_allow_html=True)
   
   # MAIN INTELLIGENCE TABS
   tab1, tab2, tab3, tab4, tab5 = st.tabs([
       "🎯 STRATEGIC OVERVIEW",
       "📊 INTELLIGENCE FEED", 
       "💰 MARKET WARFARE",
       "✈️ MOBILITY TRACKING",
       "📋 THREAT ANALYSIS"
   ])
   
   with tab1:
       st.markdown("## 🎯 STRATEGIC INTELLIGENCE OVERVIEW")
       
       # Regional activity heatmap
       col1, col2 = st.columns(2)
       
       with col1:
           st.markdown("### 🌍 Regional Activity Matrix")
           regional_data = assessment['regional_activity']
           
           if regional_data:
               regions_df = pd.DataFrame([
                   {'Region': region, 'Total': data['total'], 'Critical': data['critical'], 'High': data['high']}
                   for region, data in regional_data.items()
               ])
               
               fig = px.bar(regions_df, x='Region', y=['Critical', 'High', 'Total'], 
                          title="Intelligence Activity by Region",
                          color_discrete_map={'Critical': '#ff0044', 'High': '#ffcc00', 'Total': '#0066ff'})
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='white'
               )
               st.plotly_chart(fig, use_container_width=True)
       
       with col2:
           st.markdown("### ⚡ Real-time Threat Assessment")
           
           # Threat gauge
           fig = go.Figure(go.Indicator(
               mode = "gauge+number+delta",
               value = {'CRITICAL': 100, 'HIGH': 75, 'MEDIUM': 50, 'LOW': 25}[assessment['threat_level']],
               domain = {'x': [0, 1], 'y': [0, 1]},
               title = {'text': "THREAT LEVEL"},
               gauge = {
                   'axis': {'range': [None, 100]},
                   'bar': {'color': "red"},
                   'steps': [
                       {'range': [0, 25], 'color': "green"},
                       {'range': [25, 50], 'color': "yellow"},
                       {'range': [50, 75], 'color': "orange"},
                       {'range': [75, 100], 'color': "red"}
                   ],
                   'threshold': {
                       'line': {'color': "red", 'width': 4},
                       'thickness': 0.75,
                       'value': 90
                   }
               }
           ))
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font_color='white',
               height=300
           )
           st.plotly_chart(fig, use_container_width=True)
       
       # Strategic summary
       st.markdown("### 📋 EXECUTIVE INTELLIGENCE BRIEF")
       st.markdown(f"""
       **CLASSIFICATION:** SENSITIVE
       
       **ASSESSMENT TIME:** {assessment['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}
       
       **OVERALL THREAT LEVEL:** {assessment['threat_level']}
       
       **KEY FINDINGS:**
       - Total Intelligence Sources: {assessment['total_sources']}
       - Critical Priority Items: {assessment['critical_items']}
       - Average Sentiment Index: {assessment['avg_sentiment']:.3f}
       - Market Stress Level: {assessment['market_stress']:.1f}/100
       - Aircraft Tracked: {assessment['mobility_assessment']['total_aircraft']}
       - Military Aircraft: {assessment['mobility_assessment']['military_aircraft']}
       
       **REGIONAL HOTSPOTS:**
       """)
       
       for region, data in assessment['regional_activity'].items():
           if data['critical'] > 0:
               st.markdown(f"🔴 **{region}**: {data['critical']} critical items, {data['total']} total")
           elif data['high'] > 3:
               st.markdown(f"🟡 **{region}**: {data['high']} high priority items, {data['total']} total")
   
   with tab2:
       st.markdown("## 📊 LIVE INTELLIGENCE FEED")
       
       # Filter and combine all intelligence
       all_intelligence = []
       
       # Add Reddit data
       if 'Social Intelligence' in selected_sources:
           for item in reddit_data:
               if item['priority'] in selected_priorities and item['region'] in selected_regions:
                   all_intelligence.append(item)
       
       # Add news data
       if 'News Intelligence' in selected_sources:
           for item in news_data:
               if item['priority'] in selected_priorities:
                   all_intelligence.append(item)
       
       # Sort by intelligence score
       all_intelligence.sort(key=lambda x: x['intelligence_score'], reverse=True)
       
       # Display intelligence items
       for item in all_intelligence[:50]:  # Show top 50
           priority_class = f"priority-{item['priority'].lower()}"
           
           st.markdown(f"""
           <div class="intelligence-item {priority_class}">
               <div>
                   <span class="source-tag">{item['source']}</span>
                   <span class="source-tag">{item['priority']}</span>
                   <span class="source-tag">Score: {item['intelligence_score']:.0f}</span>
               </div>
               <h4>{item['title']}</h4>
               <p><strong>Sentiment:</strong> {item['sentiment_polarity']:.3f} | 
               <strong>Region:</strong> {item.get('region', 'Global')} | 
               <strong>Time:</strong> {item['timestamp'].strftime('%H:%M')}</p>
               <p><a href="{item['url']}" target="_blank">🔗 Source Link</a></p>
           </div>
           """, unsafe_allow_html=True)
   
   with tab3:
       st.markdown("## 💰 MARKET WARFARE INTELLIGENCE")
       
       if market_data:
           # Market overview
           df_market = pd.DataFrame(market_data)
           
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("### 📈 Market Performance Matrix")
               
               # Create performance chart
               fig = go.Figure()
               
               colors = ['red' if x < 0 else 'green' for x in df_market['change_pct']]
               
               fig.add_trace(go.Bar(
                   x=df_market['name'],
                   y=df_market['change_pct'],
                   marker_color=colors,
                   text=[f"{x:.2f}%" for x in df_market['change_pct']],
                   textposition='auto'
               ))
               
               fig.update_layout(
                   title="Market Performance (%)",
                   xaxis_title="Assets",
                   yaxis_title="Change %",
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='white',
                   height=400
               )
               fig.update_xaxis(tickangle=45)
               st.plotly_chart(fig, use_container_width=True)
           
           with col2:
               st.markdown("### 🛡️ Defense Sector Analysis")
               
               defense_stocks = df_market[df_market['type'] == 'defense']
               if not defense_stocks.empty:
                   for _, stock in defense_stocks.iterrows():
                       risk_color = "🔴" if stock['risk_level'] == 'CRITICAL' else "🟡" if stock['risk_level'] == 'HIGH' else "🟢"
                       st.markdown(f"{risk_color} **{stock['name']}**: {stock['change_pct']:.2f}% | Risk: {stock['risk_level']}")
               
               st.markdown("### 🌡️ Market Stress Indicators")
               
               # VIX and volatility indicators
               vix_data = df_market[df_market['name'].str.contains('VIX', na=False)]
               if not vix_data.empty:
                   vix_level = vix_data.iloc[0]['current_price']
                   st.metric("VIX Fear Index", f"{vix_level:.2f}", 
                            help="Values >30 indicate high fear, <20 indicate complacency")
               
               # Commodity indicators
               gold_data = df_market[df_market['name'].str.contains('Gold', na=False)]
               oil_data = df_market[df_market['name'].str.contains('Oil', na=False)]
               
               if not gold_data.empty:
                   st.metric("Gold ETF", f"${gold_data.iloc[0]['current_price']:.2f}", 
                            f"{gold_data.iloc[0]['change_pct']:.2f}%")
               
               if not oil_data.empty:
                   st.metric("Crude Oil", f"${oil_data.iloc[0]['current_price']:.2f}", 
                            f"{oil_data.iloc[0]['change_pct']:.2f}%")
       else:
           st.warning("⚠️ Market intelligence temporarily unavailable")
   
   with tab4:
       st.markdown("## ✈️ MOBILITY & FLIGHT TRACKING")
       
       if mobility_data:
           mobility_assessment = assessment['mobility_assessment']
           
           # Mobility metrics
           col1, col2, col3, col4 = st.columns(4)
           
           with col1:
               st.metric("Total Aircraft", mobility_assessment['total_aircraft'])
           
           with col2:
               st.metric("Military Aircraft", mobility_assessment['military_aircraft'])
           
           with col3:
               st.metric("Critical Threats", mobility_assessment['critical_threats'])
           
           with col4:
               threat_color = "🔴" if mobility_assessment['threat_assessment'] == 'CRITICAL' else "🟡" if mobility_assessment['threat_assessment'] == 'HIGH' else "🟢"
               st.metric("Threat Assessment", f"{threat_color} {mobility_assessment['threat_assessment']}")
           
           # Aircraft map
           df_mobility = pd.DataFrame(mobility_data)
           
           if not df_mobility.empty:
               st.markdown("### 🗺️ Live Aircraft Tracking")
               
               # Color code by threat level
               color_map = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'blue'}
               df_mobility['color'] = df_mobility['threat_level'].map(color_map)
               
               fig = px.scatter_mapbox(
                   df_mobility,
                   lat="latitude",
                   lon="longitude",
                   hover_name="callsign",
                   hover_data={"country": True, "altitude": True, "velocity": True, "aircraft_type": True, "threat_level": True},
                   color="threat_level",
                   color_discrete_map=color_map,
                   size_max=15,
                   zoom=2,
                   height=600,
                   title="Global Aircraft Surveillance Network"
               )
               
               fig.update_layout(
                   mapbox_style="carto-darkmatter",
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='white'
               )
               
               st.plotly_chart(fig, use_container_width=True)
               
               # Aircraft analysis
               st.markdown("### 📊 Aircraft Classification Analysis")
               
               aircraft_by_type = df_mobility['aircraft_type'].value_counts()
               aircraft_by_threat = df_mobility['threat_level'].value_counts()
               
               col1, col2 = st.columns(2)
               
               with col1:
                   fig = px.pie(
                       values=aircraft_by_type.values,
                       names=aircraft_by_type.index,
                       title="Aircraft by Type"
                   )
                   fig.update_layout(
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='white'
                   )
                   st.plotly_chart(fig, use_container_width=True)
               
               with col2:
                   fig = px.pie(
                       values=aircraft_by_threat.values,
                       names=aircraft_by_threat.index,
                       title="Aircraft by Threat Level",
                       color_discrete_map=color_map
                   )
                   fig.update_layout(
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       font_color='white'
                   )
                   st.plotly_chart(fig, use_container_width=True)
       else:
           st.warning("⚠️ Mobility intelligence temporarily unavailable")
   
   with tab5:
       st.markdown("## 📋 COMPREHENSIVE THREAT ANALYSIS")
       
       # Threat timeline
       st.markdown("### ⏱️ Threat Evolution Timeline")
       
       # Create threat timeline chart
       all_data_with_time = reddit_data + news_data
       all_data_with_time.sort(key=lambda x: x['timestamp'])
       
       if all_data_with_time:
           # Group by hour for timeline
           timeline_data = {}
           for item in all_data_with_time[-100:]:  # Last 100 items
               hour_key = item['timestamp'].strftime('%Y-%m-%d %H:00')
               if hour_key not in timeline_data:
                   timeline_data[hour_key] = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
               timeline_data[hour_key][item['priority']] += 1
           
           timeline_df = pd.DataFrame([
               {'Time': time, **counts} for time, counts in timeline_data.items()
           ])
           
           if not timeline_df.empty:
               fig = px.bar(
                   timeline_df, 
                   x='Time', 
                   y=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                   title="Threat Activity Timeline",
                   color_discrete_map={
                       'CRITICAL': '#ff0044',
                       'HIGH': '#ffcc00', 
                       'MEDIUM': '#0066ff',
                       'LOW': '#888888'
                   }
               )
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='white'
               )
               st.plotly_chart(fig, use_container_width=True)
       
       # Correlation analysis
       st.markdown("### 🔗 Multi-Source Intelligence Correlation")
       
       # Analyze correlations between market stress and intelligence activity
       if market_data and (reddit_data or news_data):
           market_stress = assessment['market_stress']
           intelligence_activity = len([item for item in reddit_data + news_data if item['priority'] in ['CRITICAL', 'HIGH']])
           
           st.markdown(f"""
           **Current Correlations:**
           - Market Stress Level: {market_stress:.1f}/100
           - High-Priority Intelligence Items: {intelligence_activity}
           - Correlation Coefficient: {np.corrcoef([market_stress], [intelligence_activity])[0,1]:.3f}
           """)
       
       # Export capabilities
       st.markdown("### 📤 Intelligence Export")
       
       col1, col2, col3 = st.columns(3)
       
       with col1:
           if st.button("📊 Export Strategic Report", use_container_width=True):
               # Create comprehensive report
               report_data = {
                   'assessment': assessment,
                   'reddit_intelligence': reddit_data[:20],
                   'news_intelligence': news_data[:20],
                   'market_intelligence': market_data,
                   'mobility_intelligence': mobility_data[:50] if mobility_data else [],
                   'generated_at': datetime.now().isoformat()
               }
               
               json_report = json.dumps(report_data, default=str, indent=2)
               st.download_button(
                   label="Download Strategic Intelligence Report",
                   data=json_report,
                   file_name=f"strategic_intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col2:
           if st.button("📋 Export Threat Summary", use_container_width=True):
               # Create threat-focused summary
               threat_summary = {
                   'threat_level': assessment['threat_level'],
                   'critical_items': assessment['critical_items'],
                   'market_stress': assessment['market_stress'],
                   'mobility_threats': assessment['mobility_assessment'],
                   'regional_hotspots': assessment['regional_activity'],
                   'timestamp': assessment['timestamp'].isoformat()
               }
               
               json_summary = json.dumps(threat_summary, default=str, indent=2)
               st.download_button(
                   label="Download Threat Assessment",
                   data=json_summary,
                   file_name=f"threat_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col3:
           if st.button("📈 Export Market Analysis", use_container_width=True):
               if market_data:
                   market_df = pd.DataFrame(market_data)
                   csv_data = market_df.to_csv(index=False)
                   st.download_button(
                       label="Download Market Analysis",
                       data=csv_data,
                       file_name=f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                       mime="text/csv"
                   )
   
   # AUTO-REFRESH MECHANISM
   if auto_refresh:
       time.sleep(refresh_interval)
       st.rerun()

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
   main()
