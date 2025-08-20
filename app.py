# ============================================================================
# STRATEGIC INTELLIGENCE COMMAND CENTER - REAL DATA IMPLEMENTATION
# Professional Intelligence Platform with Verified APIs and Real Sources
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
import json
from textblob import TextBlob
import warnings
import folium
from streamlit_folium import st_folium
import os
import time
warnings.filterwarnings('ignore')

# ============================================================================
# REAL API CONFIGURATION
# ============================================================================

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET") 
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
POLYGON_ACCESS_KEY = os.getenv("POLYGON_ACCESS_KEY")
POLYGON_SECRET_KEY = os.getenv("POLYGON_SECRET_KEY")

# ============================================================================
# VERIFIED INTELLIGENCE SOURCES (REAL RSS FEEDS ONLY)
# ============================================================================

VERIFIED_NEWS_SOURCES = {
    'Reuters World': 'https://feeds.reuters.com/reuters/worldNews',
    'Reuters Business': 'https://feeds.reuters.com/reuters/businessNews',
    'Reuters Politics': 'https://feeds.reuters.com/reuters/politicsNews',
    'AP Top News': 'https://feeds.apnews.com/rss/apf-topnews',
    'AP World News': 'https://feeds.apnews.com/rss/apf-worldnews',
    'AP Politics': 'https://feeds.apnews.com/rss/apf-politicsnews',
    'BBC World': 'http://feeds.bbci.co.uk/news/world/rss.xml',
    'BBC Business': 'http://feeds.bbci.co.uk/news/business/rss.xml',
    'BBC Politics': 'http://feeds.bbci.co.uk/news/politics/rss.xml',
    'Financial Times': 'https://www.ft.com/rss/home/uk',
    'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
    'Breaking Defense': 'https://breakingdefense.com/feed/',
    'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
    'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
    'Bloomberg Politics': 'https://feeds.bloomberg.com/politics/news.rss',
    'Bloomberg Markets': 'https://feeds.bloomberg.com/markets/news.rss',
    'CNN World': 'http://rss.cnn.com/rss/edition_world.rss',
    'The Guardian World': 'https://www.theguardian.com/world/rss',
    'The Guardian Politics': 'https://www.theguardian.com/politics/rss',
    'Washington Post World': 'https://feeds.washingtonpost.com/rss/world',
    'NYT World': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'WSJ World': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
    'Foreign Policy': 'https://foreignpolicy.com/feed/',
    'CFR Analysis': 'https://www.cfr.org/rss-feeds',
    'CSIS Reports': 'https://www.csis.org/rss.xml',
    'ISW Reports': 'https://www.understandingwar.org/rss.xml',
    'Atlantic Council': 'https://www.atlanticcouncil.org/feed/',
    'War on the Rocks': 'https://warontherocks.com/feed/',
    'Brookings': 'https://www.brookings.edu/feed/',
    'Carnegie Endowment': 'https://carnegieendowment.org/feed/',
    'RAND Corporation': 'https://www.rand.org/content/rand/rss/pubs/research_reports.xml',
    'Chatham House': 'https://www.chathamhouse.org/rss.xml',
    'RUSI': 'https://rusi.org/rss.xml'
}

# REAL GLOBAL HOTSPOTS WITH VERIFIED COORDINATES
REAL_GLOBAL_HOTSPOTS = {
    # Active Conflicts
    'Kyiv, Ukraine': {'lat': 50.4501, 'lon': 30.5234, 'priority': 'CRITICAL', 'region': 'Eastern Europe', 'type': 'Capital'},
    'Gaza City': {'lat': 31.5017, 'lon': 34.4668, 'priority': 'CRITICAL', 'region': 'Middle East', 'type': 'Conflict Zone'},
    'Damascus, Syria': {'lat': 33.5138, 'lon': 36.2765, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Capital'},
    'Sanaa, Yemen': {'lat': 15.3694, 'lon': 44.1910, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Capital'},
    
    # Strategic Waterways
    'Strait of Hormuz': {'lat': 26.5667, 'lon': 56.25, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Waterway'},
    'Suez Canal': {'lat': 30.0444, 'lon': 32.3412, 'priority': 'MEDIUM', 'region': 'Middle East', 'type': 'Waterway'},
    'Taiwan Strait': {'lat': 23.8, 'lon': 120.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Waterway'},
    'South China Sea': {'lat': 12.0, 'lon': 113.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Waterway'},
    'Strait of Malacca': {'lat': 2.5, 'lon': 101.8, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Waterway'},
    'Bosphorus Strait': {'lat': 41.0082, 'lon': 28.9784, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Waterway'},
    'Panama Canal': {'lat': 9.0, 'lon': -79.5, 'priority': 'MEDIUM', 'region': 'Americas', 'type': 'Waterway'},
    
    # Tension Zones
    'Korean DMZ': {'lat': 38.0, 'lon': 127.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Border'},
    'Kashmir (Srinagar)': {'lat': 34.0837, 'lon': 74.7973, 'priority': 'MEDIUM', 'region': 'Asia Pacific', 'type': 'Disputed Territory'},
    'Nagorno-Karabakh': {'lat': 39.8282, 'lon': 46.7633, 'priority': 'MEDIUM', 'region': 'Europe', 'type': 'Disputed Territory'},
    
    # Major Capitals
    'Moscow, Russia': {'lat': 55.7558, 'lon': 37.6176, 'priority': 'HIGH', 'region': 'Eastern Europe', 'type': 'Capital'},
    'Beijing, China': {'lat': 39.9042, 'lon': 116.4074, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Capital'},
    'Tehran, Iran': {'lat': 35.6892, 'lon': 51.3890, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Capital'},
    'Pyongyang, North Korea': {'lat': 39.0392, 'lon': 125.7625, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Capital'},
    'Jerusalem': {'lat': 31.7683, 'lon': 35.2137, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Capital'},
    'Taipei, Taiwan': {'lat': 25.0330, 'lon': 121.5654, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Capital'}
}

# ============================================================================
# PROFESSIONAL DESIGN SYSTEM
# ============================================================================

st.set_page_config(
    page_title="Strategic Intelligence Command Center | Blis Analytics",
    page_icon="▓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --executive-primary: #0A0E27;
        --executive-secondary: #1A1F3A;
        --executive-accent: #3B82F6;
        --executive-white: #FFFFFF;
        --executive-light: #F8FAFC;
        --executive-border: #E5E7EB;
        --executive-text: #111827;
        --executive-text-secondary: #6B7280;
        --executive-red: #DC2626;
        --executive-green: #059669;
        --executive-amber: #D97706;
        --shadow-primary: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .stApp {
        background: var(--executive-light);
        font-family: 'Inter', sans-serif;
        color: var(--executive-text);
    }

    .command-header {
        background: linear-gradient(135deg, var(--executive-primary) 0%, var(--executive-secondary) 50%, var(--executive-accent) 100%);
        color: var(--executive-white);
        padding: 4rem 3rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        box-shadow: var(--shadow-primary);
    }

    .command-title {
        font-size: 4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -2px;
    }

    .command-subtitle {
        font-size: 1.5rem;
        margin-top: 1rem;
        opacity: 0.9;
        letter-spacing: 1px;
    }

    .classification-banner {
        background: var(--executive-red);
        color: var(--executive-white);
        padding: 1rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 2px;
        margin-top: 2rem;
    }

    .intelligence-card {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-primary);
        transition: all 0.3s ease;
    }

    .intelligence-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: var(--executive-accent);
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--executive-text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .intelligence-item {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-left: 4px solid var(--executive-accent);
    }

    .intelligence-item:hover {
        box-shadow: var(--shadow-primary);
        transform: translateX(4px);
    }

    .priority-critical {
        border-left-color: var(--executive-red);
        background: linear-gradient(90deg, rgba(220, 38, 38, 0.02), var(--executive-white));
    }

    .priority-high {
        border-left-color: var(--executive-amber);
        background: linear-gradient(90deg, rgba(217, 119, 6, 0.02), var(--executive-white));
    }

    .priority-medium {
        border-left-color: var(--executive-accent);
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.02), var(--executive-white));
    }

    .priority-low {
        border-left-color: var(--executive-green);
        background: linear-gradient(90deg, rgba(5, 150, 105, 0.02), var(--executive-white));
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--executive-text);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--executive-border);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-badge {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-critical { background: #FEE2E2; color: var(--executive-red); }
    .status-high { background: #FEF3C7; color: var(--executive-amber); }
    .status-medium { background: #DBEAFE; color: var(--executive-accent); }
    .status-low { background: #D1FAE5; color: var(--executive-green); }

    .source-link {
        color: var(--executive-accent);
        text-decoration: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: 1px solid var(--executive-accent);
        transition: all 0.3s ease;
        display: inline-block;
        margin-top: 0.5rem;
    }

    .source-link:hover {
        background: var(--executive-accent);
        color: white;
        text-decoration: none;
    }

    .api-status {
        padding: 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        text-align: center;
        margin: 0.25rem 0;
    }

    .api-active { background: #D1FAE5; color: var(--executive-green); }
    .api-inactive { background: #FEE2E2; color: var(--executive-red); }
</style>
""", unsafe_allow_html=True)

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
    """Classify content by region using keyword analysis"""
    regional_keywords = {
        'Eastern Europe': [
            'ukraine', 'russia', 'belarus', 'poland', 'baltic', 'estonia',
            'latvia', 'lithuania', 'moldova', 'romania', 'bulgaria', 'moscow', 'kyiv'
        ],
        'Asia Pacific': [
            'china', 'taiwan', 'japan', 'korea', 'australia', 'singapore',
            'thailand', 'vietnam', 'philippines', 'indonesia', 'india', 'beijing',
            'tokyo', 'seoul', 'pyongyang', 'taipei'
        ],
        'Middle East': [
            'iran', 'israel', 'palestine', 'saudi', 'gulf', 'syria',
            'lebanon', 'jordan', 'iraq', 'yemen', 'qatar', 'uae', 'tehran',
            'damascus', 'baghdad', 'jerusalem', 'gaza'
        ],
        'Europe': [
            'nato', 'eu', 'france', 'germany', 'uk', 'britain', 'italy',
            'spain', 'netherlands', 'belgium', 'sweden', 'norway', 'paris',
            'berlin', 'london'
        ],
        'Africa': [
            'sudan', 'egypt', 'libya', 'algeria', 'morocco', 'nigeria',
            'ethiopia', 'somalia', 'chad', 'mali', 'sahel', 'cairo'
        ],
        'Americas': [
            'usa', 'canada', 'mexico', 'brazil', 'argentina', 'venezuela',
            'colombia', 'cuba', 'haiti', 'washington', 'ottawa'
        ]
    }
    
    for region, keywords in regional_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return region
    
    return 'Global'

# ============================================================================
# REAL DATA COLLECTION FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def fetch_verified_news_intelligence():
    """Fetch real news intelligence from verified RSS sources"""
    intelligence_items = []
    
    for source_name, url in VERIFIED_NEWS_SOURCES.items():
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
            else:
                feed = feedparser.parse(url)
            
            for entry in feed.entries[:10]:
                if not entry.title or len(entry.title) < 15:
                    continue
                
                text = f"{entry.title} {entry.get('summary', '')}"
                sentiment = TextBlob(text).sentiment.polarity
                
                # Real intelligence scoring based on keywords
                critical_keywords = [
                    'nuclear', 'missile', 'attack', 'invasion', 'war', 'bombing',
                    'terrorist', 'assassination', 'coup', 'revolution'
                ]
                
                high_keywords = [
                    'military', 'conflict', 'crisis', 'sanctions', 'diplomacy',
                    'intelligence', 'security', 'cyber', 'espionage', 'defense'
                ]
                
                medium_keywords = [
                    'tension', 'dispute', 'exercise', 'alliance', 'treaty',
                    'strategic', 'geopolitical', 'bilateral', 'trade war'
                ]
                
                text_lower = text.lower()
                critical_score = sum(4 for k in critical_keywords if k in text_lower)
                high_score = sum(2 for k in high_keywords if k in text_lower)
                medium_score = sum(1 for k in medium_keywords if k in text_lower)
                
                relevance_score = min(10, 3 + critical_score + high_score + medium_score)
                
                # Source credibility based on real reputation
                credibility_scores = {
                    'reuters': 10, 'ap': 10, 'bbc': 9, 'financial times': 9,
                    'wall street journal': 9, 'washington post': 8, 'nyt': 8,
                    'bloomberg': 8, 'cnn': 7, 'guardian': 8, 'al jazeera': 7,
                    'defense news': 8, 'breaking defense': 7, 'military times': 7,
                    'cfr': 9, 'csis': 9, 'isw': 9, 'atlantic council': 8,
                    'foreign policy': 8, 'brookings': 8, 'carnegie': 8
                }
                
                source_lower = source_name.lower()
                credibility = next((v for k, v in credibility_scores.items() 
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
                
                intelligence_items.append({
                    'source': source_name,
                    'category': 'Verified News Intelligence',
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
                    'type': 'verified_news'
                })
                
        except Exception as e:
            continue  # Skip failed sources silently
    
    return sorted(intelligence_items, key=lambda x: x['intelligence_score'], reverse=True)

@st.cache_data(ttl=300)
def fetch_real_reddit_intelligence():
    """Fetch real Reddit intelligence using your API credentials"""
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
        return []
    
    try:
        import praw
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        
        # Real subreddits for intelligence gathering
        strategic_subreddits = {
            'worldnews': {'region': 'Global', 'weight': 1.2, 'min_score': 100},
            'geopolitics': {'region': 'Global', 'weight': 1.8, 'min_score': 50},
            'ukraine': {'region': 'Eastern Europe', 'weight': 2.0, 'min_score': 50},
            'taiwan': {'region': 'Asia Pacific', 'weight': 1.7, 'min_score': 25},
            'MiddleEastNews': {'region': 'Middle East', 'weight': 1.5, 'min_score': 25},
            'intelligence': {'region': 'Global', 'weight': 1.9, 'min_score': 10},
            'Military': {'region': 'Global', 'weight': 1.3, 'min_score': 50},
            'CredibleDefense': {'region': 'Global', 'weight': 1.6, 'min_score': 25},
            'syriancivilwar': {'region': 'Middle East', 'weight': 1.4, 'min_score': 25},
            'NATONews': {'region': 'Europe', 'weight': 1.3, 'min_score': 10}
        }
        
        reddit_intelligence = []
        
        for subreddit_name, config in strategic_subreddits.items():
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                for post in subreddit.hot(limit=15):
                    if (post.score >= config['min_score'] and 
                        not post.stickied and 
                        not post.over_18 and
                        len(post.title) > 20):
                        
                        text = f"{post.title} {post.selftext[:200]}"
                        sentiment = TextBlob(text).sentiment.polarity
                        
                        # Real intelligence scoring
                        intelligence_keywords = [
                            'breaking', 'confirmed', 'verified', 'official',
                            'military', 'defense', 'security', 'intelligence',
                            'conflict', 'crisis', 'war', 'attack'
                        ]
                        
                        text_lower = text.lower()
                        keyword_score = sum(1.5 for keyword in intelligence_keywords if keyword in text_lower)
                        
                        # Social engagement metrics
                        engagement_score = min(3, post.score / 500)
                        ratio_score = post.upvote_ratio * 2
                        comment_score = min(2, post.num_comments / 50)
                        
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
                            'content': post.selftext[:300] if post.selftext else 'External content - click to view',
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
        
    except ImportError:
        return []
    except Exception:
        return []

@st.cache_data(ttl=300)
def fetch_real_newsapi_intelligence():
    """Fetch real news using NewsAPI with your key"""
    if not NEWSAPI_KEY:
        return []
    
    try:
        from newsapi import NewsApiClient
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        
        # Real search queries for intelligence
        intelligence_queries = [
            'military conflict',
            'geopolitical crisis',
            'national security',
            'international relations',
            'defense intelligence'
        ]
        
        newsapi_intelligence = []
        
        for query in intelligence_queries[:3]:  # Limit to avoid rate limits
            try:
                articles = newsapi.get_everything(
                    q=query,
                    language='en',
                    sort_by='relevancy',
                    page_size=10,
                    domains='reuters.com,apnews.com,bbc.com,cnn.com,ft.com,wsj.com'
                )
                
                for article in articles.get('articles', []):
                    if (article.get('title') and 
                        '[Removed]' not in article.get('title', '') and
                        len(article.get('title', '')) > 20):
                        
                        text = f"{article.get('title', '')} {article.get('description', '')}"
                        sentiment = TextBlob(text).sentiment.polarity
                        
                        source_name = article.get('source', {}).get('name', '').lower()
                        
                        # Real credibility scoring
                        credibility_map = {
                            'reuters': 10, 'associated press': 10, 'bbc news': 9,
                            'cnn': 7, 'financial times': 9, 'wall street journal': 9
                        }
                        
                        credibility = next((v for k, v in credibility_map.items() 
                                          if k in source_name), 6)
                        
                        # Intelligence relevance
                        intel_keywords = ['military', 'security', 'intelligence', 'conflict', 'crisis']
                        relevance = min(10, 5 + sum(1 for k in intel_keywords if k in text.lower()))
                        
                        intelligence_score = (credibility + relevance) / 2
                        
                        priority = 'CRITICAL' if intelligence_score >= 8.5 else \
                                  'HIGH' if intelligence_score >= 7 else \
                                  'MEDIUM' if intelligence_score >= 5 else 'LOW'
                        
                        region = classify_region(text.lower())
                        
                        newsapi_intelligence.append({
                            'source': f"NewsAPI - {article.get('source', {}).get('name', 'Unknown')}",
                            'category': 'Premium News Intelligence',
                            'title': article.get('title', ''),
                            'content': article.get('description', '')[:400],
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
                            'type': 'newsapi_intelligence'
                        })
                        
            except Exception:
                continue
                
        return sorted(newsapi_intelligence, key=lambda x: x['intelligence_score'], reverse=True)
        
    except ImportError:
        return []
    except Exception:
        return []

@st.cache_data(ttl=300)
def fetch_real_market_data():
    """Fetch real market data using yfinance"""
    
    # Real market tickers for intelligence analysis
    intelligence_tickers = {
        # Market Indices
       '^GSPC': {'name': 'S&P 500', 'category': 'Market Index', 'weight': 1.0},
       '^DJI': {'name': 'Dow Jones', 'category': 'Market Index', 'weight': 1.0},
       '^IXIC': {'name': 'NASDAQ', 'category': 'Market Index', 'weight': 1.0},
       '^VIX': {'name': 'VIX Volatility Index', 'category': 'Market Stress', 'weight': 2.0},
       
       # Defense Contractors
       'LMT': {'name': 'Lockheed Martin', 'category': 'Defense', 'weight': 1.8},
       'RTX': {'name': 'Raytheon Technologies', 'category': 'Defense', 'weight': 1.8},
       'BA': {'name': 'Boeing', 'category': 'Defense', 'weight': 1.6},
       'NOC': {'name': 'Northrop Grumman', 'category': 'Defense', 'weight': 1.7},
       'GD': {'name': 'General Dynamics', 'category': 'Defense', 'weight': 1.7},
       'LHX': {'name': 'L3Harris Technologies', 'category': 'Defense', 'weight': 1.5},
       
       # Intelligence & Cybersecurity
       'PLTR': {'name': 'Palantir Technologies', 'category': 'Intelligence', 'weight': 2.0},
       'CRWD': {'name': 'CrowdStrike', 'category': 'Cybersecurity', 'weight': 1.6},
       'PANW': {'name': 'Palo Alto Networks', 'category': 'Cybersecurity', 'weight': 1.5},
       
       # Safe Haven Assets
       'GLD': {'name': 'Gold ETF', 'category': 'Safe Haven', 'weight': 1.3},
       'TLT': {'name': '20+ Year Treasury', 'category': 'Safe Haven', 'weight': 1.2},
       'SLV': {'name': 'Silver ETF', 'category': 'Safe Haven', 'weight': 1.1},
       
       # Energy & Commodities
       'XLE': {'name': 'Energy Sector ETF', 'category': 'Energy', 'weight': 1.4},
       'USO': {'name': 'Oil ETF', 'category': 'Energy', 'weight': 1.5},
       'UNG': {'name': 'Natural Gas ETF', 'category': 'Energy', 'weight': 1.2},
       
       # Currency ETFs
       'UUP': {'name': 'US Dollar ETF', 'category': 'Currency', 'weight': 1.1},
       'FXE': {'name': 'Euro ETF', 'category': 'Currency', 'weight': 1.0},
       'FXY': {'name': 'Japanese Yen ETF', 'category': 'Currency', 'weight': 1.0},
       
       # Regional ETFs
       'EWZ': {'name': 'Brazil ETF', 'category': 'Emerging Markets', 'weight': 1.1},
       'FXI': {'name': 'China Large Cap ETF', 'category': 'Emerging Markets', 'weight': 1.3},
       'EWY': {'name': 'South Korea ETF', 'category': 'Emerging Markets', 'weight': 1.2}
   }
   
   market_data = []
   
   for ticker, info in intelligence_tickers.items():
       try:
           stock = yf.Ticker(ticker)
           hist = stock.history(period="5d")
           
           if hist.empty:
               continue
           
           current_price = float(hist['Close'].iloc[-1])
           previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
           change_pct = ((current_price - previous_price) / previous_price) * 100 if previous_price else 0.0
           
           # Calculate volatility and volume metrics
           volatility = hist['Close'].pct_change().std() * 100 if len(hist) > 1 else 0
           volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
           avg_volume = hist['Volume'].mean() if 'Volume' in hist.columns else 0
           volume_ratio = volume / avg_volume if avg_volume > 0 else 1
           
           # Intelligence significance
           price_significance = abs(change_pct) * info['weight']
           volume_significance = min(3, abs(volume_ratio - 1) * 2)
           
           total_significance = price_significance + volume_significance
           
           market_data.append({
               'ticker': ticker,
               'name': info['name'],
               'category': info['category'],
               'current_price': current_price,
               'change_pct': change_pct,
               'volatility': volatility,
               'volume': volume,
               'volume_ratio': volume_ratio,
               'significance_score': total_significance,
               'timestamp': datetime.utcnow()
           })
           
       except Exception:
           continue
   
   return sorted(market_data, key=lambda x: x['significance_score'], reverse=True)

@st.cache_data(ttl=600)
def fetch_gdelt_events():
   """Fetch real GDELT global events data"""
   try:
       # GDELT Event Database API
       gdelt_url = "https://api.gdeltproject.org/api/v2/doc/doc"
       params = {
           'query': 'military OR conflict OR security OR crisis OR geopolitical',
           'mode': 'ArtList',
           'maxrecords': 25,
           'format': 'json',
           'timespan': '24h'
       }
       
       response = requests.get(gdelt_url, params=params, timeout=15)
       
       if response.status_code == 200:
           data = response.json()
           gdelt_events = []
           
           for article in data.get('articles', []):
               title = article.get('title', '')
               if len(title) < 20:
                   continue
               
               text = f"{title} {article.get('summary', '')}"
               sentiment = TextBlob(text).sentiment.polarity
               
               # GDELT intelligence scoring
               intel_terms = [
                   'military', 'conflict', 'security', 'defense', 'crisis',
                   'intelligence', 'strategic', 'geopolitical', 'war'
               ]
               
               relevance = min(10, 4 + sum(1 for term in intel_terms if term in text.lower()))
               
               priority = 'HIGH' if relevance >= 8 else 'MEDIUM' if relevance >= 6 else 'LOW'
               
               gdelt_events.append({
                   'source': 'GDELT Global Database',
                   'category': 'Global Events Intelligence',
                   'title': title,
                   'content': article.get('summary', '')[:400],
                   'url': article.get('url', ''),
                   'sentiment_polarity': sentiment,
                   'sentiment_label': classify_sentiment(sentiment),
                   'credibility_score': 8.0,
                   'relevance_score': relevance,
                   'intelligence_score': (8.0 + relevance) / 2,
                   'priority': priority,
                   'region': classify_region(text.lower()),
                   'timestamp': datetime.utcnow(),
                   'type': 'gdelt_events'
               })
           
           return sorted(gdelt_events, key=lambda x: x['intelligence_score'], reverse=True)
       
   except Exception:
       return []

# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class IntelligenceAnalyticsEngine:
   """Professional analytics for intelligence assessment"""
   
   def __init__(self):
       self.priority_weights = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
       self.regional_weights = {
           'Eastern Europe': 2.0, 'Middle East': 1.8, 'Asia Pacific': 1.6,
           'Europe': 1.3, 'Africa': 1.2, 'Americas': 1.1, 'Global': 1.4
       }
   
   def generate_threat_assessment(self, all_intelligence, market_data):
       """Generate comprehensive threat assessment"""
       
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
       
       # Sentiment analysis
       sentiments = [item.get('sentiment_polarity', 0) for item in all_intelligence]
       avg_sentiment = np.mean(sentiments) if sentiments else 0
       sentiment_volatility = np.std(sentiments) if len(sentiments) > 1 else 0
       
       # Market stress calculation
       market_stress_index = self._calculate_market_stress(market_data)
       
       # Regional analysis
       regional_assessment = self._analyze_regional_threats(all_intelligence)
       
       # Overall threat calculation
       base_threat = (critical_items * 4) + (high_items * 2) + (medium_items * 1)
       market_threat = market_stress_index * 1.5
       sentiment_threat = (abs(avg_sentiment) * 2) + (sentiment_volatility * 3)
       regional_threat = max([data.get('threat_level', 0) for data in regional_assessment.values()], default=0)
       
       overall_threat = min(10, (base_threat + market_threat + sentiment_threat + regional_threat) / 4)
       
       # Threat classification
       if overall_threat >= 8:
           threat_level = 'CRITICAL'
       elif overall_threat >= 6:
           threat_level = 'HIGH'
       elif overall_threat >= 4:
           threat_level = 'ELEVATED'
       else:
           threat_level = 'NORMAL'
       
       # Source diversity
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
           'timestamp': datetime.now()
       }
   
   def _calculate_market_stress(self, market_data):
       """Calculate market stress index"""
       if not market_data:
           return 0
       
       stress_indicators = []
       
       # VIX analysis
       vix_data = [item for item in market_data if 'VIX' in item['name']]
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
       
       # Defense sector performance
       defense_items = [item for item in market_data if item['category'] == 'Defense']
       if defense_items:
           defense_performance = np.mean([item['change_pct'] for item in defense_items])
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
           stress_indicators.append(min(8, max(0, safe_haven_performance * 2)))
       
       # Overall volatility
       volatilities = [item.get('volatility', 0) for item in market_data]
       if volatilities:
           avg_volatility = np.mean(volatilities)
           stress_indicators.append(min(10, avg_volatility))
       
       return np.mean(stress_indicators) if stress_indicators else 0
   
   def _analyze_regional_threats(self, all_intelligence):
       """Analyze threats by region"""
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
       
       # Calculate threat levels
       for region, data in regional_data.items():
           critical_weight = data['critical'] * 4
           high_weight = data['high'] * 2
           medium_weight = data['medium'] * 1
           
           avg_sentiment = np.mean(data['sentiments']) if data['sentiments'] else 0
           avg_intelligence = np.mean(data['intelligence_scores']) if data['intelligence_scores'] else 0
           
           regional_significance = self.regional_weights.get(region, 1.0)
           
           threat_level = min(10, ((critical_weight + high_weight + medium_weight) * regional_significance + 
                                  abs(avg_sentiment) * 2) / max(1, data['total_items']))
           
           data['threat_level'] = threat_level
           data['avg_sentiment'] = avg_sentiment
           data['avg_intelligence'] = avg_intelligence
           
           if threat_level >= 8:
               data['classification'] = 'CRITICAL'
           elif threat_level >= 6:
               data['classification'] = 'HIGH'
           elif threat_level >= 4:
               data['classification'] = 'ELEVATED'
           else:
               data['classification'] = 'NORMAL'
       
       return regional_data
   
   def _baseline_assessment(self):
       """Baseline assessment when no data"""
       return {
           'overall_threat_score': 0, 'threat_level': 'NORMAL', 'intelligence_quality': 0,
           'total_sources': 0, 'critical_items': 0, 'high_items': 0, 'medium_items': 0,
           'avg_sentiment': 0, 'sentiment_volatility': 0, 'market_stress_index': 0,
           'regional_assessment': {}, 'source_diversity': 0, 'confidence_score': 0,
           'timestamp': datetime.now()
       }

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_threat_gauge(threat_score, threat_level):
   """Create professional threat assessment gauge"""
   
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
       title={'text': f"THREAT LEVEL: {threat_level}", 
              'font': {'size': 18, 'color': '#0A0E27'}},
       number={'font': {'size': 40, 'color': color_mapping.get(threat_level, '#6B7280')}},
       gauge={
           'axis': {'range': [None, 10], 'tickcolor': '#6B7280'},
           'bar': {'color': color_mapping.get(threat_level, '#6B7280'), 'thickness': 0.8},
           'steps': [
               {'range': [0, 2.5], 'color': '#F3F4F6'},
               {'range': [2.5, 5], 'color': '#E5E7EB'},
               {'range': [5, 7.5], 'color': '#D1D5DB'},
               {'range': [7.5, 10], 'color': '#9CA3AF'}
           ],
           'threshold': {
               'line': {'color': '#DC2626', 'width': 4},
               'thickness': 0.8,
               'value': 8
           }
       }
   ))
   
   fig.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27'},
       height=350,
       margin=dict(l=20, r=20, t=60, b=20)
   )
   
   return fig

def create_global_intelligence_map(hotspots, intelligence_data):
   """Create interactive global intelligence map"""
   
   # Create map centered globally
   m = folium.Map(
       location=[20, 0],
       zoom_start=2,
       tiles='CartoDB positron'
   )
   
   # Color mapping
   priority_colors = {
       'CRITICAL': '#DC2626',
       'HIGH': '#D97706',
       'MEDIUM': '#3B82F6',
       'LOW': '#059669'
   }
   
   # Add verified hotspots
   for location, data in hotspots.items():
       folium.CircleMarker(
           location=[data['lat'], data['lon']],
           radius=15 if data['priority'] == 'CRITICAL' else 10 if data['priority'] == 'HIGH' else 6,
           popup=folium.Popup(f"""
               <div style="font-family: Inter; min-width: 250px;">
                   <h4 style="margin: 0 0 10px 0; color: {priority_colors.get(data['priority'], '#6B7280')};">
                       {location}
                   </h4>
                   <p><strong>Priority:</strong> {data['priority']}</p>
                   <p><strong>Region:</strong> {data['region']}</p>
                   <p><strong>Type:</strong> {data['type']}</p>
                   <p><strong>Coordinates:</strong> {data['lat']:.4f}, {data['lon']:.4f}</p>
               </div>
           """, max_width=300),
           color=priority_colors.get(data['priority'], '#6B7280'),
           fill=True,
           fillColor=priority_colors.get(data['priority'], '#6B7280'),
           fillOpacity=0.8,
           weight=3
       ).add_to(m)
   
   return m

def create_market_dashboard(market_data):
   """Create market intelligence dashboard"""
   
   if not market_data:
       return None, None
   
   df = pd.DataFrame(market_data)
   
   # Performance by category
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
       font={'color': '#0A0E27'},
       height=400
   )
   
   # Risk vs Performance
   fig2 = px.scatter(
       df,
       x='volatility',
       y='change_pct',
       size='significance_score',
       color='category',
       hover_data=['name', 'ticker'],
       title="Risk vs Performance Analysis"
   )
   
   fig2.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       font={'color': '#0A0E27'},
       height=400
   )
   
   return fig1, fig2

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
       <p>Blis Analytics Professional Edition</p>
       <div class="classification-banner">INTERNAL USE ONLY</div>
   </div>
   """, unsafe_allow_html=True)
   
   # Sidebar Configuration
   st.sidebar.markdown("## INTELLIGENCE CONTROLS")
   
   # API Status Display
   st.sidebar.markdown("### API STATUS")
   
   reddit_status = "ACTIVE" if all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]) else "INACTIVE"
   newsapi_status = "ACTIVE" if NEWSAPI_KEY else "INACTIVE"
   polygon_status = "ACTIVE" if all([POLYGON_ACCESS_KEY, POLYGON_SECRET_KEY]) else "INACTIVE"
   
   st.sidebar.markdown(f"""
   <div class="api-status api-{'active' if reddit_status == 'ACTIVE' else 'inactive'}">
       Reddit API: {reddit_status}
   </div>
   <div class="api-status api-{'active' if newsapi_status == 'ACTIVE' else 'inactive'}">
       NewsAPI: {newsapi_status}
   </div>
   <div class="api-status api-{'active' if polygon_status == 'ACTIVE' else 'inactive'}">
       Polygon.io: {polygon_status}
   </div>
   """, unsafe_allow_html=True)
   
   # Controls
   regions = ['Global', 'Eastern Europe', 'Asia Pacific', 'Middle East', 'Europe', 'Africa', 'Americas']
   selected_regions = st.sidebar.multiselect("ACTIVE REGIONS", regions, default=['Global'])
   
   priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
   selected_priorities = st.sidebar.multiselect("PRIORITY LEVELS", priorities, default=priorities)
   
   min_score = st.sidebar.slider("MINIMUM INTELLIGENCE SCORE", 0.0, 10.0, 5.0, 0.1)
   
   if st.sidebar.button("REFRESH INTELLIGENCE", type="primary"):
       st.cache_data.clear()
       st.rerun()
   
   # Initialize analytics
   analytics = IntelligenceAnalyticsEngine()
   
   # Data collection
   st.markdown('<div class="section-header">INTELLIGENCE COLLECTION STATUS</div>', unsafe_allow_html=True)
   
   with st.container():
       col1, col2, col3, col4 = st.columns(4)
       
       # Collect all intelligence
       all_intelligence = []
       market_data = []
       
       with col1:
           with st.spinner("Collecting verified news..."):
               news_intel = fetch_verified_news_intelligence()
               all_intelligence.extend(news_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(news_intel)}</div>
               <div class="metric-label">NEWS SOURCES</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           with st.spinner("Analyzing social intelligence..."):
               reddit_intel = fetch_real_reddit_intelligence()
               all_intelligence.extend(reddit_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(reddit_intel)}</div>
               <div class="metric-label">SOCIAL INTEL</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           with st.spinner("Processing premium news..."):
               newsapi_intel = fetch_real_newsapi_intelligence()
               all_intelligence.extend(newsapi_intel)
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(newsapi_intel)}</div>
               <div class="metric-label">PREMIUM NEWS</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col4:
           with st.spinner("Analyzing markets..."):
               market_data = fetch_real_market_data()
           
           st.markdown(f"""
           <div class="intelligence-card">
               <div class="metric-value">{len(market_data)}</div>
               <div class="metric-label">MARKET ASSETS</div>
           </div>
           """, unsafe_allow_html=True)
   
   # Generate assessment
   assessment = analytics.generate_threat_assessment(all_intelligence, market_data)
   
   # Executive Dashboard
   st.markdown('<div class="section-header">EXECUTIVE INTELLIGENCE DASHBOARD</div>', unsafe_allow_html=True)
   
   col1, col2 = st.columns([1, 2])
   
   with col1:
       # Threat gauge
       threat_fig = create_threat_gauge(assessment['overall_threat_score'], assessment['threat_level'])
       st.plotly_chart(threat_fig, use_container_width=True)
       
       # Key metrics
       st.markdown(f"""
       <div class="intelligence-card">
           <h4>INTELLIGENCE SUMMARY</h4>
           <p><strong>Confidence Level:</strong> {assessment['confidence_score']:.0f}%</p>
           <p><strong>Intelligence Quality:</strong> {assessment['intelligence_quality']:.1f}/10</p>
           <p><strong>Market Stress Index:</strong> {assessment['market_stress_index']:.1f}/10</p>
           <p><strong>Source Diversity:</strong> {assessment['source_diversity']} categories</p>
           <p><strong>Last Updated:</strong> {assessment['timestamp'].strftime('%H:%M:%S UTC')}</p>
       </div>
       """, unsafe_allow_html=True)
   
   with col2:
       # Executive metrics
       col_a, col_b, col_c, col_d = st.columns(4)
       
       with col_a:
           st.metric("CRITICAL ITEMS", assessment['critical_items'])
       with col_b:
           st.metric("HIGH PRIORITY", assessment['high_items'])
       with col_c:
           st.metric("TOTAL SOURCES", assessment['total_sources'])
       with col_d:
           st.metric("AVG SENTIMENT", f"{assessment['avg_sentiment']:+.2f}")
       
       # Top intelligence preview
       st.markdown("#### PRIORITY INTELLIGENCE")
       top_items = [item for item in all_intelligence if item['priority'] in ['CRITICAL', 'HIGH']][:5]
       
       for item in top_items:
           priority_class = f"priority-{item['priority'].lower()}"
           st.markdown(f"""
           <div class="intelligence-item {priority_class}">
               <span class="status-badge status-{item['priority'].lower()}">{item['priority']}</span>
               <h5 style="margin: 0.5rem 0;">{item['title'][:80]}...</h5>
               <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">{item['source']} | Score: {item['intelligence_score']:.1f}/10</p>
           </div>
           """, unsafe_allow_html=True)
   
   # Main Tabs
   tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
       "GLOBAL INTELLIGENCE", 
       "MARKET ANALYSIS", 
       "INTELLIGENCE FEED", 
       "REGIONAL ASSESSMENT",
       "SOURCE ANALYSIS",
       "EXECUTIVE REPORTS"
   ])
   
   with tab1:
       st.markdown("### GLOBAL INTELLIGENCE MAP")
       
       # Interactive map
       intel_map = create_global_intelligence_map(REAL_GLOBAL_HOTSPOTS, all_intelligence)
       map_data = st_folium(intel_map, width=700, height=600)
       
       # Hotspot analysis
       st.markdown("### STRATEGIC HOTSPOTS ANALYSIS")
       
       for location, data in REAL_GLOBAL_HOTSPOTS.items():
           if data['region'] in selected_regions or 'Global' in selected_regions:
               priority_class = f"priority-{data['priority'].lower()}"
               st.markdown(f"""
               <div class="intelligence-item {priority_class}">
                   <h5>{location}</h5>
                   <p><strong>Priority:</strong> {data['priority']} | <strong>Region:</strong> {data['region']}</p>
                   <p><strong>Type:</strong> {data['type']} | <strong>Coordinates:</strong> {data['lat']:.4f}, {data['lon']:.4f}</p>
               </div>
               """, unsafe_allow_html=True)
   
   with tab2:
       st.markdown("### MARKET INTELLIGENCE ANALYSIS")
       
       if market_data:
           # Market charts
           perf_fig, risk_fig = create_market_dashboard(market_data)
           
           col1, col2 = st.columns(2)
           with col1:
               if perf_fig:
                   st.plotly_chart(perf_fig, use_container_width=True)
           with col2:
               if risk_fig:
                   st.plotly_chart(risk_fig, use_container_width=True)
           
           # Market stress indicators
           st.markdown("### MARKET STRESS INDICATORS
           # Market stress analysis
           high_stress_assets = [asset for asset in market_data if abs(asset['change_pct']) > 3 or asset.get('volatility', 0) > 5]
           
           if high_stress_assets:
               st.markdown("#### HIGH STRESS ASSETS")
               for asset in high_stress_assets:
                   stress_class = "priority-critical" if abs(asset['change_pct']) > 5 else "priority-high"
                   st.markdown(f"""
                   <div class="intelligence-item {stress_class}">
                       <h5>{asset['name']} ({asset['ticker']})</h5>
                       <p><strong>Current Price:</strong> ${asset['current_price']:.2f}</p>
                       <p><strong>Change:</strong> {asset['change_pct']:+.2f}% | <strong>Volatility:</strong> {asset['volatility']:.2f}%</p>
                       <p><strong>Category:</strong> {asset['category']} | <strong>Significance:</strong> {asset['significance_score']:.1f}</p>
                   </div>
                   """, unsafe_allow_html=True)
           
           # Market data table
           st.markdown("### DETAILED MARKET DATA")
           df = pd.DataFrame(market_data)
           st.dataframe(df[['name', 'current_price', 'change_pct', 'volatility', 'category']], use_container_width=True)
       else:
           st.warning("Market intelligence unavailable")
   
   with tab3:
       st.markdown("### LIVE INTELLIGENCE FEED")
       
       # Advanced filtering
       col1, col2, col3 = st.columns(3)
       
       with col1:
           source_filter = st.selectbox("SOURCE TYPE", 
               ["All Sources", "Verified News", "Social Intelligence", "Premium News", "GDELT Events"])
       
       with col2:
           category_filter = st.selectbox("CATEGORY", 
               ["All Categories"] + list(set(item.get('category', 'Unknown') for item in all_intelligence)))
       
       with col3:
           max_items = st.slider("MAXIMUM ITEMS", 10, 100, 50, 10)
       
       # Filter intelligence
       filtered_intelligence = []
       
       for item in all_intelligence:
           # Apply filters
           if (item.get('intelligence_score', 0) >= min_score and
               item.get('priority') in selected_priorities and
               item.get('region') in selected_regions + ['Global']):
               
               # Source type filter
               if source_filter != "All Sources":
                   if source_filter == "Verified News" and item.get('type') != 'verified_news':
                       continue
                   elif source_filter == "Social Intelligence" and item.get('type') != 'social_intelligence':
                       continue
                   elif source_filter == "Premium News" and item.get('type') != 'newsapi_intelligence':
                       continue
                   elif source_filter == "GDELT Events" and item.get('type') != 'gdelt_events':
                       continue
               
               # Category filter
               if category_filter != "All Categories" and item.get('category') != category_filter:
                   continue
               
               filtered_intelligence.append(item)
       
       # Sort and limit
       filtered_intelligence.sort(key=lambda x: x.get('intelligence_score', 0), reverse=True)
       filtered_intelligence = filtered_intelligence[:max_items]
       
       st.markdown(f"**Displaying {len(filtered_intelligence)} intelligence items**")
       
       # Display intelligence items
       for item in filtered_intelligence:
           priority_class = f"priority-{item.get('priority', 'medium').lower()}"
           
           st.markdown(f"""
           <div class="intelligence-item {priority_class}">
               <div style="margin-bottom: 1rem;">
                   <span class="status-badge status-{item.get('priority', 'medium').lower()}">{item.get('priority', 'MEDIUM')}</span>
                   <span style="margin-left: 1rem; font-weight: 600;">Score: {item.get('intelligence_score', 0):.1f}/10</span>
                   <span style="margin-left: 1rem; color: #6B7280;">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                   <span style="margin-left: 1rem; color: #6B7280;">Region: {item.get('region', 'Global')}</span>
               </div>
               
               <h4 style="margin-bottom: 0.5rem; color: #0A0E27;">{item['title']}</h4>
               
               <p style="margin-bottom: 1rem; color: #6B7280; line-height: 1.5;">
                   {item.get('content', '')[:400]}...
               </p>
               
               <div style="margin-bottom: 1rem; font-size: 0.9rem; color: #6B7280;">
                   <strong>Source:</strong> {item['source']} | 
                   <strong>Category:</strong> {item.get('category', 'Unknown')} | 
                   <strong>Sentiment:</strong> {item.get('sentiment_label', 'Neutral')} ({item.get('sentiment_polarity', 0):.2f}) |
                   <strong>Time:</strong> {item['timestamp'].strftime('%H:%M UTC')}
               </div>
               
               <a href="{item.get('url', '#')}" target="_blank" class="source-link">
                   VIEW SOURCE
               </a>
           </div>
           """, unsafe_allow_html=True)
   
   with tab4:
       st.markdown("### REGIONAL THREAT ASSESSMENT")
       
       regional_data = assessment['regional_assessment']
       
       if regional_data:
           # Regional threat chart
           regions_list = list(regional_data.keys())
           threat_levels = [data['threat_level'] for data in regional_data.values()]
           classifications = [data['classification'] for data in regional_data.values()]
           
           fig = go.Figure(data=[
               go.Bar(
                   y=regions_list,
                   x=threat_levels,
                   orientation='h',
                   marker_color=['#DC2626' if c == 'CRITICAL' else '#D97706' if c == 'HIGH' else '#3B82F6' if c == 'ELEVATED' else '#059669' for c in classifications],
                   text=[f"{level:.1f}" for level in threat_levels],
                   textposition='inside'
               )
           ])
           
           fig.update_layout(
               title="Regional Threat Assessment",
               xaxis_title="Threat Level (0-10)",
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font={'color': '#0A0E27'},
               height=400
           )
           
           st.plotly_chart(fig, use_container_width=True)
           
           # Detailed regional analysis
           st.markdown("### REGIONAL INTELLIGENCE BREAKDOWN")
           
           for region, data in sorted(regional_data.items(), key=lambda x: x[1]['threat_level'], reverse=True):
               if region in selected_regions or 'Global' in selected_regions:
                   classification_class = f"priority-{data['classification'].lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-card {classification_class}">
                       <h3>{region.upper()} - {data['classification']}</h3>
                       
                       <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0;">
                           <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                               <div style="font-size: 1.5rem; font-weight: 600;">{data['threat_level']:.1f}/10</div>
                               <div style="font-size: 0.8rem; opacity: 0.8;">THREAT LEVEL</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                               <div style="font-size: 1.5rem; font-weight: 600;">{data['total_items']}</div>
                               <div style="font-size: 0.8rem; opacity: 0.8;">TOTAL SOURCES</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                               <div style="font-size: 1.5rem; font-weight: 600;">{data['critical']}</div>
                               <div style="font-size: 0.8rem; opacity: 0.8;">CRITICAL ITEMS</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                               <div style="font-size: 1.5rem; font-weight: 600;">{data['avg_sentiment']:+.2f}</div>
                               <div style="font-size: 0.8rem; opacity: 0.8;">AVG SENTIMENT</div>
                           </div>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       else:
           st.info("Regional analysis will be available when intelligence data is collected")
   
   with tab5:
       st.markdown("### SOURCE ANALYSIS & CREDIBILITY")
       
       if all_intelligence:
           # Source analysis
           source_analysis = {}
           
           for item in all_intelligence:
               source = item['source']
               if source not in source_analysis:
                   source_analysis[source] = {
                       'total_items': 0, 'avg_credibility': 0, 'avg_intelligence': 0,
                       'critical_items': 0, 'categories': set(), 'avg_sentiment': 0
                   }
               
               source_analysis[source]['total_items'] += 1
               source_analysis[source]['avg_credibility'] += item.get('credibility_score', 0)
               source_analysis[source]['avg_intelligence'] += item.get('intelligence_score', 0)
               source_analysis[source]['avg_sentiment'] += item.get('sentiment_polarity', 0)
               source_analysis[source]['categories'].add(item.get('category', 'Unknown'))
               
               if item.get('priority') == 'CRITICAL':
                   source_analysis[source]['critical_items'] += 1
           
           # Calculate averages
           for source, data in source_analysis.items():
               if data['total_items'] > 0:
                   data['avg_credibility'] /= data['total_items']
                   data['avg_intelligence'] /= data['total_items']
                   data['avg_sentiment'] /= data['total_items']
                   data['categories'] = list(data['categories'])
           
           # Top sources by intelligence score
           top_sources = sorted(source_analysis.items(), 
                              key=lambda x: x[1]['avg_intelligence'], reverse=True)[:15]
           
           st.markdown("### TOP INTELLIGENCE SOURCES")
           
           for source, data in top_sources:
               st.markdown(f"""
               <div class="intelligence-card">
                   <h4>{source}</h4>
                   <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                       <div style="text-align: center;">
                           <div class="metric-value" style="font-size: 1.5rem;">{data['avg_intelligence']:.1f}</div>
                           <div class="metric-label">AVG INTELLIGENCE</div>
                       </div>
                       <div style="text-align: center;">
                           <div class="metric-value" style="font-size: 1.5rem;">{data['avg_credibility']:.1f}</div>
                           <div class="metric-label">AVG CREDIBILITY</div>
                       </div>
                       <div style="text-align: center;">
                           <div class="metric-value" style="font-size: 1.5rem;">{data['total_items']}</div>
                           <div class="metric-label">TOTAL ITEMS</div>
                       </div>
                       <div style="text-align: center;">
                           <div class="metric-value" style="font-size: 1.5rem;">{data['critical_items']}</div>
                           <div class="metric-label">CRITICAL ITEMS</div>
                       </div>
                   </div>
                   <p style="margin-top: 1rem;"><strong>Categories:</strong> {', '.join(data['categories'][:3])}{'...' if len(data['categories']) > 3 else ''}</p>
                   <p><strong>Avg Sentiment:</strong> {data['avg_sentiment']:+.2f}</p>
               </div>
               """, unsafe_allow_html=True)
       else:
           st.info("Source analysis will be available when intelligence data is collected")
   
   with tab6:
       st.markdown("### EXECUTIVE REPORTS & EXPORTS")
       
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
                   'intelligence_overview': {
                       'total_sources': assessment['total_sources'],
                       'critical_items': assessment['critical_items'],
                       'high_priority_items': assessment['high_items'],
                       'intelligence_quality': assessment['intelligence_quality'],
                       'market_stress_index': assessment['market_stress_index']
                   },
                   'regional_assessment': assessment['regional_assessment'],
                   'source_breakdown': {
                       'verified_news': len([i for i in all_intelligence if i.get('type') == 'verified_news']),
                       'social_intelligence': len([i for i in all_intelligence if i.get('type') == 'social_intelligence']),
                       'premium_news': len([i for i in all_intelligence if i.get('type') == 'newsapi_intelligence']),
                       'gdelt_events': len([i for i in all_intelligence if i.get('type') == 'gdelt_events'])
                   },
                   'api_status': {
                       'reddit_api': reddit_status,
                       'newsapi': newsapi_status,
                       'polygon_api': polygon_status
                   }
               }
               
               summary_json = json.dumps(executive_summary, indent=2, default=str)
               st.download_button(
                   label="DOWNLOAD EXECUTIVE SUMMARY",
                   data=summary_json,
                   file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col2:
           if st.button("GENERATE DETAILED REPORT"):
               detailed_report = {
                   'report_timestamp': datetime.now().isoformat(),
                   'classification': 'INTERNAL USE ONLY',
                   'executive_assessment': assessment,
                   'intelligence_data': {
                       'total_items': len(all_intelligence),
                       'intelligence_items': all_intelligence[:50],  # Limit for file size
                       'market_data': market_data
                   },
                   'hotspots_analysis': REAL_GLOBAL_HOTSPOTS,
                   'collection_metadata': {
                       'collection_time': datetime.now().isoformat(),
                       'sources_active': len(VERIFIED_NEWS_SOURCES),
                       'api_status': {
                           'reddit': reddit_status,
                           'newsapi': newsapi_status,
                           'polygon': polygon_status
                       }
                   }
               }
               
               report_json = json.dumps(detailed_report, indent=2, default=str)
               st.download_button(
                   label="DOWNLOAD DETAILED REPORT",
                   data=report_json,
                   file_name=f"detailed_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col3:
           if st.button("EXPORT THREAT BRIEFING"):
               # Generate formatted threat briefing
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
Market Stress Index: {assessment['market_stress_index']:.1f}/10

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

TOP PRIORITY INTELLIGENCE
--------------------------
"""
               
               critical_items = [item for item in all_intelligence if item.get('priority') == 'CRITICAL'][:5]
               for item in critical_items:
                   briefing += f"""
CRITICAL: {item['title'][:100]}...
Source: {item['source']}
Region: {item.get('region', 'Global')}
Score: {item.get('intelligence_score', 0):.1f}/10
URL: {item.get('url', 'N/A')}

"""
               
               briefing += f"""
API STATUS
----------
Reddit API: {reddit_status}
NewsAPI: {newsapi_status}
Polygon API: {polygon_status}

NEXT ASSESSMENT: {(datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S UTC')}

END OF BRIEFING
===============
"""
               
               st.download_button(
                   label="DOWNLOAD THREAT BRIEFING",
                   data=briefing,
                   file_name=f"threat_briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                   mime="text/plain"
               )
       
       # Current assessment display
       st.markdown("### CURRENT ASSESSMENT OVERVIEW")
       
       st.markdown(f"""
       <div class="intelligence-card">
           <h4>SYSTEM STATUS</h4>
           <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
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
                   <strong>Sentiment:</strong> {assessment['avg_sentiment']:+.2f}<br>
                   <strong>Last Update:</strong> {assessment['timestamp'].strftime('%H:%M UTC')}<br>
                   <strong>Active APIs:</strong> {sum([1 for status in [reddit_status, newsapi_status, polygon_status] if status == 'ACTIVE'])}/3
               </div>
           </div>
       </div>
       """, unsafe_allow_html=True)
   
   # Footer
   st.markdown("---")
   st.markdown(f"""
   <div style="text-align: center; color: #6B7280; font-size: 0.9rem; padding: 2rem 0;">
       <p><strong>Strategic Intelligence Command Center</strong> | 
       Blis Analytics Professional Edition | 
       Classification: INTERNAL USE ONLY</p>
       <p>System Status: OPERATIONAL | 
       Sources Active: {len([status for status in [reddit_status, newsapi_status, polygon_status] if status == 'ACTIVE'])}/3 APIs | 
       Intelligence Items: {len(all_intelligence)} | 
       Last Collection: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Blis signature
   st.markdown("""
   <div style="position: fixed; bottom: 20px; right: 20px; background: #0A0E27; color: white; 
               padding: 1rem 2rem; font-weight: 600; font-size: 0.9rem; letter-spacing: 1px; 
               z-index: 1000; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
       BLIS ANALYTICS
   </div>
   """, unsafe_allow_html=True)

if __name__ == "__main__":
   main()
