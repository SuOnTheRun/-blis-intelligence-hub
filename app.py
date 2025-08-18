# ============================================================================
# ULTIMATE WHITE LUXURY INTELLIGENCE HUB v4.0
# Sophisticated • Minimalist • Executive Grade
# White Design System with Elegant Accents
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
# WHITE LUXURY DESIGN SYSTEM
# ============================================================================

st.set_page_config(
    page_title="Global Strategic Intelligence Hub",
    page_icon="⚪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SOPHISTICATED WHITE LUXURY STYLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=IBM+Plex+Sans:wght@200;300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    :root {
        --pure-white: #FFFFFF;
        --soft-white: #FAFAFA;
        --light-gray: #F5F5F5;
        --subtle-gray: #E8E8E8;
        --medium-gray: #CCCCCC;
        --charcoal: #222222;
        --jet-black: #000000;
        --navy-blue: #003366;
        --executive-gold: #C9A227;
        --emerald-green: #2E8B57;
        --scarlet-red: #B22222;
        --soft-blue: #E6F3FF;
        --soft-gold: #FDF6E3;
        --soft-green: #F0F8F5;
        --soft-red: #FDF2F2;
        --shadow-subtle: rgba(0,0,0,0.04);
        --shadow-medium: rgba(0,0,0,0.08);
        --shadow-strong: rgba(0,0,0,0.12);
    }
    
    .stApp {
        background: var(--pure-white);
        color: var(--charcoal);
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    .luxury-header {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px var(--shadow-medium);
        position: relative;
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--navy-blue), var(--executive-gold), var(--emerald-green));
        background-size: 200% 100%;
        animation: gradient-flow 8s ease-in-out infinite;
    }
    
    @keyframes gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .luxury-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.2rem;
        font-weight: 200;
        letter-spacing: 2px;
        color: var(--navy-blue);
        margin: 0;
        line-height: 1.1;
    }
    
    .luxury-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 300;
        color: var(--charcoal);
        margin-top: 1rem;
        letter-spacing: 1px;
        opacity: 0.8;
    }
    
    .classification-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: var(--scarlet-red);
        color: var(--pure-white);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .luxury-card {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px var(--shadow-subtle);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
    }
    
    .luxury-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px var(--shadow-medium);
        border-color: var(--navy-blue);
    }
    
    .metric-card {
        text-align: center;
        padding: 2rem 1rem;
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        box-shadow: 0 4px 20px var(--shadow-subtle);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow-medium);
    }
    
    .metric-value {
        font-family: 'Space Grotesk', monospace;
        font-size: 2.8rem;
        font-weight: 600;
        color: var(--navy-blue);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--charcoal);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.7;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .score-excellent { color: var(--emerald-green); }
    .score-good { color: var(--executive-gold); }
    .score-warning { color: #FF8C00; }
    .score-critical { color: var(--scarlet-red); }
    
    .status-operational { color: var(--emerald-green); font-weight: 600; }
    .status-elevated { color: var(--executive-gold); font-weight: 600; }
    .status-critical { color: var(--scarlet-red); font-weight: 600; }
    
    .intelligence-section {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px var(--shadow-subtle);
        border-left: 4px solid var(--navy-blue);
    }
    
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--navy-blue);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .intelligence-item {
        background: var(--light-gray);
        border: 1px solid var(--subtle-gray);
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    
    .intelligence-item:hover {
        background: var(--soft-blue);
        border-color: var(--navy-blue);
        transform: translateX(4px);
    }
    
    .priority-critical { border-left: 4px solid var(--scarlet-red); }
    .priority-high { border-left: 4px solid #FF8C00; }
    .priority-medium { border-left: 4px solid var(--executive-gold); }
    .priority-low { border-left: 4px solid var(--emerald-green); }
    
    .tag-elegant {
        display: inline-block;
        background: var(--light-gray);
        color: var(--navy-blue);
        padding: 0.3rem 0.8rem;
        border: 1px solid var(--subtle-gray);
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Space Grotesk', monospace;
    }
    
    .tag-critical { background: var(--soft-red); color: var(--scarlet-red); border-color: var(--scarlet-red); }
    .tag-high { background: #FFF4E6; color: #FF8C00; border-color: #FF8C00; }
    .tag-medium { background: var(--soft-gold); color: var(--executive-gold); border-color: var(--executive-gold); }
    .tag-low { background: var(--soft-green); color: var(--emerald-green); border-color: var(--emerald-green); }
    
    .sentiment-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .sentiment-positive { background: var(--soft-green); color: var(--emerald-green); }
    .sentiment-negative { background: var(--soft-red); color: var(--scarlet-red); }
    .sentiment-neutral { background: var(--light-gray); color: var(--charcoal); }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.8rem;
        background: var(--scarlet-red);
        color: var(--pure-white);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
        animation: pulse-subtle 3s infinite;
        box-shadow: 0 4px 15px rgba(178, 34, 34, 0.2);
    }
    
    @keyframes pulse-subtle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: var(--pure-white);
        border-radius: 50%;
        animation: pulse-dot 2s infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
    }
    
    .interactive-button {
        background: linear-gradient(135deg, var(--navy-blue), #004080);
        color: var(--pure-white);
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 15px rgba(0, 51, 102, 0.2);
    }
    
    .interactive-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 51, 102, 0.3);
    }
    
    .risk-dial {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px var(--shadow-subtle);
    }
    
    .emotional-radar {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px var(--shadow-subtle);
    }
    
    div[data-testid="stSidebar"] {
        background: var(--soft-white);
        border-right: 1px solid var(--subtle-gray);
    }
    
    div[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--light-gray);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid var(--subtle-gray);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--charcoal);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
        padding: 1rem 1.5rem;
        margin: 0.2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--soft-blue);
        color: var(--navy-blue);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--navy-blue);
        color: var(--pure-white);
        font-weight: 600;
    }
    
    .human-pulse-card {
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px var(--shadow-subtle);
    }
    
    .emotion-meter {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding: 0.8rem;
        border-radius: 8px;
        background: var(--light-gray);
    }
    
    .emotion-label {
        font-weight: 600;
        color: var(--charcoal);
        font-size: 0.9rem;
    }
    
    .emotion-score {
        font-family: 'Space Grotesk', monospace;
        font-weight: 700;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ENHANCED DATA COLLECTION WITH SENTIMENT ANALYSIS
# ============================================================================

class WhiteLuxuryIntelligenceCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Strategic-Intelligence-Hub/4.0 (Executive)'
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
        
        # SOPHISTICATED INTELLIGENCE SOURCES
        self.intelligence_sources = {
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
                'War on the Rocks': 'https://warontherocks.com/feed/'
            },
            'economic_warfare': {
                'Bloomberg Markets': 'https://feeds.bloomberg.com/markets/news.rss',
                'MarketWatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
                'Economic Times': 'https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms'
            },
            'conflict_monitoring': {
                'LiveUAMap': 'https://liveuamap.com/rss',
                'Crisis Group': 'https://www.crisisgroup.org/rss.xml'
            }
        }
        
        # HUMAN-CENTRIC SUBREDDIT NETWORK
        self.human_intelligence_subreddits = {
            'worldnews': {'weight': 1.0, 'region': 'Global', 'human_factor': 'Public Opinion'},
            'geopolitics': {'weight': 1.0, 'region': 'Global', 'human_factor': 'Strategic Thinking'},
            'UkraineConflict': {'weight': 0.9, 'region': 'Eastern Europe', 'human_factor': 'Conflict Psychology'},
            'syriancivilwar': {'weight': 0.8, 'region': 'Middle East', 'human_factor': 'Regional Sentiment'},
            'china': {'weight': 0.9, 'region': 'Asia Pacific', 'human_factor': 'Superpower Perception'},
            'russia': {'weight': 0.9, 'region': 'Eastern Europe', 'human_factor': 'Authoritarian Response'},
            'investing': {'weight': 0.7, 'region': 'Global', 'human_factor': 'Market Psychology'},
            'security': {'weight': 0.8, 'region': 'Global', 'human_factor': 'Security Concerns'}
        }

    @st.cache_data(ttl=300)
    def collect_human_intelligence(_self):
        """Collect human-centric intelligence with emotional analysis"""
        if not _self.reddit:
            return []
        
        intelligence = []
        
        for subreddit_name, config in _self.human_intelligence_subreddits.items():
            try:
                subreddit = _self.reddit.subreddit(subreddit_name)
                posts = list(subreddit.hot(limit=20))
                
                for post in posts:
                    # Enhanced human sentiment analysis
                    full_text = f"{post.title} {post.selftext[:1000]}"
                    sentiment = TextBlob(full_text).sentiment
                    
                    # Human emotional indicators
                    emotional_analysis = _self._analyze_human_emotions(full_text)
                    
                    # Sophisticated scoring (1-10 scale)
                    credibility_score = _self._calculate_reddit_credibility(post, subreddit_name)
                    impact_score = _self._calculate_impact_score(post, sentiment, emotional_analysis)
                    human_interest_score = _self._calculate_human_interest(full_text, emotional_analysis)
                    
                    # Overall intelligence score (1-10)
                    intelligence_score = (credibility_score * 0.3 + impact_score * 0.4 + human_interest_score * 0.3)
                    
                    # Priority classification
                    if intelligence_score >= 8.5:
                        priority = 'CRITICAL'
                    elif intelligence_score >= 7.0:
                        priority = 'HIGH'
                    elif intelligence_score >= 5.0:
                        priority = 'MEDIUM'
                    else:
                        priority = 'LOW'
                    
                    # Enhanced metadata
                    created_time = datetime.fromtimestamp(post.created_utc)
                    
                    intelligence.append({
                        'source': f'Reddit r/{subreddit_name}',
                        'category': config['human_factor'],
                        'title': post.title,
                        'content_preview': post.selftext[:300] if post.selftext else 'Link post - click to view full content',
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'upvote_ratio': post.upvote_ratio,
                        'author': str(post.author) if post.author else 'Unknown',
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_subjectivity': sentiment.subjectivity,
                        'sentiment_label': _self._get_sentiment_label(sentiment.polarity),
                        'emotional_analysis': emotional_analysis,
                        'credibility_score': credibility_score,
                        'impact_score': impact_score,
                        'human_interest_score': human_interest_score,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': config['region'],
                        'human_factor': config['human_factor'],
                        'timestamp': created_time,
                        'type': 'human_intelligence',
                        'clickable': True
                    })
                    
            except Exception as e:
                continue
        
        return sorted(intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_news_intelligence(_self):
        """Collect sophisticated news intelligence"""
        news_intelligence = []
        
        for category, sources in _self.intelligence_sources.items():
            for source_name, url in sources.items():
                try:
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:15]:
                        # Enhanced content analysis
                        full_content = f"{entry.title} {entry.get('summary', '')} {entry.get('description', '')}"
                        sentiment = TextBlob(full_content).sentiment
                        
                        # Human impact analysis
                        human_impact = _self._analyze_human_impact(full_content)
                        emotional_analysis = _self._analyze_human_emotions(full_content)
                        
                        # Sophisticated scoring (1-10 scale)
                        credibility = _self._calculate_news_credibility(source_name)
                        relevance_score = _self._calculate_relevance_score(full_content)
                        urgency_score = _self._calculate_urgency_score(entry.title, full_content)
                        
                        # Overall intelligence score (1-10)
                        intelligence_score = (credibility * 0.4 + relevance_score * 0.3 + urgency_score * 0.3)
                        
                        # Priority classification
                        if intelligence_score >= 8.5 or 'BREAKING' in entry.title.upper():
                            priority = 'CRITICAL'
                        elif intelligence_score >= 7.0:
                            priority = 'HIGH'
                        elif intelligence_score >= 5.0:
                            priority = 'MEDIUM'
                        else:
                            priority = 'LOW'
                        
                        news_intelligence.append({
                            'source': source_name,
                            'category': category.replace('_', ' ').title(),
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:400],
                            'url': entry.link,
                            'published': entry.get('published', ''),
                            'sentiment_polarity': sentiment.polarity,
                            'sentiment_subjectivity': sentiment.subjectivity,
                            'sentiment_label': _self._get_sentiment_label(sentiment.polarity),
                            'emotional_analysis': emotional_analysis,
                            'human_impact': human_impact,
                            'credibility_score': credibility,
                            'relevance_score': relevance_score,
                            'urgency_score': urgency_score,
                            'intelligence_score': intelligence_score,
                            'priority': priority,
                            'timestamp': datetime.now(),
                            'type': 'news_intelligence',
                            'clickable': True
                        })
                        
                except Exception as e:
                    continue
        
        return sorted(news_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    def _analyze_human_emotions(self, text):
        """Analyze human emotions using keyword detection"""
        emotion_keywords = {
            'fear': ['afraid', 'scared', 'terror', 'panic', 'worry', 'anxiety', 'threat'],
            'anger': ['angry', 'rage', 'fury', 'outrage', 'mad', 'furious', 'hate'],
            'hope': ['hope', 'optimistic', 'positive', 'better', 'improve', 'progress'],
            'trust': ['trust', 'believe', 'confidence', 'faith', 'reliable', 'honest'],
            'resentment': ['resentment', 'bitter', 'grudge', 'unfair', 'injustice', 'betrayal']
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotions[emotion] = min(10, score * 2)  # Scale to 1-10
        
        return emotions

    def _analyze_human_impact(self, text):
        """Analyze potential human impact"""
        impact_indicators = {
            'displacement': ['refugee', 'evacuate', 'flee', 'migration', 'displacement'],
            'economic_hardship': ['poverty', 'unemployment', 'inflation', 'crisis', 'shortage'],
            'social_unrest': ['protest', 'riot', 'demonstration', 'uprising', 'strike'],
            'health_safety': ['health', 'safety', 'emergency', 'disaster', 'epidemic']
        }
        
        text_lower = text.lower()
        impact_scores = {}
        
        for category, keywords in impact_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            impact_scores[category] = min(10, score * 2.5)  # Scale to 1-10
        
        return impact_scores

    def _get_sentiment_label(self, polarity):
        """Convert sentiment polarity to label"""
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

    def _calculate_reddit_credibility(self, post, subreddit_name):
        """Calculate Reddit post credibility (1-10 scale)"""
        base_credibility = {
            'worldnews': 8, 'geopolitics': 9, 'UkraineConflict': 7,
            'syriancivilwar': 7, 'china': 6, 'russia': 6,
            'investing': 7, 'security': 8
        }.get(subreddit_name, 5)
        
        # Adjust based on engagement
        if post.upvote_ratio > 0.9 and post.score > 1000:
            base_credibility += 1
        elif post.upvote_ratio < 0.6:
            base_credibility -= 1
        
        return min(10, max(1, base_credibility))

    def _calculate_impact_score(self, post, sentiment, emotional_analysis):
        """Calculate impact score (1-10 scale)"""
        base_score = 5
        
        # Engagement factor
        engagement_factor = min(3, (post.score + post.num_comments) / 1000)
        
        # Emotional intensity
        max_emotion = max(emotional_analysis.values()) if emotional_analysis else 0
        emotion_factor = min(2, max_emotion / 5)
        
        # Sentiment extremity
        sentiment_factor = min(1, abs(sentiment.polarity) * 2)
        
        total_score = base_score + engagement_factor + emotion_factor + sentiment_factor
        return min(10, max(1, total_score))

    def _calculate_human_interest(self, text, emotional_analysis):
        """Calculate human interest score (1-10 scale)"""
        human_keywords = ['people', 'family', 'children', 'community', 'citizens', 'victims', 'survivors']
        
        keyword_count = sum(1 for keyword in human_keywords if keyword in text.lower())
        emotion_intensity = sum(emotional_analysis.values()) / len(emotional_analysis) if emotional_analysis else 0
        
        score = 3 + (keyword_count * 1.5) + (emotion_intensity / 2)
        return min(10, max(1, score))

    def _calculate_news_credibility(self, source_name):
        """Calculate news source credibility (1-10 scale)"""
        credibility_scores = {
            'Reuters': 10, 'AP': 10, 'BBC': 9.5, 'Financial Times': 9,
            'Al Jazeera': 8.5, 'Defense News': 8, 'Military Times': 7.5,
            'Breaking Defense': 7, 'War on the Rocks': 8.5, 'Crisis Group': 9,
            'Bloomberg': 9, 'MarketWatch': 7.5, 'Economic Times': 7,
            'LiveUAMap': 7
        }
        
        for source, score in credibility_scores.items():
            if source.lower() in source_name.lower():
               return score
       
       return 6.0  # Default credibility

   def _calculate_relevance_score(self, content):
       """Calculate relevance score (1-10 scale)"""
       relevance_keywords = {
           'high': ['war', 'conflict', 'crisis', 'emergency', 'breaking', 'urgent', 'critical'],
           'medium': ['government', 'policy', 'economy', 'military', 'security', 'international'],
           'low': ['meeting', 'statement', 'announcement', 'report', 'study']
       }
       
       content_lower = content.lower()
       score = 5  # Base score
       
       for keyword in relevance_keywords['high']:
           if keyword in content_lower:
               score += 1.5
       
       for keyword in relevance_keywords['medium']:
           if keyword in content_lower:
               score += 0.8
       
       for keyword in relevance_keywords['low']:
           if keyword in content_lower:
               score += 0.3
       
       return min(10, max(1, score))

   def _calculate_urgency_score(self, title, content):
       """Calculate urgency score (1-10 scale)"""
       urgency_indicators = ['breaking', 'urgent', 'immediate', 'emergency', 'alert', 'now', 'just in']
       
       text = f"{title} {content}".lower()
       urgency_count = sum(1 for indicator in urgency_indicators if indicator in text)
       
       base_score = 3
       urgency_factor = min(4, urgency_count * 2)
       
       # Time sensitivity
       time_words = ['today', 'tonight', 'this hour', 'moments ago']
       time_factor = min(2, sum(1 for word in time_words if word in text))
       
       total_score = base_score + urgency_factor + time_factor
       return min(10, max(1, total_score))

# ============================================================================
# SOPHISTICATED ANALYTICS ENGINE
# ============================================================================

class WhiteLuxuryAnalyticsEngine:
   def __init__(self):
       pass
   
   def generate_executive_assessment(self, reddit_data, news_data):
       """Generate sophisticated executive assessment"""
       
       # Human Pulse Analysis
       human_pulse = self._analyze_human_pulse(reddit_data, news_data)
       
       # Regional Risk Assessment
       regional_risks = self._assess_regional_risks(reddit_data + news_data)
       
       # Sentiment & Emotional Intelligence
       emotional_intelligence = self._analyze_emotional_landscape(reddit_data + news_data)
       
       # Executive Summary Metrics
       executive_metrics = self._calculate_executive_metrics(reddit_data, news_data, regional_risks)
       
       return {
           'human_pulse': human_pulse,
           'regional_risks': regional_risks,
           'emotional_intelligence': emotional_intelligence,
           'executive_metrics': executive_metrics,
           'timestamp': datetime.now()
       }
   
   def _analyze_human_pulse(self, reddit_data, news_data):
       """Analyze human pulse across all data"""
       all_data = reddit_data + news_data
       
       if not all_data:
           return {}
       
       # Aggregate emotional scores
       emotion_totals = {'fear': 0, 'anger': 0, 'hope': 0, 'trust': 0, 'resentment': 0}
       emotion_counts = {'fear': 0, 'anger': 0, 'hope': 0, 'trust': 0, 'resentment': 0}
       
       for item in all_data:
           if 'emotional_analysis' in item:
               for emotion, score in item['emotional_analysis'].items():
                   if score > 0:
                       emotion_totals[emotion] += score
                       emotion_counts[emotion] += 1
       
       # Calculate averages (1-10 scale)
       emotion_averages = {}
       for emotion in emotion_totals:
           if emotion_counts[emotion] > 0:
               emotion_averages[emotion] = emotion_totals[emotion] / emotion_counts[emotion]
           else:
               emotion_averages[emotion] = 0
       
       # Overall human sentiment
       sentiment_scores = [item.get('sentiment_polarity', 0) for item in all_data]
       avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
       
       # Psychological pressure index (1-10)
       pressure_factors = [emotion_averages.get('fear', 0), emotion_averages.get('anger', 0), 
                         emotion_averages.get('resentment', 0)]
       psychological_pressure = np.mean(pressure_factors) if pressure_factors else 0
       
       # Social cohesion index (1-10)
       cohesion_factors = [emotion_averages.get('trust', 0), emotion_averages.get('hope', 0)]
       social_cohesion = np.mean(cohesion_factors) if cohesion_factors else 0
       
       return {
           'emotions': emotion_averages,
           'overall_sentiment': avg_sentiment,
           'psychological_pressure': psychological_pressure,
           'social_cohesion': social_cohesion,
           'total_samples': len(all_data)
       }
   
   def _assess_regional_risks(self, all_data):
       """Assess risks by region with sophisticated scoring"""
       regional_data = {}
       
       for item in all_data:
           region = item.get('region', 'Global')
           if region not in regional_data:
               regional_data[region] = {
                   'risk_score': 0, 'items': [], 'intelligence_scores': [],
                   'sentiment_scores': [], 'emotional_intensity': []
               }
           
           regional_data[region]['items'].append(item)
           regional_data[region]['intelligence_scores'].append(item.get('intelligence_score', 0))
           regional_data[region]['sentiment_scores'].append(item.get('sentiment_polarity', 0))
           
           # Calculate emotional intensity
           if 'emotional_analysis' in item:
               intensity = sum(item['emotional_analysis'].values())
               regional_data[region]['emotional_intensity'].append(intensity)
       
       # Calculate sophisticated risk scores (1-10 scale)
       for region, data in regional_data.items():
           if data['items']:
               # Base risk from intelligence scores
               avg_intelligence = np.mean(data['intelligence_scores'])
               
               # Emotional volatility factor
               sentiment_volatility = np.std(data['sentiment_scores']) if len(data['sentiment_scores']) > 1 else 0
               
               # Emotional intensity factor
               avg_emotional_intensity = np.mean(data['emotional_intensity']) if data['emotional_intensity'] else 0
               
               # Critical items factor
               critical_count = len([item for item in data['items'] if item.get('priority') == 'CRITICAL'])
               critical_factor = min(3, critical_count * 0.5)
               
               # Calculate composite risk score (1-10)
               risk_score = (avg_intelligence * 0.4 + 
                           sentiment_volatility * 20 * 0.2 + 
                           avg_emotional_intensity * 0.2 + 
                           critical_factor * 0.2)
               
               data['risk_score'] = min(10, max(1, risk_score))
               data['total_items'] = len(data['items'])
               data['critical_items'] = critical_count
               data['avg_sentiment'] = np.mean(data['sentiment_scores'])
       
       return regional_data
   
   def _analyze_emotional_landscape(self, all_data):
       """Analyze the overall emotional landscape"""
       sentiment_distribution = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
       
       for item in all_data:
           sentiment_label = item.get('sentiment_label', 'Neutral')
           sentiment_distribution[sentiment_label] += 1
       
       # Calculate percentages
       total = sum(sentiment_distribution.values())
       if total > 0:
           for sentiment in sentiment_distribution:
               sentiment_distribution[sentiment] = (sentiment_distribution[sentiment] / total) * 100
       
       # Emotional volatility index (1-10)
       sentiment_scores = [item.get('sentiment_polarity', 0) for item in all_data]
       volatility = np.std(sentiment_scores) * 10 if sentiment_scores else 0
       
       # Dominant emotions
       all_emotions = {'fear': [], 'anger': [], 'hope': [], 'trust': [], 'resentment': []}
       for item in all_data:
           if 'emotional_analysis' in item:
               for emotion, score in item['emotional_analysis'].items():
                   all_emotions[emotion].append(score)
       
       dominant_emotions = {}
       for emotion, scores in all_emotions.items():
           if scores:
               dominant_emotions[emotion] = np.mean(scores)
           else:
               dominant_emotions[emotion] = 0
       
       return {
           'sentiment_distribution': sentiment_distribution,
           'emotional_volatility': min(10, volatility),
           'dominant_emotions': dominant_emotions
       }
   
   def _calculate_executive_metrics(self, reddit_data, news_data, regional_risks):
       """Calculate executive-level metrics"""
       total_sources = len(reddit_data) + len(news_data)
       
       # Critical items
       all_data = reddit_data + news_data
       critical_items = len([item for item in all_data if item.get('priority') == 'CRITICAL'])
       
       # Global risk score (1-10)
       risk_scores = [data['risk_score'] for data in regional_risks.values()]
       global_risk = np.mean(risk_scores) if risk_scores else 5.0
       
       # Intelligence quality score (1-10)
       intelligence_scores = [item.get('intelligence_score', 0) for item in all_data]
       avg_intelligence_quality = np.mean(intelligence_scores) if intelligence_scores else 5.0
       
       # Data confidence (1-10)
       confidence_factors = [
           min(10, total_sources / 50),  # Source diversity
           min(10, len(regional_risks) * 2),  # Geographic coverage
           avg_intelligence_quality / 10 * 10  # Quality factor
       ]
       data_confidence = np.mean(confidence_factors)
       
       return {
           'global_risk_score': global_risk,
           'intelligence_quality': avg_intelligence_quality,
           'data_confidence': data_confidence,
           'total_sources': total_sources,
           'critical_items': critical_items
       }

# ============================================================================
# WHITE LUXURY DASHBOARD
# ============================================================================

def create_elegant_charts(data, chart_type="sentiment"):
   """Create elegant white-themed charts"""
   if chart_type == "sentiment" and data:
       sentiment_dist = data.get('sentiment_distribution', {})
       
       fig = go.Figure(data=[
           go.Pie(
               labels=list(sentiment_dist.keys()),
               values=list(sentiment_dist.values()),
               hole=.4,
               marker_colors=['#2E8B57', '#B22222', '#CCCCCC'],
               textfont_size=12
           )
       ])
       
       fig.update_layout(
           plot_bgcolor='rgba(0,0,0,0)',
           paper_bgcolor='rgba(0,0,0,0)',
           font_color='#222222',
           title={
               'text': 'Global Sentiment Distribution',
               'x': 0.5,
               'font': {'size': 16, 'color': '#003366'}
           },
           showlegend=True,
           height=300
       )
       
       return fig
   
   return None

def create_emotion_radar(emotions):
   """Create emotional radar chart"""
   if not emotions:
       return None
   
   categories = list(emotions.keys())
   values = list(emotions.values())
   
   fig = go.Figure()
   
   fig.add_trace(go.Scatterpolar(
       r=values,
       theta=categories,
       fill='toself',
       fillcolor='rgba(0, 51, 102, 0.1)',
       line_color='#003366',
       line_width=2,
       marker_size=8,
       marker_color='#003366'
   ))
   
   fig.update_layout(
       polar=dict(
           bgcolor='rgba(0,0,0,0)',
           radialaxis=dict(
               visible=True,
               range=[0, 10],
               tickfont_size=10,
               tickfont_color='#222222'
           ),
           angularaxis=dict(
               tickfont_size=11,
               tickfont_color='#222222'
           )
       ),
       plot_bgcolor='rgba(0,0,0,0)',
       paper_bgcolor='rgba(0,0,0,0)',
       title={
           'text': 'Human Emotional Pulse',
           'x': 0.5,
           'font': {'size': 16, 'color': '#003366'}
       },
       height=350
   )
   
   return fig

def main():
   # LUXURY WHITE HEADER
   st.markdown("""
   <div class="luxury-header">
       <div class="classification-badge">SENSITIVE</div>
       <h1 class="luxury-title">Global Strategic Intelligence Hub</h1>
       <p class="luxury-subtitle">Human-Centric Intelligence • Geopolitical Analysis • Executive Insights</p>
       <div class="live-indicator">
           <div class="pulse-dot"></div>
           LIVE INTELLIGENCE
       </div>
   </div>
   """, unsafe_allow_html=True)
   
   # SOPHISTICATED SIDEBAR
   st.sidebar.markdown("## Strategic Controls")
   st.sidebar.markdown("---")
   
   # Elegant filters
   st.sidebar.markdown("### 🌍 Geographic Intelligence")
   regions = ['Global', 'North America', 'Europe', 'Asia Pacific', 'Middle East', 'Africa', 'Eastern Europe', 'South Asia']
   selected_regions = st.sidebar.multiselect("Monitor Regions:", regions, default=['Global', 'Middle East', 'Asia Pacific'])
   
   st.sidebar.markdown("### 📊 Intelligence Priorities")
   priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
   selected_priorities = st.sidebar.multiselect("Priority Levels:", priorities, default=priorities)
   
   st.sidebar.markdown("### 🧠 Human Factors")
   human_factors = ['Public Opinion', 'Conflict Psychology', 'Market Psychology', 'Security Concerns']
   selected_factors = st.sidebar.multiselect("Human Intelligence:", human_factors, default=human_factors)
   
   st.sidebar.markdown("### ⚙️ System Controls")
   auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=True)
   show_emotions = st.sidebar.checkbox("Show emotional analysis", value=True)
   
   if st.sidebar.button("🔄 Refresh Intelligence", use_container_width=True):
       st.cache_data.clear()
       st.rerun()
   
   # Initialize systems
   collector = WhiteLuxuryIntelligenceCollector()
   analyzer = WhiteLuxuryAnalyticsEngine()
   
   # SOPHISTICATED DATA COLLECTION
   with st.container():
       st.markdown("### 📡 Intelligence Collection Status")
       
       col1, col2 = st.columns(2)
       
       with col1:
           with st.spinner("Collecting human intelligence..."):
               reddit_data = collector.collect_human_intelligence()
           
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-value">{len(reddit_data)}</div>
               <div class="metric-label">Human Intelligence Sources</div>
               <div class="metric-delta status-operational">ACTIVE</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           with st.spinner("Collecting news intelligence..."):
               news_data = collector.collect_news_intelligence()
           
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-value">{len(news_data)}</div>
               <div class="metric-label">News Intelligence Sources</div>
               <div class="metric-delta status-operational">OPERATIONAL</div>
           </div>
           """, unsafe_allow_html=True)
   
   # EXECUTIVE ASSESSMENT
   assessment = analyzer.generate_executive_assessment(reddit_data, news_data)
   
   # EXECUTIVE DASHBOARD
   st.markdown("### ⚪ Executive Intelligence Dashboard")
   
   # Top-level metrics
   col1, col2, col3, col4, col5 = st.columns(5)
   
   with col1:
       risk_score = assessment['executive_metrics']['global_risk_score']
       risk_class = "score-critical" if risk_score >= 8 else "score-warning" if risk_score >= 6 else "score-good" if risk_score >= 4 else "score-excellent"
       
       if st.button(f"Risk: {risk_score:.1f}/10", key="risk_score", use_container_width=True):
           st.info(f"**Global Risk Assessment**\n\nCurrent Level: {risk_score:.1f}/10\nConfidence: {assessment['executive_metrics']['data_confidence']:.1f}/10\nBased on {assessment['executive_metrics']['total_sources']} intelligence sources")
   
   with col2:
       quality_score = assessment['executive_metrics']['intelligence_quality']
       quality_class = "score-excellent" if quality_score >= 8 else "score-good" if quality_score >= 6 else "score-warning"
       
       if st.button(f"Quality: {quality_score:.1f}/10", key="quality_score", use_container_width=True):
           st.info(f"**Intelligence Quality**\n\nAverage Score: {quality_score:.1f}/10\nTotal Sources: {assessment['executive_metrics']['total_sources']}\nCritical Items: {assessment['executive_metrics']['critical_items']}")
   
   with col3:
       confidence_score = assessment['executive_metrics']['data_confidence']
       confidence_class = "score-excellent" if confidence_score >= 8 else "score-good" if confidence_score >= 6 else "score-warning"
       
       if st.button(f"Confidence: {confidence_score:.1f}/10", key="confidence_score", use_container_width=True):
           st.info(f"**Data Confidence**\n\nConfidence Level: {confidence_score:.1f}/10\nGeographic Coverage: {len(assessment['regional_risks'])} regions\nSource Diversity: High")
   
   with col4:
       pressure_score = assessment['human_pulse'].get('psychological_pressure', 0)
       pressure_class = "score-critical" if pressure_score >= 7 else "score-warning" if pressure_score >= 5 else "score-good"
       
       if st.button(f"Pressure: {pressure_score:.1f}/10", key="pressure_score", use_container_width=True):
           emotions = assessment['human_pulse'].get('emotions', {})
           st.info(f"**Psychological Pressure**\n\nLevel: {pressure_score:.1f}/10\nFear: {emotions.get('fear', 0):.1f}\nAnger: {emotions.get('anger', 0):.1f}\nResentment: {emotions.get('resentment', 0):.1f}")
   
   with col5:
       cohesion_score = assessment['human_pulse'].get('social_cohesion', 0)
       cohesion_class = "score-excellent" if cohesion_score >= 7 else "score-good" if cohesion_score >= 5 else "score-warning"
       
       if st.button(f"Cohesion: {cohesion_score:.1f}/10", key="cohesion_score", use_container_width=True):
           emotions = assessment['human_pulse'].get('emotions', {})
           st.info(f"**Social Cohesion**\n\nLevel: {cohesion_score:.1f}/10\nTrust: {emotions.get('trust', 0):.1f}\nHope: {emotions.get('hope', 0):.1f}\nOverall Sentiment: {assessment['human_pulse'].get('overall_sentiment', 0):.3f}")
   
   # MAIN INTELLIGENCE INTERFACE
   tab1, tab2, tab3, tab4, tab5 = st.tabs([
       "🎯 Strategic Overview",
       "🧠 Human Pulse",
       "📊 Intelligence Feed",
       "🌍 Regional Analysis",
       "📋 Executive Reports"
   ])
   
   with tab1:
       st.markdown("## 🎯 Strategic Intelligence Overview")
       
       col1, col2, col3 = st.columns([1, 1, 1])
       
       with col1:
           st.markdown("### 📊 Global Risk Dial")
           
           # Risk gauge
           risk_score = assessment['executive_metrics']['global_risk_score']
           
           fig = go.Figure(go.Indicator(
               mode = "gauge+number",
               value = risk_score,
               domain = {'x': [0, 1], 'y': [0, 1]},
               title = {'text': "Global Risk Level", 'font': {'size': 14, 'color': '#003366'}},
               gauge = {
                   'axis': {'range': [None, 10], 'tickcolor': '#222222'},
                   'bar': {'color': "#003366"},
                   'steps': [
                       {'range': [0, 3], 'color': "#2E8B57"},
                       {'range': [3, 6], 'color': "#C9A227"},
                       {'range': [6, 8], 'color': "#FF8C00"},
                       {'range': [8, 10], 'color': "#B22222"}
                   ],
                   'threshold': {
                       'line': {'color': "#B22222", 'width': 3},
                       'thickness': 0.75,
                       'value': 8
                   }
               }
           ))
           
           fig.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               paper_bgcolor='rgba(0,0,0,0)',
               font_color='#222222',
               height=300
           )
           
           st.plotly_chart(fig, use_container_width=True)
       
       with col2:
           st.markdown("### 🧠 Human Emotional Pulse")
           
           emotions = assessment['human_pulse'].get('emotions', {})
           emotion_fig = create_emotion_radar(emotions)
           
           if emotion_fig:
               st.plotly_chart(emotion_fig, use_container_width=True)
       
       with col3:
           st.markdown("### 📈 Sentiment Distribution")
           
           sentiment_fig = create_elegant_charts(assessment['emotional_intelligence'], "sentiment")
           
           if sentiment_fig:
               st.plotly_chart(sentiment_fig, use_container_width=True)
       
       # Top Critical Events
       st.markdown("### 🚨 Top 5 Critical Events Today")
       
       all_intelligence = reddit_data + news_data
       critical_events = [item for item in all_intelligence if item.get('priority') == 'CRITICAL'][:5]
       
       if not critical_events:
           critical_events = sorted(all_intelligence, key=lambda x: x.get('intelligence_score', 0), reverse=True)[:5]
       
       for i, event in enumerate(critical_events, 1):
           priority_class = f"priority-{event.get('priority', 'medium').lower()}"
           sentiment_class = f"sentiment-{event.get('sentiment_label', 'neutral').lower()}"
           
           st.markdown(f"""
           <div class="intelligence-item {priority_class}">
               <div style="margin-bottom: 0.8rem;">
                   <span class="tag-elegant tag-{event.get('priority', 'medium').lower()}">{event.get('priority', 'MEDIUM')}</span>
                   <span class="tag-elegant">Score: {event.get('intelligence_score', 0):.1f}/10</span>
                   <span class="tag-elegant">{event.get('category', 'Unknown')}</span>
                   <span class="sentiment-indicator sentiment-{event.get('sentiment_label', 'neutral').lower()}">
                       {event.get('sentiment_label', 'Neutral')}
                   </span>
               </div>
               
               <h4 style="margin-bottom: 0.5rem; color: #003366; font-weight: 600;">{event['title']}</h4>
               
               {f'<p style="margin-bottom: 0.5rem; color: #222222; line-height: 1.5;">{event.get("content_preview", event.get("summary", ""))[:250]}...</p>' if event.get('content_preview') or event.get('summary') else ''}
               
               <div style="margin-bottom: 0.8rem;">
                   <span style="color: #222222;"><strong>Source:</strong> {event['source']}</span>
                   <span style="color: #222222; margin-left: 1rem;"><strong>Region:</strong> {event.get('region', 'Global')}</span>
                   <span style="color: #222222; margin-left: 1rem;"><strong>Time:</strong> {event['timestamp'].strftime('%H:%M')}</span>
               </div>
               
               {f'<div style="margin-bottom: 0.5rem;"><strong>Human Impact:</strong> {", ".join([f"{k.replace("_", " ").title()}: {v:.1f}/10" for k, v in event.get("human_impact", {}).items() if v > 0])}</div>' if event.get('human_impact') else ''}
               
               <div style="margin-top: 1rem;">
                   <a href="{event['url']}" target="_blank" style="color: #003366; text-decoration: none; font-weight: 600; border: 1px solid #003366; padding: 0.4rem 1rem; border-radius: 6px; transition: all 0.3s ease;">
                       📖 VIEW FULL SOURCE
                   </a>
               </div>
           </div>
           """, unsafe_allow_html=True)
   
   with tab2:
       st.markdown("## 🧠 Human Pulse & Sentiment Intelligence")
       
       # Human emotional analysis
       col1, col2 = st.columns(2)
       
       with col1:
           st.markdown("### 😊 Emotional State Analysis")
           
           emotions = assessment['human_pulse'].get('emotions', {})
           
           st.markdown("""
           <div class="human-pulse-card">
               <div class="section-header">Human Emotional Indicators (1-10 Scale)</div>
           """, unsafe_allow_html=True)
           
           for emotion, score in emotions.items():
               emotion_class = "score-critical" if score >= 7 else "score-warning" if score >= 5 else "score-good" if score >= 3 else "score-excellent"
               
               st.markdown(f"""
               <div class="emotion-meter">
                   <span class="emotion-label">{emotion.title()}</span>
                   <span class="emotion-score {emotion_class}">{score:.1f}/10</span>
               </div>
               """, unsafe_allow_html=True)
           
           st.markdown("</div>", unsafe_allow_html=True)
       
       with col2:
           st.markdown("### 📊 Psychological Indicators")
           
           pressure = assessment['human_pulse'].get('psychological_pressure', 0)
           cohesion = assessment['human_pulse'].get('social_cohesion', 0)
           sentiment = assessment['human_pulse'].get('overall_sentiment', 0)
           
           st.markdown(f"""
           <div class="human-pulse-card">
               <div class="section-header">Psychological Assessment</div>
               
               <div class="emotion-meter">
                   <span class="emotion-label">Psychological Pressure</span>
                   <span class="emotion-score {'score-critical' if pressure >= 7 else 'score-warning' if pressure >= 5 else 'score-good'}">{pressure:.1f}/10</span>
               </div>
               
               <div class="emotion-meter">
                   <span class="emotion-label">Social Cohesion</span>
                   <span class="emotion-score {'score-excellent' if cohesion >= 7 else 'score-good' if cohesion >= 5 else 'score-warning'}">{cohesion:.1f}/10</span>
               </div>
               
               <div class="emotion-meter">
                   <span class="emotion-label">Overall Sentiment</span>
                   <span class="emotion-score {'sentiment-positive' if sentiment > 0.1 else 'sentiment-negative' if sentiment < -0.1 else 'sentiment-neutral'}">{sentiment:.3f}</span>
               </div>
               
               <div class="emotion-meter">
                   <span class="emotion-label">Sample Size</span>
                   <span class="emotion-score">{assessment['human_pulse'].get('total_samples', 0)}</span>
               </div>
           </div>
           """, unsafe_allow_html=True)
       
       # Detailed sentiment analysis by source
       st.markdown("### 📱 Human Intelligence by Source")
       
       human_factors = {}
       for item in reddit_data:
           factor = item.get('human_factor', 'Unknown')
           if factor not in human_factors:
               human_factors[factor] = []
           human_factors[factor].append(item)
       
       for factor, items in human_factors.items():
           if items and factor in selected_factors:
               avg_score = np.mean([item.get('intelligence_score', 0) for item in items])
               avg_sentiment = np.mean([item.get('sentiment_polarity', 0) for item in items])
               
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-header">{factor.upper()} ({len(items)} sources, avg score: {avg_score:.1f}/10)</div>
               """, unsafe_allow_html=True)
               
               for item in items[:5]:  # Show top 5 per factor
                   sentiment_class = f"sentiment-{item.get('sentiment_label', 'neutral').lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-item">
                       <div style="margin-bottom: 0.8rem;">
                           <span class="tag-elegant">Score: {item.get('intelligence_score', 0):.1f}/10</span>
                           <span class="tag-elegant">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                           <span class="sentiment-indicator {sentiment_class}">
                               {item.get('sentiment_label', 'Neutral')}
                           </span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #003366;">{item['title']}</h4>
                       
                       <div style="margin-bottom: 0.5rem;">
                           <span style="color: #222222;"><strong>Engagement:
           <span style="color: #222222;"><strong>Engagement:</strong> {item.get('score', 0)} ↑ {item.get('comments', 0)} 💬</span>
                           <span style="color: #222222; margin-left: 1rem;"><strong>Impact Score:</strong> {item.get('impact_score', 0):.1f}/10</span>
                           <span style="color: #222222; margin-left: 1rem;"><strong>Human Interest:</strong> {item.get('human_interest_score', 0):.1f}/10</span>
                       </div>
                       
                       {f'<div style="margin-bottom: 0.5rem;"><strong>Emotional Profile:</strong> {", ".join([f"{k.title()}: {v:.1f}" for k, v in item.get("emotional_analysis", {}).items() if v > 0])}</div>' if item.get('emotional_analysis') else ''}
                       
                       <div style="margin-top: 1rem;">
                           <a href="{item['url']}" target="_blank" style="color: #003366; text-decoration: none; font-weight: 600;">
                               🔗 Read Full Discussion
                           </a>
                           <span style="color: #222222; margin-left: 1rem;">Author: {item.get('author', 'Unknown')}</span>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
   
   with tab3:
       st.markdown("## 📊 Comprehensive Intelligence Feed")
       
       # Advanced filtering
       col1, col2, col3 = st.columns(3)
       
       with col1:
           min_score = st.slider("Minimum Intelligence Score", 0.0, 10.0, 5.0, 0.1)
       
       with col2:
           source_type = st.selectbox("Source Type", ["All Sources", "Human Intelligence", "News Intelligence"])
       
       with col3:
           sentiment_filter = st.selectbox("Sentiment Filter", ["All Sentiments", "Positive", "Negative", "Neutral"])
       
       # Filter and combine intelligence
       all_intelligence = []
       
       # Add Reddit data
       if source_type in ["All Sources", "Human Intelligence"]:
           for item in reddit_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities and
                   item.get('region') in selected_regions and
                   (sentiment_filter == "All Sentiments" or item.get('sentiment_label') == sentiment_filter)):
                   all_intelligence.append(item)
       
       # Add news data
       if source_type in ["All Sources", "News Intelligence"]:
           for item in news_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities and
                   (sentiment_filter == "All Sentiments" or item.get('sentiment_label') == sentiment_filter)):
                   all_intelligence.append(item)
       
       # Sort by intelligence score
       all_intelligence.sort(key=lambda x: x.get('intelligence_score', 0), reverse=True)
       
       st.markdown(f"### 📡 Intelligence Feed ({len(all_intelligence)} items)")
       
       # Group by category
       categories = {}
       for item in all_intelligence[:100]:  # Show top 100
           category = item.get('category', 'Unknown')
           if category not in categories:
               categories[category] = []
           categories[category].append(item)
       
       for category, items in categories.items():
           if items:
               avg_score = np.mean([item.get('intelligence_score', 0) for item in items])
               avg_credibility = np.mean([item.get('credibility_score', 0) for item in items])
               
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-header">{category.upper()} INTELLIGENCE</div>
                   <p style="color: #222222; margin-bottom: 1rem;">
                       <strong>{len(items)} sources</strong> | 
                       <strong>Avg Score: {avg_score:.1f}/10</strong> | 
                       <strong>Avg Credibility: {avg_credibility:.1f}/10</strong>
                   </p>
               """, unsafe_allow_html=True)
               
               for item in items[:10]:  # Show top 10 per category
                   priority_class = f"priority-{item.get('priority', 'medium').lower()}"
                   sentiment_class = f"sentiment-{item.get('sentiment_label', 'neutral').lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <div style="margin-bottom: 0.8rem;">
                           <span class="tag-elegant tag-{item.get('priority', 'medium').lower()}">{item.get('priority', 'MEDIUM')}</span>
                           <span class="tag-elegant">Intelligence: {item.get('intelligence_score', 0):.1f}/10</span>
                           <span class="tag-elegant">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                           {f'<span class="tag-elegant">Relevance: {item.get("relevance_score", 0):.1f}/10</span>' if 'relevance_score' in item else ''}
                           {f'<span class="tag-elegant">Urgency: {item.get("urgency_score", 0):.1f}/10</span>' if 'urgency_score' in item else ''}
                           <span class="sentiment-indicator {sentiment_class}">
                               {item.get('sentiment_label', 'Neutral')} ({item.get('sentiment_polarity', 0):.2f})
                           </span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #003366; font-weight: 600;">{item['title']}</h4>
                       
                       {f'<p style="margin-bottom: 0.8rem; color: #222222; line-height: 1.5;">{item.get("content_preview", item.get("summary", ""))[:300]}...</p>' if item.get('content_preview') or item.get('summary') else ''}
                       
                       <div style="margin-bottom: 0.8rem;">
                           <span style="color: #222222;"><strong>Source:</strong> {item['source']}</span>
                           <span style="color: #222222; margin-left: 1rem;"><strong>Region:</strong> {item.get('region', 'Global')}</span>
                           <span style="color: #222222; margin-left: 1rem;"><strong>Time:</strong> {item['timestamp'].strftime('%H:%M')}</span>
                           {f'<span style="color: #222222; margin-left: 1rem;"><strong>Type:</strong> {item.get("human_factor", item.get("type", "")).replace("_", " ").title()}</span>' if item.get('human_factor') or item.get('type') else ''}
                       </div>
                       
                       {f'<div style="margin-bottom: 0.5rem;"><strong>Emotional Analysis:</strong> {", ".join([f"{k.title()}: {v:.1f}/10" for k, v in item.get("emotional_analysis", {}).items() if v > 0])}</div>' if item.get('emotional_analysis') else ''}
                       
                       {f'<div style="margin-bottom: 0.5rem;"><strong>Human Impact:</strong> {", ".join([f"{k.replace("_", " ").title()}: {v:.1f}/10" for k, v in item.get("human_impact", {}).items() if v > 0])}</div>' if item.get('human_impact') else ''}
                       
                       <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                           <a href="{item['url']}" target="_blank" style="color: #003366; text-decoration: none; font-weight: 600; border: 1px solid #003366; padding: 0.4rem 1rem; border-radius: 6px;">
                               📖 VIEW SOURCE
                           </a>
                           {f'<span style="color: #222222;">Author: {item.get("author", "Unknown")}</span>' if item.get('author') and item['author'] != 'Unknown' else ''}
                           {f'<span style="color: #222222;">Engagement: {item.get("score", 0)} ↑ {item.get("comments", 0)} 💬</span>' if item.get('score') else ''}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
   
   with tab4:
       st.markdown("## 🌍 Regional Risk Analysis")
       
       regional_risks = assessment['regional_risks']
       
       # Regional risk overview
       if regional_risks:
           risk_data = []
           for region, data in regional_risks.items():
               risk_data.append({
                   'Region': region,
                   'Risk Score': data['risk_score'],
                   'Total Items': data['total_items'],
                   'Critical Items': data['critical_items'],
                   'Avg Sentiment': data['avg_sentiment']
               })
           
           risk_df = pd.DataFrame(risk_data)
           
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("### 📊 Regional Risk Scores")
               
               # Risk score bar chart
               fig = px.bar(
                   risk_df, 
                   x='Risk Score', 
                   y='Region', 
                   orientation='h',
                   color='Risk Score',
                   color_continuous_scale=['#2E8B57', '#C9A227', '#FF8C00', '#B22222'],
                   title="Risk Assessment by Region (1-10 Scale)"
               )
               
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='#222222',
                   title_font_color='#003366',
                   height=400
               )
               
               st.plotly_chart(fig, use_container_width=True)
           
           with col2:
               st.markdown("### 📈 Intelligence Volume vs Risk")
               
               # Scatter plot
               fig = px.scatter(
                   risk_df,
                   x='Total Items',
                   y='Risk Score',
                   size='Critical Items',
                   color='Avg Sentiment',
                   hover_name='Region',
                   title="Intelligence Volume vs Risk Level",
                   color_continuous_scale='RdYlGn_r'
               )
               
               fig.update_layout(
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font_color='#222222',
                   title_font_color='#003366',
                   height=400
               )
               
               st.plotly_chart(fig, use_container_width=True)
       
       # Detailed regional analysis
       st.markdown("### 🌐 Detailed Regional Intelligence")
       
       for region, data in regional_risks.items():
           if region in selected_regions:
               risk_class = "score-critical" if data['risk_score'] >= 8 else "score-warning" if data['risk_score'] >= 6 else "score-good"
               
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-header">{region.upper()} INTELLIGENCE ASSESSMENT</div>
                   
                   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                       <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                           <div style="font-size: 1.5rem; font-weight: 700; color: #003366;">{data['risk_score']:.1f}/10</div>
                           <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Risk Score</div>
                       </div>
                       
                       <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                           <div style="font-size: 1.5rem; font-weight: 700; color: #003366;">{data['total_items']}</div>
                           <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Total Sources</div>
                       </div>
                       
                       <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                           <div style="font-size: 1.5rem; font-weight: 700; color: #B22222;">{data['critical_items']}</div>
                           <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Critical Items</div>
                       </div>
                       
                       <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                           <div style="font-size: 1.5rem; font-weight: 700; color: {'#2E8B57' if data['avg_sentiment'] > 0 else '#B22222' if data['avg_sentiment'] < 0 else '#222222'};">{data['avg_sentiment']:.2f}</div>
                           <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Avg Sentiment</div>
                       </div>
                   </div>
               </div>
               """, unsafe_allow_html=True)
   
   with tab5:
       st.markdown("## 📋 Executive Intelligence Reports")
       
       # Executive summary
       st.markdown("### 📊 Executive Summary")
       
       current_time = datetime.now()
       
       st.markdown(f"""
       <div class="intelligence-section">
           <div class="section-header">STRATEGIC INTELLIGENCE BRIEF</div>
           
           <p><strong>Classification:</strong> SENSITIVE</p>
           <p><strong>Generated:</strong> {current_time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
           <p><strong>Intelligence Cycle:</strong> {current_time.strftime('%Y-%m-%d')}</p>
           
           <h4 style="color: #003366; margin-top: 1.5rem;">KEY ASSESSMENTS:</h4>
           
           <div style="margin: 1rem 0;">
               <strong>Global Risk Level:</strong> 
               <span style="color: {'#B22222' if assessment['executive_metrics']['global_risk_score'] >= 8 else '#FF8C00' if assessment['executive_metrics']['global_risk_score'] >= 6 else '#2E8B57'};">
                   {assessment['executive_metrics']['global_risk_score']:.1f}/10
               </span>
           </div>
           
           <div style="margin: 1rem 0;">
               <strong>Intelligence Quality:</strong> {assessment['executive_metrics']['intelligence_quality']:.1f}/10
           </div>
           
           <div style="margin: 1rem 0;">
               <strong>Data Confidence:</strong> {assessment['executive_metrics']['data_confidence']:.1f}/10
           </div>
           
           <div style="margin: 1rem 0;">
               <strong>Psychological Pressure:</strong> {assessment['human_pulse'].get('psychological_pressure', 0):.1f}/10
           </div>
           
           <div style="margin: 1rem 0;">
               <strong>Social Cohesion:</strong> {assessment['human_pulse'].get('social_cohesion', 0):.1f}/10
           </div>
           
           <h4 style="color: #003366; margin-top: 1.5rem;">REGIONAL HOTSPOTS:</h4>
       </div>
       """, unsafe_allow_html=True)
       
       # Regional hotspots
       sorted_regions = sorted(assessment['regional_risks'].items(), 
                             key=lambda x: x[1]['risk_score'], reverse=True)
       
       for region, data in sorted_regions[:5]:
           if data['risk_score'] >= 6:  # Only show medium+ risk regions
               st.markdown(f"**{region}:** Risk {data['risk_score']:.1f}/10 | {data['critical_items']} critical items | Sentiment: {data['avg_sentiment']:.2f}")
       
       # Export capabilities
       st.markdown("### 📤 Intelligence Export Options")
       
       col1, col2, col3 = st.columns(3)
       
       with col1:
           if st.button("📊 Executive Summary", use_container_width=True):
               summary_data = {
                   'executive_summary': {
                       'timestamp': current_time.isoformat(),
                       'global_risk': assessment['executive_metrics']['global_risk_score'],
                       'intelligence_quality': assessment['executive_metrics']['intelligence_quality'],
                       'data_confidence': assessment['executive_metrics']['data_confidence'],
                       'psychological_pressure': assessment['human_pulse'].get('psychological_pressure', 0),
                       'social_cohesion': assessment['human_pulse'].get('social_cohesion', 0)
                   },
                   'regional_risks': assessment['regional_risks'],
                   'human_emotions': assessment['human_pulse'].get('emotions', {}),
                   'classification': 'SENSITIVE'
               }
               
               json_summary = json.dumps(summary_data, default=str, indent=2)
               st.download_button(
                   label="📥 Download Executive Summary",
                   data=json_summary,
                   file_name=f"executive_summary_{current_time.strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col2:
           if st.button("🧠 Human Intelligence", use_container_width=True):
               human_data = {
                   'human_pulse': assessment['human_pulse'],
                   'emotional_intelligence': assessment['emotional_intelligence'],
                   'human_intelligence_sources': reddit_data[:50],
                   'classification': 'SENSITIVE'
               }
               
               json_human = json.dumps(human_data, default=str, indent=2)
               st.download_button(
                   label="📥 Download Human Intelligence",
                   data=json_human,
                   file_name=f"human_intelligence_{current_time.strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       with col3:
           if st.button("📄 Full Intelligence", use_container_width=True):
               full_data = {
                   'assessment': assessment,
                   'human_intelligence': reddit_data,
                   'news_intelligence': news_data,
                   'generated_at': current_time.isoformat(),
                   'classification': 'SENSITIVE'
               }
               
               json_full = json.dumps(full_data, default=str, indent=2)
               st.download_button(
                   label="📥 Download Full Report",
                   data=json_full,
                   file_name=f"full_intelligence_{current_time.strftime('%Y%m%d_%H%M')}.json",
                   mime="application/json"
               )
       
       # Quick actions
       st.markdown("### ⚡ Quick Actions")
       
       col1, col2 = st.columns(2)
       
       with col1:
           if st.button("🔔 Set Risk Alerts", use_container_width=True):
               st.info("**Risk Alert Thresholds:**\n\n• Global Risk > 8.0/10\n• Regional Risk > 7.5/10\n• Critical Items > 10\n• Psychological Pressure > 8.0/10")
       
       with col2:
           if st.button("📈 Trend Analysis", use_container_width=True):
               trends_text = f"""
               **TREND ANALYSIS - {current_time.strftime('%Y-%m-%d')}**
               
               **Intelligence Trends:**
               • Total Sources: {assessment['executive_metrics']['total_sources']} (Quality: {assessment['executive_metrics']['intelligence_quality']:.1f}/10)
               • Critical Items: {assessment['executive_metrics']['critical_items']}
               • Geographic Coverage: {len(assessment['regional_risks'])} regions
               
               **Human Trends:**
               • Psychological Pressure: {assessment['human_pulse'].get('psychological_pressure', 0):.1f}/10
               • Social Cohesion: {assessment['human_pulse'].get('social_cohesion', 0):.1f}/10
               • Dominant Emotions: {', '.join([f"{k.title()}: {v:.1f}" for k, v in assessment['human_pulse'].get('emotions', {}).items() if v > 3])}
               """
               st.text_area("Intelligence Trends", trends_text, height=200)
   
   # AUTO-REFRESH MECHANISM
   if auto_refresh:
       # Display elegant countdown
       countdown_placeholder = st.empty()
       for remaining in range(300, 0, -1):  # 5 minutes
           mins, secs = divmod(remaining, 60)
           countdown_placeholder.markdown(f"""
           <div style="position: fixed; bottom: 20px; right: 20px; background: white; border: 1px solid #CCCCCC; border-radius: 8px; padding: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 1000;">
               <div style="color: #003366; font-weight: 600;">⏰ Next refresh: {mins:02d}:{secs:02d}</div>
           </div>
           """, unsafe_allow_html=True)
           time.sleep(1)
       
       st.cache_data.clear()
       st.rerun()

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
   main()
