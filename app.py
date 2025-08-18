# ============================================================================
# ULTIMATE WHITE LUXURY INTELLIGENCE HUB v4.0
# Sophisticated • Minimalist • Executive Grade
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import feedparser
import praw
from datetime import datetime, timedelta
import time
import json
from textblob import TextBlob
import warnings
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
        --charcoal: #222222;
        --navy-blue: #003366;
        --executive-gold: #C9A227;
        --emerald-green: #2E8B57;
        --scarlet-red: #B22222;
        --soft-blue: #E6F3FF;
        --soft-gold: #FDF6E3;
        --soft-green: #F0F8F5;
        --soft-red: #FDF2F2;
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
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
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
    
    .metric-card {
        text-align: center;
        padding: 2rem 1rem;
        background: var(--pure-white);
        border: 1px solid var(--subtle-gray);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
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
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
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
    
    div[data-testid="stSidebar"] {
        background: var(--soft-white);
        border-right: 1px solid var(--subtle-gray);
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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA COLLECTION
# ============================================================================

class IntelligenceCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Strategic-Intelligence-Hub/4.0'
        })
        
        try:
            self.reddit = praw.Reddit(
                client_id="gPAQFk1IFWSkMEVMXFMMCQ",
                client_secret="2LoxxZ8c-Cr-Y0rrE9CmwvQQuHdskw",
                user_agent="StrategicWarRoom/1.0 by u/Quick_Shower_6934"
            )
        except:
            self.reddit = None
        
        self.intelligence_sources = {
            'geopolitical': {
                'Reuters World': 'https://feeds.reuters.com/reuters/worldNews',
                'AP International': 'https://feeds.apnews.com/rss/apf-topnews',
                'BBC Global': 'http://feeds.bbci.co.uk/news/world/rss.xml'
            },
            'defense': {
                'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
                'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/'
            }
        }
        
        self.subreddits = {
            'worldnews': {'region': 'Global', 'factor': 'Public Opinion'},
            'geopolitics': {'region': 'Global', 'factor': 'Strategic Thinking'},
            'investing': {'region': 'Global', 'factor': 'Market Psychology'}
        }

    @st.cache_data(ttl=300)
    def collect_human_intelligence(_self):
        """Collect human intelligence from Reddit"""
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
                    
                    # Calculate scores (1-10 scale)
                    credibility = _self._calculate_credibility(post, subreddit_name)
                    impact = _self._calculate_impact(post, sentiment)
                    intelligence_score = (credibility + impact) / 2
                    
                    # Priority
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
                        'category': config['factor'],
                        'title': post.title,
                        'content_preview': post.selftext[:200] if post.selftext else 'Link post',
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'comments': post.num_comments,
                        'sentiment_polarity': sentiment.polarity,
                        'sentiment_label': _self._get_sentiment_label(sentiment.polarity),
                        'credibility_score': credibility,
                        'impact_score': impact,
                        'intelligence_score': intelligence_score,
                        'priority': priority,
                        'region': config['region'],
                        'timestamp': datetime.fromtimestamp(post.created_utc),
                        'type': 'human_intelligence'
                    })
                    
            except Exception as e:
                continue
        
        return sorted(intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    @st.cache_data(ttl=300)
    def collect_news_intelligence(_self):
        """Collect news intelligence"""
        news_intelligence = []
        
        for category, sources in _self.intelligence_sources.items():
            for source_name, url in sources.items():
                try:
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:8]:
                        full_content = f"{entry.title} {entry.get('summary', '')}"
                        sentiment = TextBlob(full_content).sentiment
                        
                        # Calculate scores
                        credibility = _self._calculate_news_credibility(source_name)
                        relevance = _self._calculate_relevance(full_content)
                        intelligence_score = (credibility + relevance) / 2
                        
                        # Priority
                        if intelligence_score >= 8.5:
                            priority = 'CRITICAL'
                        elif intelligence_score >= 7.0:
                            priority = 'HIGH'
                        elif intelligence_score >= 5.0:
                            priority = 'MEDIUM'
                        else:
                            priority = 'LOW'
                        
                        news_intelligence.append({
                            'source': source_name,
                            'category': category.title(),
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:250],
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
                    continue
        
        return sorted(news_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

    def _calculate_credibility(self, post, subreddit_name):
        """Calculate Reddit credibility (1-10)"""
        base = {'worldnews': 8, 'geopolitics': 9, 'investing': 7}.get(subreddit_name, 5)
        if post.upvote_ratio > 0.9 and post.score > 1000:
            base += 1
        return min(10, max(1, base))

    def _calculate_impact(self, post, sentiment):
        """Calculate impact score (1-10)"""
        engagement = min(3, (post.score + post.num_comments) / 1000)
        sentiment_factor = abs(sentiment.polarity) * 2
        return min(10, max(1, 5 + engagement + sentiment_factor))

    def _calculate_news_credibility(self, source_name):
        """Calculate news credibility (1-10)"""
        scores = {
            'Reuters': 10, 'AP': 10, 'BBC': 9.5, 'Defense News': 8, 'Military Times': 7.5
        }
        for source, score in scores.items():
            if source.lower() in source_name.lower():
                return score
        return 6.0

    def _calculate_relevance(self, content):
        """Calculate relevance (1-10)"""
        keywords = ['war', 'conflict', 'crisis', 'emergency', 'military', 'security']
        content_lower = content.lower()
        score = 5 + sum(2 for keyword in keywords if keyword in content_lower)
        return min(10, max(1, score))

    def _get_sentiment_label(self, polarity):
        """Convert polarity to label"""
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
    def generate_assessment(self, reddit_data, news_data):
        """Generate executive assessment"""
        all_data = reddit_data + news_data
        
        if not all_data:
            return self._empty_assessment()
        
        # Calculate metrics
        total_sources = len(all_data)
        critical_items = len([item for item in all_data if item.get('priority') == 'CRITICAL'])
        
        # Intelligence quality
        scores = [item.get('intelligence_score', 0) for item in all_data]
        avg_intelligence = np.mean(scores) if scores else 5.0
        
        # Sentiment analysis
        sentiments = [item.get('sentiment_polarity', 0) for item in all_data]
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        
        # Risk assessment
        risk_score = min(10, (critical_items * 2) + (avg_intelligence / 2))
        
        # Regional analysis
        regions = {}
        for item in all_data:
            region = item.get('region', 'Global')
            if region not in regions:
                regions[region] = {'items': 0, 'critical': 0, 'sentiment': []}
            regions[region]['items'] += 1
            if item.get('priority') == 'CRITICAL':
                regions[region]['critical'] += 1
            regions[region]['sentiment'].append(item.get('sentiment_polarity', 0))
        
        # Calculate regional risk scores
        for region, data in regions.items():
            sentiment_avg = np.mean(data['sentiment']) if data['sentiment'] else 0
            data['risk_score'] = min(10, (data['critical'] * 3) + abs(sentiment_avg) * 5)
            data['avg_sentiment'] = sentiment_avg
        
        return {
            'global_risk_score': risk_score,
            'intelligence_quality': avg_intelligence,
            'total_sources': total_sources,
            'critical_items': critical_items,
            'avg_sentiment': avg_sentiment,
            'regional_risks': regions,
            'timestamp': datetime.now()
        }
    
    def _empty_assessment(self):
        """Return empty assessment when no data"""
        return {
            'global_risk_score': 0,
            'intelligence_quality': 0,
            'total_sources': 0,
            'critical_items': 0,
            'avg_sentiment': 0,
            'regional_risks': {},
            'timestamp': datetime.now()
        }

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_risk_gauge(risk_score):
    """Create risk gauge chart"""
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
            ]
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#222222',
        height=300
    )
    
    return fig

def create_sentiment_chart(sentiment_data):
    """Create sentiment distribution chart"""
    if not sentiment_data:
        return None
    
    # Count sentiments
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for item in sentiment_data:
        label = item.get('sentiment_label', 'Neutral')
        sentiment_counts[label] += 1
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(sentiment_counts.keys()),
            values=list(sentiment_counts.values()),
            hole=.4,
            marker_colors=['#2E8B57', '#B22222', '#CCCCCC']
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#222222',
        title={'text': 'Sentiment Distribution', 'x': 0.5, 'font': {'size': 16, 'color': '#003366'}},
        height=300
    )
    
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
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
    
    # Sidebar
    st.sidebar.markdown("## Strategic Controls")
    st.sidebar.markdown("---")
    
    regions = ['Global', 'North America', 'Europe', 'Asia Pacific', 'Middle East']
    selected_regions = st.sidebar.multiselect("Monitor Regions:", regions, default=['Global'])
    
    priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    selected_priorities = st.sidebar.multiselect("Priority Levels:", priorities, default=priorities)
    
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=False)
    
    if st.sidebar.button("🔄 Refresh Intelligence", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Initialize systems
    collector = IntelligenceCollector()
    analyzer = AnalyticsEngine()
    
    # Data collection
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
    
    # Generate assessment
    assessment = analyzer.generate_assessment(reddit_data, news_data)
    
    # Executive metrics
    st.markdown("### ⚪ Executive Intelligence Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_score = assessment['global_risk_score']
        if st.button(f"Risk: {risk_score:.1f}/10", key="risk", use_container_width=True):
            st.info(f"**Global Risk Assessment**\n\nLevel: {risk_score:.1f}/10\nSources: {assessment['total_sources']}")
    
    with col2:
        quality = assessment['intelligence_quality']
        if st.button(f"Quality: {quality:.1f}/10", key="quality", use_container_width=True):
            st.info(f"**Intelligence Quality**\n\nAverage: {quality:.1f}/10\nCritical: {assessment['critical_items']}")
    
    with col3:
        sentiment = assessment['avg_sentiment']
        if st.button(f"Sentiment: {sentiment:.2f}", key="sentiment", use_container_width=True):
            st.info(f"**Overall Sentiment**\n\nAverage: {sentiment:.3f}\nSample: {assessment['total_sources']} sources")
    
    with col4:
        if st.button(f"Sources: {assessment['total_sources']}", key="sources", use_container_width=True):
            st.info(f"**Intelligence Sources**\n\nReddit: {len(reddit_data)}\nNews: {len(news_data)}")
    
    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Strategic Overview", "📊 Intelligence Feed", "🌍 Regional Analysis"])
    
    with tab1:
        st.markdown("## 🎯 Strategic Intelligence Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Global Risk Dial")
            risk_fig = create_risk_gauge(assessment['global_risk_score'])
            st.plotly_chart(risk_fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Sentiment Distribution")
            sentiment_fig = create_sentiment_chart(reddit_data + news_data)
            if sentiment_fig:
                st.plotly_chart(sentiment_fig, use_container_width=True)
        
        # Top critical events
        st.markdown("### 🚨 Top Critical Intelligence")
        
        all_intelligence = reddit_data + news_data
        critical_events = [item for item in all_intelligence if item.get('priority') == 'CRITICAL'][:5]
        
        if not critical_events:
            critical_events = sorted(all_intelligence, key=lambda x: x.get('intelligence_score', 0), reverse=True)[:5]
        
        for event in critical_events:
            priority_class = f"priority-{event.get('priority', 'medium').lower()}"
            sentiment_class = f"sentiment-{event.get('sentiment_label', 'neutral').lower()}"
            
            st.markdown(f"""
            <div class="intelligence-item {priority_class}">
                <div style="margin-bottom: 0.8rem;">
            <span class="tag-elegant tag-{event.get('priority', 'medium').lower()}">{event.get('priority', 'MEDIUM')}</span>
                   <span class="tag-elegant">Score: {event.get('intelligence_score', 0):.1f}/10</span>
                   <span class="tag-elegant">{event.get('category', 'Unknown')}</span>
                   <span class="sentiment-indicator {sentiment_class}">
                       {event.get('sentiment_label', 'Neutral')}
                   </span>
               </div>
               
               <h4 style="margin-bottom: 0.5rem; color: #003366; font-weight: 600;">{event['title']}</h4>
               
               <p style="margin-bottom: 0.5rem; color: #222222; line-height: 1.5;">{event.get('content_preview', event.get('summary', ''))[:200]}...</p>
               
               <div style="margin-bottom: 0.8rem;">
                   <span style="color: #222222;"><strong>Source:</strong> {event['source']}</span>
                   <span style="color: #222222; margin-left: 1rem;"><strong>Region:</strong> {event.get('region', 'Global')}</span>
                   <span style="color: #222222; margin-left: 1rem;"><strong>Time:</strong> {event['timestamp'].strftime('%H:%M')}</span>
               </div>
               
               <div style="margin-top: 1rem;">
                   <a href="{event['url']}" target="_blank" style="color: #003366; text-decoration: none; font-weight: 600; border: 1px solid #003366; padding: 0.4rem 1rem; border-radius: 6px;">
                       📖 VIEW SOURCE
                   </a>
               </div>
           </div>
           """, unsafe_allow_html=True)
   
       with tab2:
       st.markdown("## 📊 Comprehensive Intelligence Feed")
       
       # Filter controls
       col1, col2 = st.columns(2)
       
       with col1:
           min_score = st.slider("Minimum Intelligence Score", 0.0, 10.0, 5.0, 0.1)
       
       with col2:
           source_type = st.selectbox("Source Type", ["All Sources", "Human Intelligence", "News Intelligence"])
       
       # Filter intelligence
       all_intelligence = []
       
       if source_type in ["All Sources", "Human Intelligence"]:
           for item in reddit_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities):
                   all_intelligence.append(item)
       
       if source_type in ["All Sources", "News Intelligence"]:
           for item in news_data:
               if (item.get('intelligence_score', 0) >= min_score and
                   item.get('priority') in selected_priorities):
                   all_intelligence.append(item)
       
       # Sort by intelligence score
       all_intelligence.sort(key=lambda x: x.get('intelligence_score', 0), reverse=True)
       
       st.markdown(f"### 📡 Intelligence Feed ({len(all_intelligence)} items)")
       
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
                   <div class="section-header">{category.upper()} INTELLIGENCE</div>
                   <p style="color: #222222; margin-bottom: 1rem;">
                       <strong>{len(items)} sources</strong> | 
                       <strong>Avg Score: {avg_score:.1f}/10</strong>
                   </p>
               """, unsafe_allow_html=True)
               
               for item in items[:8]:  # Show top 8 per category
                   priority_class = f"priority-{item.get('priority', 'medium').lower()}"
                   sentiment_class = f"sentiment-{item.get('sentiment_label', 'neutral').lower()}"
                   
                   st.markdown(f"""
                   <div class="intelligence-item {priority_class}">
                       <div style="margin-bottom: 0.8rem;">
                           <span class="tag-elegant tag-{item.get('priority', 'medium').lower()}">{item.get('priority', 'MEDIUM')}</span>
                           <span class="tag-elegant">Intelligence: {item.get('intelligence_score', 0):.1f}/10</span>
                           <span class="tag-elegant">Credibility: {item.get('credibility_score', 0):.1f}/10</span>
                           <span class="sentiment-indicator {sentiment_class}">
                               {item.get('sentiment_label', 'Neutral')} ({item.get('sentiment_polarity', 0):.2f})
                           </span>
                       </div>
                       
                       <h4 style="margin-bottom: 0.5rem; color: #003366; font-weight: 600;">{item['title']}</h4>
                       
                       <p style="margin-bottom: 0.8rem; color: #222222; line-height: 1.5;">{item.get('content_preview', item.get('summary', ''))[:250]}...</p>
                       
                       <div style="margin-bottom: 0.8rem;">
                           <span style="color: #222222;"><strong>Source:</strong> {item['source']}</span>
                           <span style="color: #222222; margin-left: 1rem;"><strong>Time:</strong> {item['timestamp'].strftime('%H:%M')}</span>
                           {f'<span style="color: #222222; margin-left: 1rem;"><strong>Engagement:</strong> {item.get("score", 0)} ↑ {item.get("comments", 0)} 💬</span>' if item.get('score') else ''}
                       </div>
                       
                       <div style="margin-top: 1rem;">
                           <a href="{item['url']}" target="_blank" style="color: #003366; text-decoration: none; font-weight: 600; border: 1px solid #003366; padding: 0.4rem 1rem; border-radius: 6px;">
                               📖 VIEW SOURCE
                           </a>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
               
               st.markdown("</div>", unsafe_allow_html=True)
   
   with tab3:
       st.markdown("## 🌍 Regional Risk Analysis")
       
       regional_risks = assessment['regional_risks']
       
       if regional_risks:
           # Regional overview
           risk_data = []
           for region, data in regional_risks.items():
               risk_data.append({
                   'Region': region,
                   'Risk Score': data['risk_score'],
                   'Total Items': data['items'],
                   'Critical Items': data['critical'],
                   'Avg Sentiment': data['avg_sentiment']
               })
           
           risk_df = pd.DataFrame(risk_data)
           
           col1, col2 = st.columns(2)
           
           with col1:
               st.markdown("### 📊 Regional Risk Scores")
               
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
                   st.markdown(f"""
                   <div class="intelligence-section">
                       <div class="section-header">{region.upper()} INTELLIGENCE ASSESSMENT</div>
                       
                       <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                           <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                               <div style="font-size: 1.5rem; font-weight: 700; color: #003366;">{data['risk_score']:.1f}/10</div>
                               <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Risk Score</div>
                           </div>
                           
                           <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                               <div style="font-size: 1.5rem; font-weight: 700; color: #003366;">{data['items']}</div>
                               <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Total Sources</div>
                           </div>
                           
                           <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                               <div style="font-size: 1.5rem; font-weight: 700; color: #B22222;">{data['critical']}</div>
                               <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Critical Items</div>
                           </div>
                           
                           <div style="background: #F5F5F5; padding: 1rem; border-radius: 8px; text-align: center;">
                               <div style="font-size: 1.5rem; font-weight: 700; color: {'#2E8B57' if data['avg_sentiment'] > 0 else '#B22222' if data['avg_sentiment'] < 0 else '#222222'};">{data['avg_sentiment']:.2f}</div>
                               <div style="font-size: 0.8rem; color: #222222; text-transform: uppercase;">Avg Sentiment</div>
                           </div>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       else:
           st.info("No regional data available. Collect more intelligence sources to see regional analysis.")
   
   # Export section
   st.markdown("### 📤 Intelligence Export Options")
   
   col1, col2, col3 = st.columns(3)
   
   with col1:
       if st.button("📊 Executive Summary", use_container_width=True):
           summary_data = {
               'executive_summary': {
                   'timestamp': datetime.now().isoformat(),
                   'global_risk': assessment['global_risk_score'],
                   'intelligence_quality': assessment['intelligence_quality'],
                   'total_sources': assessment['total_sources'],
                   'critical_items': assessment['critical_items'],
                   'avg_sentiment': assessment['avg_sentiment']
               },
               'regional_risks': assessment['regional_risks'],
               'classification': 'SENSITIVE'
           }
           
           json_summary = json.dumps(summary_data, default=str, indent=2)
           st.download_button(
               label="📥 Download Executive Summary",
               data=json_summary,
               file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   with col2:
       if st.button("🧠 Human Intelligence", use_container_width=True):
           human_data = {
               'human_intelligence_sources': reddit_data,
               'total_sources': len(reddit_data),
               'classification': 'SENSITIVE'
           }
           
           json_human = json.dumps(human_data, default=str, indent=2)
           st.download_button(
               label="📥 Download Human Intelligence",
               data=json_human,
               file_name=f"human_intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   with col3:
       if st.button("📄 Full Report", use_container_width=True):
           full_data = {
               'assessment': assessment,
               'human_intelligence': reddit_data,
               'news_intelligence': news_data,
               'generated_at': datetime.now().isoformat(),
               'classification': 'SENSITIVE'
           }
           
           json_full = json.dumps(full_data, default=str, indent=2)
           st.download_button(
               label="📥 Download Full Report",
               data=json_full,
               file_name=f"full_intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
               mime="application/json"
           )
   
   # Auto-refresh
   if auto_refresh:
       countdown_placeholder = st.empty()
       for remaining in range(300, 0, -1):
           mins, secs = divmod(remaining, 60)
           countdown_placeholder.markdown(f"""
           <div style="position: fixed; bottom: 20px; right: 20px; background: white; border: 1px solid #CCCCCC; border-radius: 8px; padding: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 1000;">
               <div style="color: #003366; font-weight: 600;">⏰ Next refresh: {mins:02d}:{secs:02d}</div>
           </div>
           """, unsafe_allow_html=True)
           time.sleep(1)
       
       st.cache_data.clear()
       st.rerun()

if __name__ == "__main__":
   main()
