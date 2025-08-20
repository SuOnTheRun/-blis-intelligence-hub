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
import xml.etree.ElementTree as ET
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION & API CREDENTIALS
# ============================================================================

# Your verified API credentials
NEWSAPI_KEY = st.secrets.get("NEWSAPI_KEY", "cdaa3b7303c740faa31a55fbb95bacd6")

# GDELT & Flight APIs (Free)
GDELT_API_BASE = "https://api.gdeltproject.org/api/v2/"

# ============================================================================
# COMPREHENSIVE INTELLIGENCE SOURCES
# ============================================================================

TIER_1_INTELLIGENCE_SOURCES = {
    'primary_news': {
        'Reuters World News': 'https://feeds.reuters.com/reuters/worldNews',
        'Reuters Politics': 'https://feeds.reuters.com/reuters/politicsNews',
        'Reuters Business': 'https://feeds.reuters.com/reuters/businessNews',
        'Associated Press International': 'https://feeds.apnews.com/rss/apf-topnews',
        'BBC World News': 'http://feeds.bbci.co.uk/news/world/rss.xml',
        'Financial Times World': 'https://www.ft.com/rss/home/world',
        'The Guardian World': 'https://www.theguardian.com/world/rss'
    },
    
    'defense_intelligence': {
        'Defense News': 'https://www.defensenews.com/arc/outboundfeeds/rss/',
        'Military Times': 'https://www.militarytimes.com/arc/outboundfeeds/rss/',
        'Breaking Defense': 'https://breakingdefense.com/feed/',
        'Defense One': 'https://www.defenseone.com/rss/policy/'
    },
    
    'strategic_analysis': {
        'Council on Foreign Relations': 'https://www.cfr.org/rss-feeds',
        'Atlantic Council': 'https://www.atlanticcouncil.org/feed/',
        'Carnegie Endowment': 'https://carnegieendowment.org/feed',
        'Brookings Institution': 'https://www.brookings.edu/feed/'
    }
}

# Global Intelligence Hotspots
GLOBAL_INTELLIGENCE_HOTSPOTS = {
    'Ukraine Operational Zone': {'lat': 49.5937, 'lon': 32.2922, 'priority': 'CRITICAL', 'region': 'Eastern Europe', 'type': 'Active Conflict'},
    'Gaza Strip': {'lat': 31.3547, 'lon': 34.3088, 'priority': 'CRITICAL', 'region': 'Middle East', 'type': 'Active Conflict'},
    'Taiwan Strait': {'lat': 23.8, 'lon': 120.9, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
    'South China Sea': {'lat': 16.0, 'lon': 114.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Strategic Waterway'},
    'Strait of Hormuz': {'lat': 26.5667, 'lon': 56.25, 'priority': 'HIGH', 'region': 'Middle East', 'type': 'Strategic Waterway'},
    'Korean DMZ': {'lat': 38.0, 'lon': 127.0, 'priority': 'HIGH', 'region': 'Asia Pacific', 'type': 'Border Tension'}
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
        --executive-white: #FFFFFF;
        --executive-light: #F8FAFC;
        --executive-border: #E5E7EB;
        --executive-text: #111827;
        --executive-red: #DC2626;
        --executive-green: #059669;
        --executive-amber: #D97706;
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
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        position: relative;
        overflow: hidden;
    }

    .command-title {
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: -3px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
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

    .intelligence-card {
        background: var(--executive-white);
        border: 1px solid var(--executive-border);
        border-radius: 0;
        padding: 2.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .intelligence-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
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
        color: var(--executive-text);
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
        border-left: 4px solid var(--executive-accent);
    }

    .intelligence-item:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateX(8px);
    }

    .priority-critical {
        border-left-color: var(--executive-red);
    }

    .priority-high {
        border-left-color: var(--executive-amber);
    }

    .priority-medium {
        border-left-color: var(--executive-accent);
    }

    .priority-low {
        border-left-color: var(--executive-green);
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
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA COLLECTION ENGINE
# ============================================================================

@st.cache_data(ttl=300)
def fetch_comprehensive_intelligence():
    """Fetch intelligence from all verified sources"""
    all_intelligence = []
    
    for category_name, sources in TIER_1_INTELLIGENCE_SOURCES.items():
        for source_name, url in sources.items():
            try:
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:5]:  # Limit per source
                    if not entry.title or len(entry.title) < 10:
                        continue
                    
                    text = f"{entry.title} {entry.get('summary', '')}"
                    sentiment = TextBlob(text).sentiment.polarity
                    
                    # Intelligence scoring
                    critical_terms = ['nuclear', 'missile', 'attack', 'invasion', 'war', 'bombing']
                    high_terms = ['military', 'conflict', 'crisis', 'sanctions', 'diplomacy']
                    
                    text_lower = text.lower()
                    critical_score = sum(5 for term in critical_terms if term in text_lower)
                    high_score = sum(3 for term in high_terms if term in text_lower)
                    
                    relevance_score = min(10, 2 + critical_score + high_score)
                    
                    # Source credibility
                    credibility_matrix = {
                        'reuters': 10, 'associated press': 10, 'bbc': 9,
                        'financial times': 9, 'council on foreign relations': 10,
                        'atlantic council': 8, 'carnegie': 8, 'brookings': 8,
                        'defense news': 8, 'military times': 7
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
                continue  # Skip failed sources
    
    return sorted(all_intelligence, key=lambda x: x['intelligence_score'], reverse=True)

@st.cache_data(ttl=300)
def fetch_market_intelligence():
    """Comprehensive market intelligence analysis"""
    
    strategic_tickers = {
        # Market Indices
        '^GSPC': {'name': 'S&P 500', 'category': 'Market Index', 'weight': 1.0},
        '^VIX': {'name': 'Volatility Index', 'category': 'Market Stress', 'weight': 2.5},
        
        # Defense & Aerospace
        'LMT': {'name': 'Lockheed Martin', 'category': 'Defense', 'weight': 2.0},
        'RTX': {'name': 'Raytheon Technologies', 'category': 'Defense', 'weight': 2.0},
        'BA': {'name': 'Boeing Company', 'category': 'Defense', 'weight': 1.8},
        'NOC': {'name': 'Northrop Grumman', 'category': 'Defense', 'weight': 1.9},
        
        # Safe Haven Assets
        'GLD': {'name': 'SPDR Gold Trust', 'category': 'Safe Haven', 'weight': 1.5},
        'TLT': {'name': '20+ Year Treasury Bond', 'category': 'Safe Haven', 'weight': 1.4},
        
        # Energy & Resources
        'XLE': {'name': 'Energy Select SPDR', 'category': 'Energy', 'weight': 1.6},
        'USO': {'name': 'United States Oil Fund', 'category': 'Energy', 'weight': 1.7}
    }
    
    market_intelligence = []
    
    for ticker, info in strategic_tickers.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if hist.empty:
                continue
            
            current_price = float(hist['Close'].iloc[-1])
            previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
            change_pct = ((current_price - previous_price) / previous_price) * 100 if previous_price else 0.0
            
            # Advanced metrics
            volatility = hist['Close'].pct_change().std() * 100 if len(hist) > 1 else 0
            volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
            
            # Intelligence significance calculation
            price_significance = abs(change_pct) * info['weight']
            volatility_significance = min(5, volatility * 2)
            
            total_significance = price_significance + volatility_significance
            
            # Market stress indicator
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
        'Eastern Europe': ['ukraine', 'russia', 'belarus', 'poland', 'baltic'],
        'Asia Pacific': ['china', 'taiwan', 'japan', 'korea', 'australia'],
        'Middle East': ['iran', 'israel', 'palestine', 'saudi', 'gulf', 'syria'],
        'Europe': ['nato', 'eu', 'france', 'germany', 'uk', 'britain'],
        'Africa': ['sudan', 'egypt', 'libya', 'algeria', 'morocco'],
        'Americas': ['usa', 'canada', 'mexico', 'brazil', 'venezuela']
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
    
    def generate_executive_assessment(self, all_intelligence, market_data):
        """Generate comprehensive executive assessment"""
        
        if not all_intelligence and not market_data:
            return self._baseline_assessment()
        
        # Core intelligence metrics
        total_sources = len(all_intelligence)
        critical_items = len([item for item in all_intelligence if item.get('priority') == 'CRITICAL'])
        high_items = len([item for item in all_intelligence if item.get('priority') == 'HIGH'])
        
        # Intelligence quality assessment
        intelligence_scores = [item.get('intelligence_score', 0) for item in all_intelligence]
        avg_intelligence_quality = np.mean(intelligence_scores) if intelligence_scores else 5.0
        
        # Sentiment analysis
        sentiments = [item.get('sentiment_polarity', 0) for item in all_intelligence]
        avg_sentiment = np.mean(sentiments) if sentiments else 0
        
        # Market stress analysis
        market_stress_index = self._calculate_market_stress(market_data)
        
        # Multi-dimensional threat calculation
        base_threat = (critical_items * 4) + (high_items * 2)
        market_threat = market_stress_index * 1.5
        sentiment_threat = abs(avg_sentiment) * 2
        
        overall_threat = min(10, (base_threat + market_threat + sentiment_threat) / 3)
        
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
        confidence_score = min(100, (total_sources * 2) + (avg_intelligence_quality * 8) + (source_diversity * 3))
        
        return {
            'overall_threat_score': overall_threat,
            'threat_level': threat_level,
            'intelligence_quality': avg_intelligence_quality,
            'total_sources': total_sources,
            'critical_items': critical_items,
            'high_items': high_items,
            'avg_sentiment': avg_sentiment,
            'market_stress_index': market_stress_index,
            'source_diversity': source_diversity,
            'confidence_score': confidence_score,
            'timestamp': datetime.now()
        }
    
    def _calculate_market_stress(self, market_data):
        """Calculate comprehensive market stress index"""
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
            else:
                stress_indicators.append(3)
        
        # Defense sector performance
        defense_items = [item for item in market_data if item['category'] == 'Defense']
        if defense_items:
            defense_performance = np.mean([item['change_pct'] for item in defense_items])
            if defense_performance > 3:
                stress_indicators.append(6)
            else:
                stress_indicators.append(2)
        
        return np.mean(stress_indicators) if stress_indicators else 0
    
    def _baseline_assessment(self):
        """Baseline assessment when no data is available"""
        return {
            'overall_threat_score': 0,
            'threat_level': 'NORMAL',
            'intelligence_quality': 0,
            'total_sources': 0,
            'critical_items': 0,
            'high_items': 0,
            'avg_sentiment': 0,
            'market_stress_index': 0,
            'source_diversity': 0,
            'confidence_score': 0,
            'timestamp': datetime.now()
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

def create_global_intelligence_map(hotspots):
    """Create comprehensive global intelligence map"""
    
    # Initialize map centered on global view
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='CartoDB positron'
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
    
    return m

def create_market_analysis_dashboard(market_data):
    """Create comprehensive market intelligence dashboard"""
    
    if not market_data:
        return None
    
    df = pd.DataFrame(market_data)
    
    # Market performance by category
    fig = px.bar(
        df.groupby('category').agg({
            'change_pct': 'mean'
        }).reset_index(),
        x='category',
        y='change_pct',
        title="Market Performance by Sector",
        color='change_pct',
        color_continuous_scale=['#DC2626', '#FFFFFF', '#059669']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#0A0E27', 'family': 'Inter'},
        height=400,
        xaxis_title="Sector",
        yaxis_title="Average Change %"
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
    
    # Initialize analytics engine
    analytics_engine = StrategicAnalyticsEngine()
    
    # Data collection phase
    st.markdown('<div class="section-header">INTELLIGENCE COLLECTION STATUS</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        # Collect intelligence sources
        all_intelligence = []
        market_data = []
        
        with col1:
            with st.spinner("Collecting comprehensive intelligence..."):
                news_intel = fetch_comprehensive_intelligence()
                all_intelligence.extend(news_intel)
            
            st.markdown(f"""
            <div class="intelligence-card">
                <div class="metric-value">{len(all_intelligence)}</div>
                <div class="metric-label">NEWS SOURCES</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.spinner("Analyzing market intelligence..."):
                market_data = fetch_market_intelligence()
            
            st.markdown(f"""
            <div class="intelligence-card">
                <div class="metric-value">{len(market_data)}</div>
                <div class="metric-label">MARKET ASSETS</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="intelligence-card">
                <div class="metric-value">{len(GLOBAL_INTELLIGENCE_HOTSPOTS)}</div>
                <div class="metric-label">HOTSPOTS</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Generate executive assessment
    assessment = analytics_engine.generate_executive_assessment(all_intelligence, market_data)
    
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
            <p><strong>Last Updated:</strong> {assessment['timestamp'].strftime('%H:%M:%S UTC')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Market analysis
        market_fig = create_market_analysis_dashboard(market_data)
        if market_fig:
            st.plotly_chart(market_fig, use_container_width=True)
        else:
            st.info("Market analysis will display when data is available")
    
    # Main intelligence tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "GLOBAL INTELLIGENCE", 
        "MARKET ANALYSIS", 
        "INTELLIGENCE FEED", 
        "EXECUTIVE REPORTS"
    ])
    
    with tab1:
        st.markdown("### GLOBAL INTELLIGENCE MAP")
        
        # Interactive global map
        intel_map = create_global_intelligence_map(GLOBAL_INTELLIGENCE_HOTSPOTS)
        map_data = st_folium(intel_map, width=700, height=600)
        
        # Hotspot analysis
        st.markdown("### STRATEGIC HOTSPOTS")
        
        for location, data in GLOBAL_INTELLIGENCE_HOTSPOTS.items():
            priority_class = f"priority-{data['priority'].lower()}"
            st.markdown(f"""
            <div class="intelligence-item {priority_class}">
                <h5>{location}</h5>
                <p><strong>Priority:</strong> {data['priority']}</p>
                <p><strong>Region:</strong> {data['region']}</p>
                <p><strong>Type:</strong> {data['type']}</p>
                <p><strong>Coordinates:</strong> {data['lat']:.4f}, {data['lon']:.4f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### MARKET INTELLIGENCE ANALYSIS")
        
        if market_data:
            # Market stress indicators
            st.markdown("### MARKET STRESS INDICATORS")
            
            high_stress_assets = [asset for asset in market_data if asset['stress_level'] in ['CRITICAL', 'HIGH']]
            
            if high_stress_assets:
                for asset in high_stress_assets:
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
        
        # Filter intelligence data
        filtered_intelligence = sorted(all_intelligence, key=lambda x: x.get('intelligence_score', 0), reverse=True)[:50]
        
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
                
                for item in priority_groups[priority][:10]:  # Limit display
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
                            <a href="{item.get('url', '#')}" target="_blank" style="color: #3B82F6; text-decoration: none; font-weight: 600;">
                                VIEW SOURCE
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### EXECUTIVE REPORTS")
        
        # Executive summary generation
        col1, col2 = st.columns(2)
        
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
                    'source_breakdown': {
                        'news_intelligence': len(all_intelligence),
                        'market_intelligence': len(market_data)
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
            if st.button("EXPORT THREAT BRIEFING"):
                threat_briefing = f"""
STRATEGIC INTELLIGENCE THREAT BRIEFING
======================================

CLASSIFICATION: INTERNAL USE ONLY
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

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

TOP PRIORITY INTELLIGENCE ITEMS
--------------------------------
"""
                
                critical_items = [item for item in all_intelligence if item.get('priority') == 'CRITICAL'][:5]
                
                for item in critical_items:
                    threat_briefing += f"""
CRITICAL: {item['title'][:100]}...
Source: {item['source']}
Region: {item.get('region', 'Global')}
Score: {item.get('intelligence_score', 0):.1f}/10
URL: {item.get('url', 'N/A')}

"""
                
                threat_briefing += """
END OF BRIEFING
===============
"""
                
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
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
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

if __name__ == "__main__":
    main()
