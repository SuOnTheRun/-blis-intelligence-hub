# ============================================================================
# STRATEGIC INTELLIGENCE HUB v5.0
# Professional Intelligence Platform for Executive Decision Making
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import feedparser
import praw
import yfinance as yf
from datetime import datetime, timedelta
import time
import json
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PROFESSIONAL DESIGN SYSTEM
# ============================================================================

st.set_page_config(
    page_title="Strategic Intelligence Hub",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CLEAN PROFESSIONAL STYLING
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --primary-bg: #FFFFFF;
        --secondary-bg: #F8FAFC;
        --tertiary-bg: #F1F5F9;
        --border-color: #E2E8F0;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --accent-blue: #0F172A;
        --accent-green: #059669;
        --accent-red: #DC2626;
        --accent-amber: #D97706;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stApp {
        background: var(--primary-bg);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: var(--primary-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: var(--accent-blue);
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .metric-card {
        background: var(--primary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
        box-shadow: var(--shadow);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: var(--accent-blue);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .status-operational { color: var(--accent-green); }
    .status-warning { color: var(--accent-amber); }
    .status-critical { color: var(--accent-red); }
    
    .intelligence-section {
        background: var(--primary-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--accent-blue);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .intelligence-item {
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .intelligence-item:hover {
        background: var(--tertiary-bg);
        border-color: var(--accent-blue);
    }
    
    .priority-critical { border-left: 4px solid var(--accent-red); }
    .priority-high { border-left: 4px solid var(--accent-amber); }
    .priority-medium { border-left: 4px solid var(--accent-blue); }
    .priority-low { border-left: 4px solid var(--accent-green); }
    
    .tag {
        display: inline-block;
        background: var(--tertiary-bg);
        color: var(--text-primary);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.25rem;
    }
    
    .tag-critical { background-color: #FEE2E2; color: var(--accent-red); }
    .tag-high { background-color: #FEF3C7; color: var(--accent-amber); }
    .tag-medium { background-color: #DBEAFE; color: var(--accent-blue); }
    .tag-low { background-color: #D1FAE5; color: var(--accent-green); }
    
    .sentiment-positive { color: var(--accent-green); font-weight: 600; }
    .sentiment-negative { color: var(--accent-red); font-weight: 600; }
    .sentiment-neutral { color: var(--text-secondary); font-weight: 600; }
    
    .live-indicator {
        display: inline-block;
        background: var(--accent-red);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stSidebar"] {
        background: var(--secondary-bg);
        border-right: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--tertiary-bg);
        border-radius: 8px;
        padding: 0.25rem;
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0.75rem 1rem;
        margin: 0.125rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--secondary-bg);
        color: var(--text-primary);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--accent-blue);
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA COLLECTION ENGINE
# ============================================================================

class IntelligenceCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Strategic-Intelligence-Platform/5.0'
        })
        
        try:
            self.reddit = praw.Reddit(
                client_id="gPAQFk1IFWSkMEVMXFMMCQ",
                client_secret="2LoxxZ8c-Cr-Y0rrE9CmwvQQuHdskw",
                user_agent="StrategicWarRoom/1.0 by u/Quick_Shower_6934"
            )
        except Exception as e:
            self.reddit = None
            st.warning(f"Reddit API initialization failed: {e}")
        
        self.news_sources = {
            'Reuters World': 'https://feeds.reuters.com/reuters/worldNews',
            'AP International': 'https://feeds.apnews.com/rss/apf-topnews',
            'BBC Global': 'http://feeds.bbci.co.uk/news/world/rss.xml',
            'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
            'Economic Times': 'https://economictimes.indiatimes.com/news/rssfeeds/1715249553.cms'
        }
        
        self.subreddits = {
            'worldnews': {'region': 'Global', 'category': 'News Analysis'},
            'geopolitics': {'region': 'Global', 'category': 'Strategic Analysis'},
            'UkraineConflict': {'region': 'Eastern Europe', 'category': 'Conflict Intelligence'},
            'investing': {'region': 'Global', 'category': 'Economic Intelligence'}
        }

    @st.cache_data(ttl=300)
    def collect_reddit_intelligence(_self):
        """Collect intelligence from Reddit sources"""
        if not _self.reddit:
            return []
        
        intelligence = []
        
        for subreddit_name, config in _self.subreddits.items():
            try:
                subreddit = _self.reddit.subreddit(subreddit_name)
                posts = list(subreddit.hot(limit=10))
                
                for post in posts:
                    full_text = f"{post.title} {post.selftext[:500]}"
                    sentiment = TextBlob(full_text).sentiment
                    
                    # Calculate intelligence scores (1-10 scale)
                    credibility = _self._calculate_credibility(post, subreddit_name)
                    relevance = _self._calculate_relevance(full_text)
                    intelligence_score = (credibility + relevance) / 2
                    
                    # Assign priority
                    if intelligence_score >= 8.5:
                        priority = 'CRITICAL'
                    elif intelligence_score >= 7.0:
                        priority = 'HIGH'
                    elif intelligence_score >= 5.0:
                        priority = 'MEDIUM'
                    else:
                        priority = 'LOW'
                    
                    intelligence.append({
                        'source': f'Reddit r/{subreddit_name}',
                        'category': config['category'],
                        'title': post.title,
                        'content': post.selftext[:300] if post.selftext else 'External link - click to view',
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_label': _self._get_sentiment_label(sentiment.polarity),
                        'credibility_score': credibility,
                        'relevance_score': relevance,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': config['region'],
                        'timestamp': datetime.fromtimestamp(post.created_utc),
                        'type': 'social_intelligence'
                    })
                    
            except Exception as e:
                st.warning(f"Error collecting from r/{subreddit_name}: {e}")
                continue
        
        return sorted(intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_news_intelligence(_self):
        """Collect intelligence from news sources"""
        news_intelligence = []
        
        for source_name, url in _self.news_sources.items():
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:8]:
                    full_content = f"{entry.title} {entry.get('summary', '')}"
                    sentiment = TextBlob(full_content).sentiment
                    
                    # Calculate scores
                    credibility = _self._calculate_news_credibility(source_name)
                    relevance = _self._calculate_relevance(full_content)
                    intelligence_score = (credibility + relevance) / 2
                    
                    # Assign priority
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
                        'category': 'News Intelligence',
                        'title': entry.title,
                        'content': entry.get('summary', '')[:300],
                        'url': entry.link,
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_label': _self._get_sentiment_label(sentiment.polarity),
                        'credibility_score': credibility,
                        'relevance_score': relevance,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'timestamp': datetime.now(),
                        'type': 'news_intelligence'
                    })
                    
            except Exception as e:
                st.warning(f"Error collecting from {source_name}: {e}")
                continue
        
        return sorted(news_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_market_intelligence(_self):
        """Collect market intelligence"""
        tickers = {
            '^GSPC': 'S&P 500',
            '^NSEI': 'Nifty 50',
            '^VIX': 'VIX Fear Index',
            'LMT': 'Lockheed Martin',
            'RTX': 'Raytheon Technologies',
            'GLD': 'Gold ETF'
        }
        
        market_data = []
        
        for ticker, name in tickers.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    market_data.append({
                        'ticker': ticker,
                        'name': name,
                        'current_price': current_price,
                        'change_pct': change_pct,
                        'timestamp': datetime.now()
                    })
                    
            except Exception as e:
                continue
        
        return market_data

    def _calculate_credibility(self, post, subreddit_name):
        """Calculate credibility score (1-10)"""
        base_scores = {
            'worldnews': 8, 'geopolitics': 9, 'UkraineConflict': 7, 'investing': 7
        }
        base = base_scores.get(subreddit_name, 5)
        
        if post.upvote_ratio > 0.9 and post.score > 1000:
            base += 1
        elif post.upvote_ratio < 0.6:
            base -= 1
        
        return min(10, max(1, base))

    def _calculate_news_credibility(self, source_name):
        """Calculate news source credibility (1-10)"""
        scores = {
            'Reuters': 10, 'AP': 10, 'BBC': 9.5, 'Defense News': 8, 'Economic Times': 7
        }
        for source, score in scores.items():
            if source.lower() in source_name.lower():
                return score
        return 6.0

    def _calculate_relevance(self, content):
        """Calculate relevance score (1-10)"""
        keywords = ['war', 'conflict', 'crisis', 'military', 'security', 'intelligence', 'threat']
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        return min(10, max(1, 5 + matches))

    def _get_sentiment_label(self, polarity):
        """Convert sentiment polarity to label"""
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

# ============================================================================
# ANALYTICS ENGINE
# ============================================================================

class AnalyticsEngine:
    def generate_assessment(self, reddit_data, news_data, market_data):
        """Generate comprehensive assessment"""
        all_intelligence = reddit_data + news_data
        
        if not all_intelligence:
            return self._empty_assessment()
        
        # Calculate metrics
        total_sources = len(all_intelligence)
        critical_items = len([item for item in all_intelligence if item.get('priority') == 'CRITICAL'])
        high_items = len([item for item in all_intelligence if item.get('priority') == 'HIGH'])
        
        # Intelligence quality
        scores = [item.get('intelligence_score', 0) for item in all_intelligence]
        avg_intelligence = np.mean(scores) if scores else 5.0
        
        # Sentiment analysis
        sentiments = [item.get('sentiment_polarity', 0) for item in all_intelligence]
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        
        # Risk calculation
        risk_score = min(10, (critical_items * 2) + (high_items * 1) + (avg_intelligence / 2))
        
        # Regional analysis
        regions = self._analyze_regions(all_intelligence)
        
        # Market stress
        market_stress = self._calculate_market_stress(market_data)
        
        return {
            'global_risk_score': risk_score,
            'intelligence_quality': avg_intelligence,
            'total_sources': total_sources,
            'critical_items': critical_items,
            'high_items': high_items,
            'avg_sentiment': avg_sentiment,
            'regional_analysis': regions,
            'market_stress': market_stress,
            'timestamp': datetime.now()
        }
    
    def _analyze_regions(self, intelligence_data):
        """Analyze intelligence by region"""
        regions = {}
        for item in intelligence_data:
            region = item.get('region', 'Global')
            if region not in regions:
                regions[region] = {'items': 0, 'critical': 0, 'sentiment': []}
            
            regions[region]['items'] += 1
            if item.get('priority') == 'CRITICAL':
                regions[region]['critical'] += 1
            regions[region]['sentiment'].append(item.get('sentiment_polarity', 0))
        
        # Calculate regional metrics
        for region, data in regions.items():
            data['avg_sentiment'] = np.mean(data['sentiment']) if data['sentiment'] else 0
            data['risk_score'] = min(10, (data['critical'] * 3) + abs(data['avg_sentiment']) * 2)
        
        return regions
    
    def _calculate_market_stress(self, market_data):
        """Calculate market stress indicator"""
        if not market_data:
            return 0
        
        vix_data = [item for item in market_data if 'VIX' in item['name']]
        if vix_data:
            vix_level = vix_data[0]['current_price']
            return min(10, vix_level / 4)  # Scale VIX to 1-10
        
        # Alternative: use overall volatility
        changes = [abs(item['change_pct']) for item in market_data]
        avg_volatility = np.mean(changes) if changes else 0
        return min(10, avg_volatility)
    
    def _empty_assessment(self):
        """Return empty assessment when no data"""
        return {
            'global_risk_score': 0,
            'intelligence_quality': 0,
            'total_sources': 0,
            'critical_items': 0,
            'high_items': 0,
            'avg_sentiment': 0,
            'regional_analysis': {},
            'market_stress': 0,
            'timestamp': datetime.now()
        }

# ============================================================================
# VISUALIZATION ENGINE
# ============================================================================

def create_risk_gauge(risk_score):
    """Create professional risk gauge"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Global Risk Assessment", 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': "#0F172A"},
            'steps': [
                {'range': [0, 3], 'color': "#D1FAE5"},
                {'range': [3, 6], 'color': "#FEF3C7"},
                {'range': [6, 8], 'color': "#FED7AA"},
                {'range': [8, 10], 'color': "#FEE2E2"}
            ]
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#1E293B'},
        height=300
    )
    
    return fig

def create_sentiment_chart(intelligence_data):
    """Create sentiment distribution chart"""
    if not intelligence_data:
        return None
    
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for item in intelligence_data:
        label = item.get('sentiment_label', 'Neutral')
        sentiment_counts[label] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(sentiment_counts.keys()),
            y=list(sentiment_counts.values()),
            marker_color=['#059669', '#DC2626', '#64748B']
        )
    ])
    
    fig.update_layout(
        title="Sentiment Distribution",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#1E293B'},
        height=300
    )
    
    return fig

def create_regional_chart(regional_data):
    """Create regional analysis chart"""
    if not regional_data:
        return None
    
    regions = list(regional_data.keys())
    risk_scores = [data['risk_score'] for data in regional_data.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            y=regions,
            x=risk_scores,
            orientation='h',
            marker_color=['#DC2626' if score >= 7 else '#D97706' if score >= 5 else '#059669' for score in risk_scores]
        )
    ])
    
    fig.update_layout(
        title="Regional Risk Assessment",
        xaxis_title="Risk Score (1-10)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#1E293B'},
        height=400
    )
    
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">Strategic Intelligence Hub</h1>
        <p class="header-subtitle">Global Intelligence Collection & Analysis Platform</p>
        <div class="live-indicator">Live Data Collection Active</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("### Intelligence Controls")
    
    regions = ['Global', 'North America', 'Europe', 'Asia Pacific', 'Middle East', 'Eastern Europe']
    selected_regions = st.sidebar.multiselect("Active Regions:", regions, default=['Global'])
    
    priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    selected_priorities = st.sidebar.multiselect("Priority Levels:", priorities, default=priorities)
    
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=False)
    
    if st.sidebar.button("Refresh Intelligence", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Initialize systems
    collector = IntelligenceCollector()
    analyzer = AnalyticsEngine()
    
    # Data collection
    with st.container():
        st.markdown("### Intelligence Collection Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.spinner("Collecting social intelligence..."):
                reddit_data = collector.collect_reddit_intelligence()
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(reddit_data)}</div>
                <div class="metric-label">Social Intelligence</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.spinner("Collecting news intelligence..."):
                news_data = collector.collect_news_intelligence()
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(news_data)}</div>
                <div class="metric-label">News Intelligence</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            with st.spinner("Collecting market data..."):
                market_data = collector.collect_market_intelligence()
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(market_data)}</div>
                <div class="metric-label">Market Intelligence</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Generate assessment
    assessment = analyzer.generate_assessment(reddit_data, news_data, market_data)
    
    # Executive metrics
    st.markdown("### Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_score = assessment['global_risk_score']
        risk_class = "status-critical" if risk_score >= 7 else "status-warning" if risk_score >= 5 else "status-operational"
        if st.button(f"Risk: {risk_score:.1f}/10", key="risk", use_container_width=True):
            st.info(f"**Global Risk Assessment**\n\nLevel: {risk_score:.1f}/10\nSources: {assessment['total_sources']}\nCritical Items: {assessment['critical_items']}")
    
    with col2:
        quality = assessment['intelligence_quality']
        if st.button(f"Quality: {quality:.1f}/10", key="quality", use_container_width=True):
            st.info(f"**Intelligence Quality**\n\nAverage Score: {quality:.1f}/10\nTotal Sources: {assessment['total_sources']}")
    
    with col3:
        sentiment = assessment['avg_sentiment']
        sentiment_class = "sentiment-positive" if sentiment > 0.1 else "sentiment-negative" if sentiment < -0.1 else "sentiment-neutral"
        if st.button(f"Sentiment: {sentiment:.2f}", key="sentiment", use_container_width=True):
            st.info(f"**Global Sentiment**\n\nAverage: {sentiment:.3f}\nSample Size: {assessment['total_sources']}")
    
    with col4:
        market_stress = assessment['market_stress']
        if st.button(f"Market: {market_stress:.1f}/10", key="market", use_container_width=True):
            st.info(f"**Market Stress**\n\nLevel: {market_stress:.1f}/10\nTracked Assets: {len(market_data)}")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Strategic Overview", "Intelligence Feed", "Regional Analysis", "Market Intelligence"])
    
    with tab1:
        st.markdown("### Strategic Intelligence Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_fig = create_risk_gauge(assessment['global_risk_score'])
            st.plotly_chart(risk_fig, use_container_width=True)
        
        with col2:
            sentiment_fig = create_sentiment_chart(reddit_data + news_data)
            if sentiment_fig:
                st.plotly_chart(sentiment_fig, use_container_width=True)
        
        # Top intelligence items
        st.markdown("### Priority Intelligence")
        
        all_intelligence = reddit_data + news_data
        top_items = sorted(all_intelligence, key=lambda x: x.get('intelligence_score', 0), reverse=True)[:10]
        
        for item in top_items:
            priority_class = f"priority-{item.get('priority', 'medium').lower()}"
            sentiment_class = f"sentiment-{item.get('sentiment_label', 'neutral').lower()}"
            
            st.markdown(f"""
            <div class="intelligence-item {priority_class}">
                <div style="margin-bottom: 0.5rem;">
                    <span class="tag tag-{item.get('priority', 'medium').lower()}">{item.get('priority', 'MEDIUM')}</span>
                    <span class="tag">Score: {item.get('intelligence_score', 0):.1f}/10</span>
                    <span class="tag">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                   <span class="{sentiment_class}">Sentiment: {item.get('sentiment_label', 'Neutral')}</span>
               </div>
               
               <h4 style="margin-bottom: 0.5rem; color: var(--accent-blue);">{item['title']}</h4>
               
               <p style="margin-bottom: 0.5rem; color: var(--text-secondary);">{item.get('content', '')[:200]}...</p>
               
               <div style="margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-secondary);">
                   <strong>Source:</strong> {item['source']} | 
                   <strong>Category:</strong> {item.get('category', 'Unknown')} | 
                   <strong>Time:</strong> {item['timestamp'].strftime('%H:%M')}
               </div>
               
               <div>
                   <a href="{item['url']}" target="_blank" style="color: var(--accent-blue); text-decoration: none; font-weight: 600;">
                       View Source
                   </a>
               </div>
           </div>
           """, unsafe_allow_html=True)
   
   with tab2:
       st.markdown("### Live Intelligence Feed")
       
       # Filter controls
       col1, col2 = st.columns(2)
       
       with col1:
           min_score = st.slider("Minimum Intelligence Score", 0.0, 10.0, 5.0, 0.1)
       
       with col2:
           source_filter = st.selectbox("Source Type", ["All Sources", "Social Intelligence", "News Intelligence"])
       
       # Filter and display intelligence
       all_intelligence = []
       
       if source_filter in ["All Sources", "Social Intelligence"]:
           for item in reddit_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities and
                   item.get('region') in selected_regions):
                   all_intelligence.append(item)
       
       if source_filter in ["All Sources", "News Intelligence"]:
           for item in news_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities):
                   all_intelligence.append(item)
       
       # Sort by intelligence score
       all_intelligence.sort(key=lambda x: x.get('intelligence_score', 0), reverse=True)
       
       st.markdown(f"**Intelligence Items: {len(all_intelligence)}**")
       
       # Group by category
       categories = {}
       for item in all_intelligence[:50]:
           category = item.get('category', 'Unknown')
           if category not in categories:
               categories[category] = []
           categories[category].append(item)
       
       for category, items in categories.items():
           if items:
               avg_score = np.mean([item.get('intelligence_score', 0) for item in items])
               
               st.markdown(f"""
               <div class="intelligence-section">
                   <div class="section-title">{category}</div>
                   <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                       {len(items)} sources | Average Score: {avg_score:.1f}/10
                   </p>
               """, unsafe_allow_html=True)
               
               for item in items[:8]:
                   priority_class = f"priority-{item.get('priority', 'medium').lower()}"
                   sentiment_class = f"sentiment-{item.get('sentiment_label', 'neutral').lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <div style="margin-bottom: 0.5rem;">
                           <span class="tag tag-{item.get('priority', 'medium').lower()}">{item.get('priority', 'MEDIUM')}</span>
                           <span class="tag">Score: {item.get('intelligence_score', 0):.1f}/10</span>
                           <span class="tag">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                           <span class="{sentiment_class}">
                               {item.get('sentiment_label', 'Neutral')} ({item.get('sentiment_polarity', 0):.2f})
                           </span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: var(--accent-blue);">{item['title']}</h4>
                       
                       <p style="margin-bottom: 0.5rem; color: var(--text-secondary);">{item.get('content', '')[:250]}...</p>
                       
                       <div style="margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-secondary);">
                           <strong>Source:</strong> {item['source']} | 
                           <strong>Time:</strong> {item['timestamp'].strftime('%H:%M')} |
                           {f"<strong>Engagement:</strong> {item.get('score', 0)} upvotes, {item.get('comments', 0)} comments" if item.get('score') else ""}
                       </div>
                       
                       <div>
                           <a href="{item['url']}" target="_blank" style="color: var(--accent-blue); text-decoration: none; font-weight: 600;">
                               View Source
                           </a>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
   
   with tab3:
       st.markdown("### Regional Intelligence Analysis")
       
       regional_data = assessment['regional_analysis']
       
       if regional_data:
           # Regional overview chart
           regional_fig = create_regional_chart(regional_data)
           if regional_fig:
               st.plotly_chart(regional_fig, use_container_width=True)
           
           # Detailed regional breakdown
           st.markdown("### Regional Intelligence Breakdown")
           
           for region, data in regional_data.items():
               if region in selected_regions:
                   risk_class = "status-critical" if data['risk_score'] >= 7 else "status-warning" if data['risk_score'] >= 5 else "status-operational"
                   
                   st.markdown(f"""
                   <div class="intelligence-section">
                       <div class="section-title">{region} Intelligence Assessment</div>
                       
                       <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem;">
                           <div style="text-align: center; padding: 1rem; background: var(--secondary-bg); border-radius: 6px;">
                               <div style="font-size: 1.5rem; font-weight: 600; color: var(--accent-blue);">{data['risk_score']:.1f}/10</div>
                               <div style="font-size: 0.8rem; color: var(--text-secondary);">Risk Score</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: var(--secondary-bg); border-radius: 6px;">
                               <div style="font-size: 1.5rem; font-weight: 600; color: var(--accent-blue);">{data['items']}</div>
                               <div style="font-size: 0.8rem; color: var(--text-secondary);">Total Sources</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: var(--secondary-bg); border-radius: 6px;">
                               <div style="font-size: 1.5rem; font-weight: 600; color: var(--accent-red);">{data['critical']}</div>
                               <div style="font-size: 0.8rem; color: var(--text-secondary);">Critical Items</div>
                           </div>
                           
                           <div style="text-align: center; padding: 1rem; background: var(--secondary-bg); border-radius: 6px;">
                               <div style="font-size: 1.5rem; font-weight: 600; color: {'var(--accent-green)' if data['avg_sentiment'] > 0 else 'var(--accent-red)' if data['avg_sentiment'] < 0 else 'var(--text-secondary)'};">{data['avg_sentiment']:.2f}</div>
                               <div style="font-size: 0.8rem; color: var(--text-secondary);">Avg Sentiment</div>
                           </div>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       else:
           st.info("No regional data available. Collect more intelligence sources to enable regional analysis.")
   
   with tab4:
       st.markdown("### Market Intelligence")
       
       if market_data:
           # Market performance overview
           market_df = pd.DataFrame(market_data)
           
           col1, col2 = st.columns(2)
           
           with col1:
               # Market performance chart
               colors = ['#DC2626' if x < -2 else '#D97706' if x < 0 else '#059669' if x > 2 else '#0F172A' for x in market_df['change_pct']]
               
               fig = go.Figure()
               fig.add_trace(go.Bar(
                   x=market_df['name'],
                   y=market_df['change_pct'],
                   marker_color=colors,
                   text=[f"{x:.2f}%" for x in market_df['change_pct']],
                   textposition='auto'
               ))
               
               fig.update_layout(
                   title="Market Performance (%)",
                   xaxis_title="Assets",
                   yaxis_title="Change %",
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)',
                   font={'color': '#1E293B'},
                   height=400
               )
               fig.update_xaxis(tickangle=45)
               st.plotly_chart(fig, use_container_width=True)
           
           with col2:
               st.markdown("### Market Stress Indicators")
               
               # Market stress metrics
               vix_data = market_df[market_df['name'].str.contains('VIX', na=False)]
               if not vix_data.empty:
                   vix_level = vix_data.iloc[0]['current_price']
                   st.metric("VIX Fear Index", f"{vix_level:.2f}", 
                            help="Values >30 indicate high market fear")
               
               # Defense sector performance
               defense_stocks = market_df[market_df['name'].str.contains('Lockheed|Raytheon', na=False)]
               if not defense_stocks.empty:
                   st.markdown("**Defense Sector Performance:**")
                   for _, stock in defense_stocks.iterrows():
                       change_color = "🟢" if stock['change_pct'] > 0 else "🔴"
                       st.markdown(f"{change_color} **{stock['name']}**: {stock['change_pct']:.2f}%")
               
               # Safe haven assets
               safe_haven = market_df[market_df['name'].str.contains('Gold', na=False)]
               if not safe_haven.empty:
                   st.markdown("**Safe Haven Assets:**")
                   for _, asset in safe_haven.iterrows():
                       change_color = "🟢" if asset['change_pct'] > 0 else "🔴"
                       st.markdown(f"{change_color} **{asset['name']}**: ${asset['current_price']:.2f} ({asset['change_pct']:.2f}%)")
           
           # Detailed market data
           st.markdown("### Detailed Market Data")
           
           for _, asset in market_df.iterrows():
               change_class = "status-operational" if asset['change_pct'] > 1 else "status-critical" if asset['change_pct'] < -1 else "status-warning"
               
               st.markdown(f"""
               <div class="intelligence-item">
                   <div style="display: flex; justify-content: space-between; align-items: center;">
                       <div>
                           <h4 style="margin: 0; color: var(--accent-blue);">{asset['name']} ({asset['ticker']})</h4>
                           <p style="margin: 0; color: var(--text-secondary);">Current Price: ${asset['current_price']:.2f}</p>
                       </div>
                       <div style="text-align: right;">
                           <div style="font-size: 1.2rem; font-weight: 600;" class="{change_class}">
                               {asset['change_pct']:+.2f}%
                           </div>
                       </div>
                   </div>
               </div>
               """, unsafe_allow_html=True)
       else:
           st.warning("Market intelligence temporarily unavailable")
   
   # Export section
   st.markdown("### Intelligence Export")
   
   col1, col2, col3 = st.columns(3)
   
   with col1:
       if st.button("Export Executive Summary", use_container_width=True):
           summary_data = {
               'executive_summary': {
                   'timestamp': datetime.now().isoformat(),
                   'global_risk': assessment['global_risk_score'],
                   'intelligence_quality': assessment['intelligence_quality'],
                   'total_sources': assessment['total_sources'],
                   'critical_items': assessment['critical_items'],
                   'avg_sentiment': assessment['avg_sentiment'],
                   'market_stress': assessment['market_stress']
               },
               'regional_analysis': assessment['regional_analysis'],
               'classification': 'INTERNAL USE'
           }
           
           json_summary = json.dumps(summary_data, default=str, indent=2)
           st.download_button(
               label="Download Executive Summary",
               data=json_summary,
               file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   with col2:
       if st.button("Export Intelligence Data", use_container_width=True):
           intelligence_data = {
               'social_intelligence': reddit_data,
               'news_intelligence': news_data,
               'market_intelligence': market_data,
               'total_sources': len(reddit_data) + len(news_data),
               'classification': 'INTERNAL USE'
           }
           
           json_intel = json.dumps(intelligence_data, default=str, indent=2)
           st.download_button(
               label="Download Intelligence Data",
               data=json_intel,
               file_name=f"intelligence_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   with col3:
       if st.button("Export Full Report", use_container_width=True):
           full_data = {
               'assessment': assessment,
               'social_intelligence': reddit_data,
               'news_intelligence': news_data,
               'market_intelligence': market_data,
               'generated_at': datetime.now().isoformat(),
               'classification': 'INTERNAL USE'
           }
           
           json_full = json.dumps(full_data, default=str, indent=2)
           st.download_button(
               label="Download Full Report",
               data=json_full,
               file_name=f"full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   # Auto-refresh
   if auto_refresh:
       countdown_placeholder = st.empty()
       for remaining in range(300, 0, -1):
           mins, secs = divmod(remaining, 60)
           countdown_placeholder.markdown(f"""
           <div style="position: fixed; bottom: 20px; right: 20px; background: var(--primary-bg); 
                      border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; 
                      box-shadow: var(--shadow); z-index: 1000;">
               <div style="color: var(--accent-blue); font-weight: 600;">
                   Next refresh: {mins:02d}:{secs:02d}
               </div>
           </div>
           """, unsafe_allow_html=True)
           time.sleep(1)
       
       st.cache_data.clear()
       st.rerun()

if __name__ == "__main__":
   main()
