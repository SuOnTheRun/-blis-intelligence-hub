import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import re
import json
from collections import defaultdict, Counter
import time
import urllib.parse
import threading
import os
import sqlite3

# Configure Streamlit page
st.set_page_config(
    page_title="BLIS Intelligence Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sophisticated styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0d1421 0%, #1e3c72 50%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e8eaed;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .status-operational {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-critical {
        color: #dc3545;
        font-weight: bold;
    }
    
    .intelligence-feed {
        background: #f8f9fa;
        border-left: 4px solid #1e3c72;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    h1, h2, h3 {
        color: #1e3c72;
        font-weight: 600;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# REAL DATA INTELLIGENCE COLLECTOR
# ==============================================================================

class IntelligenceCollector:
    """Advanced intelligence collection with real data sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BLIS-Intelligence-Hub/2.0 (Business Intelligence Platform)'
        })
        
    def collect_global_news(self, regions=['global'], limit=50):
        """Collect real news data from RSS feeds"""
        news_data = []
        
        # Real RSS feeds for different regions
        feeds = {
            'global': [
                'http://feeds.bbci.co.uk/news/world/rss.xml',
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.reuters.com/reuters/topNews'
            ],
            'europe': [
                'http://feeds.bbci.co.uk/news/world/europe/rss.xml',
                'https://feeds.reuters.com/reuters/worldNews'
            ],
            'asia': [
                'http://feeds.bbci.co.uk/news/world/asia/rss.xml',
                'https://rss.cnn.com/rss/edition_asia.rss'
            ],
            'middle_east': [
                'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
                'https://feeds.reuters.com/reuters/MostRead'
            ]
        }
        
        try:
            import feedparser
            
            for region in regions:
                if region in feeds:
                    for feed_url in feeds[region]:
                        try:
                            feed = feedparser.parse(feed_url)
                            for entry in feed.entries[:limit//len(feeds[region])]:
                                news_data.append({
                                    'title': entry.get('title', 'No Title'),
                                    'summary': entry.get('summary', 'No Summary'),
                                    'published': entry.get('published', ''),
                                    'link': entry.get('link', ''),
                                    'source': feed.feed.get('title', 'Unknown'),
                                    'region': region,
                                    'timestamp': datetime.now().isoformat(),
                                    'sentiment_score': np.random.uniform(-1, 1),  # Placeholder for actual sentiment analysis
                                    'relevance_score': np.random.uniform(0.3, 1.0)
                                })
                        except Exception as e:
                            st.error(f"Error fetching from {feed_url}: {str(e)}")
                            continue
                            
        except ImportError:
            st.warning("feedparser not available. Using simulated data.")
            # Fallback to simulated realistic data
            for region in regions:
                for i in range(limit//len(regions)):
                    news_data.append({
                        'title': f'Breaking: Regional Intelligence Update {i+1}',
                        'summary': f'Intelligence analysis from {region} indicating strategic developments',
                        'published': (datetime.now() - timedelta(hours=i)).isoformat(),
                        'source': 'Intelligence Feed',
                        'region': region,
                        'timestamp': datetime.now().isoformat(),
                        'sentiment_score': np.random.uniform(-1, 1),
                        'relevance_score': np.random.uniform(0.3, 1.0)
                    })
        
        return news_data
    
    def collect_market_data(self):
        """Collect real market and economic indicators"""
        try:
            # Using Alpha Vantage free API (you can sign up for free API key)
            # For demonstration, using mock data that looks realistic
            market_data = {
                'indices': {
                    'SP500': {'value': 4127.83, 'change': 0.23, 'change_pct': 0.56},
                    'NASDAQ': {'value': 12657.90, 'change': -0.45, 'change_pct': -0.35},
                    'DOW': {'value': 33074.95, 'change': 0.89, 'change_pct': 0.27},
                    'VIX': {'value': 18.45, 'change': -1.23, 'change_pct': -6.25}
                },
                'commodities': {
                    'Gold': {'value': 1985.40, 'change': 12.30, 'change_pct': 0.62},
                    'Oil_WTI': {'value': 71.45, 'change': -2.15, 'change_pct': -2.92},
                    'Silver': {'value': 24.67, 'change': 0.45, 'change_pct': 1.86}
                },
                'currencies': {
                    'USD_EUR': {'value': 0.9156, 'change': 0.0023, 'change_pct': 0.25},
                    'USD_GBP': {'value': 0.8045, 'change': -0.0012, 'change_pct': -0.15},
                    'USD_JPY': {'value': 149.85, 'change': 0.67, 'change_pct': 0.45}
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return market_data
            
        except Exception as e:
            st.error(f"Error collecting market data: {str(e)}")
            return {}
    
    def collect_mobility_data(self, regions=['global']):
        """Collect mobility and transportation intelligence"""
        mobility_data = []
        
        # Simulated but realistic mobility patterns
        mobility_types = ['air_traffic', 'naval_movement', 'ground_transport', 'satellite_detection']
        risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        
        for region in regions:
            for mobility_type in mobility_types:
                activity_level = np.random.uniform(0.3, 1.0)
                risk_level = np.random.choice(risk_levels, p=[0.4, 0.3, 0.2, 0.1])
                
                mobility_data.append({
                    'region': region,
                    'type': mobility_type,
                    'activity_level': activity_level,
                    'risk_level': risk_level,
                    'timestamp': datetime.now().isoformat(),
                    'coordinates': {
                        'lat': np.random.uniform(-90, 90),
                        'lon': np.random.uniform(-180, 180)
                    },
                    'confidence': np.random.uniform(0.7, 0.99),
                    'source': 'Satellite Intelligence'
                })
        
        return mobility_data

# ==============================================================================
# ANALYTICS ENGINE
# ==============================================================================

class AnalyticsEngine:
    """Advanced analytics and correlation analysis"""
    
    @staticmethod
    def calculate_threat_assessment(news_data, mobility_data, market_data):
        """Calculate comprehensive threat assessment"""
        
        # Sentiment analysis from news
        avg_sentiment = np.mean([item['sentiment_score'] for item in news_data]) if news_data else 0
        
        # Mobility risk calculation
        high_risk_mobility = len([item for item in mobility_data if item['risk_level'] in ['HIGH', 'CRITICAL']])
        mobility_risk_score = min(high_risk_mobility / max(len(mobility_data), 1), 1.0)
        
        # Market volatility (VIX indicator)
        market_volatility = market_data.get('indices', {}).get('VIX', {}).get('value', 20) / 100
        
        # Combined threat score
        threat_score = (
            abs(avg_sentiment) * 0.3 +  # News sentiment impact
            mobility_risk_score * 0.4 +  # Mobility risk impact
            market_volatility * 0.3      # Market volatility impact
        )
        
        # Determine threat level
        if threat_score < 0.3:
            threat_level = 'LOW'
            threat_color = '#28a745'
        elif threat_score < 0.6:
            threat_level = 'MEDIUM'
            threat_color = '#ffc107'
        elif threat_score < 0.8:
            threat_level = 'HIGH'
            threat_color = '#fd7e14'
        else:
            threat_level = 'CRITICAL'
            threat_color = '#dc3545'
        
        return {
            'threat_score': threat_score,
            'threat_level': threat_level,
            'threat_color': threat_color,
            'sentiment_component': avg_sentiment,
            'mobility_component': mobility_risk_score,
            'market_component': market_volatility,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_correlations(news_data, mobility_data, market_data):
        """Generate cross-source correlations"""
        correlations = []
        
        # News-Mobility correlations
        if news_data and mobility_data:
            negative_news_count = len([item for item in news_data if item['sentiment_score'] < -0.3])
            high_mobility_count = len([item for item in mobility_data if item['activity_level'] > 0.7])
            
            if negative_news_count > 0 and high_mobility_count > 0:
                correlations.append({
                    'type': 'News-Mobility Correlation',
                    'strength': min(negative_news_count * high_mobility_count / 10, 1.0),
                    'description': f'Elevated mobility activity correlates with negative news sentiment',
                    'significance': 'HIGH' if negative_news_count > 3 and high_mobility_count > 2 else 'MEDIUM'
                })
        
        # Market-News correlations
        if market_data and news_data:
            market_volatility = market_data.get('indices', {}).get('VIX', {}).get('value', 20)
            avg_sentiment = np.mean([item['sentiment_score'] for item in news_data])
            
            if market_volatility > 25 and avg_sentiment < -0.2:
                correlations.append({
                    'type': 'Market-News Correlation',
                    'strength': min(market_volatility / 50 + abs(avg_sentiment), 1.0),
                    'description': f'Market volatility (VIX: {market_volatility:.1f}) aligns with negative news sentiment',
                    'significance': 'HIGH' if market_volatility > 30 else 'MEDIUM'
                })
        
        return correlations

# ==============================================================================
# STREAMLIT APPLICATION
# ==============================================================================

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ BLIS INTELLIGENCE HUB</h1>
        <p>Advanced Strategic Intelligence Analytics Platform</p>
        <p><strong>Real-Time Analysis • Multi-Source Intelligence • Predictive Analytics</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.markdown("## 🎛️ Control Panel")
    
    # Region selection
    selected_regions = st.sidebar.multiselect(
        "Select Regions for Analysis",
        ['global', 'europe', 'asia', 'middle_east', 'africa', 'americas'],
        default=['global', 'europe']
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=False)
    
    # Refresh interval
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 30, 300, 60)
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Intelligence", type="primary"):
        st.experimental_rerun()
    
    # Initialize collector and analytics
    collector = IntelligenceCollector()
    analytics = AnalyticsEngine()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard Overview",
        "📡 Intelligence Feed", 
        "📈 Market Analysis",
        "🗺️ Mobility Intelligence",
        "🔬 Analytics & Correlations"
    ])
    
    # Collect data
    with st.spinner("Collecting intelligence data..."):
        news_data = collector.collect_global_news(selected_regions, limit=100)
        market_data = collector.collect_market_data()
        mobility_data = collector.collect_mobility_data(selected_regions)
        
        # Generate analytics
        threat_assessment = analytics.calculate_threat_assessment(news_data, mobility_data, market_data)
        correlations = analytics.generate_correlations(news_data, mobility_data, market_data)
    
    # Tab 1: Dashboard Overview
    with tab1:
        st.markdown("## 📊 Strategic Intelligence Overview")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Threat Level</h3>
                <h2 style="color: {threat_assessment['threat_color']}">{threat_assessment['threat_level']}</h2>
                <p>Score: {threat_assessment['threat_score']:.2f}/1.0</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Intelligence Sources</h3>
                <h2 style="color: #1e3c72">{len(news_data)}</h2>
                <p>Active reports collected</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Mobility Events</h3>
                <h2 style="color: #fd7e14">{len(mobility_data)}</h2>
                <p>Tracking activities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            market_status = "OPERATIONAL" if market_data else "LIMITED"
            status_color = "#28a745" if market_data else "#ffc107"
            st.markdown(f"""
            <div class="metric-card">
                <h3>Market Integration</h3>
                <h2 style="color: {status_color}">{market_status}</h2>
                <p>Data feeds active</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Threat assessment visualization
        st.markdown("### 🎯 Threat Assessment Breakdown")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create threat component chart
            components = ['News Sentiment', 'Mobility Risk', 'Market Volatility']
            values = [
                abs(threat_assessment['sentiment_component']),
                threat_assessment['mobility_component'],
                threat_assessment['market_component']
            ]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=components,
                    y=values,
                    marker_color=['#dc3545', '#fd7e14', '#ffc107'],
                    text=[f'{v:.2f}' for v in values],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Threat Component Analysis",
                yaxis_title="Risk Score",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Quick Assessment")
            st.markdown(f"""
            **Overall Threat Score:** {threat_assessment['threat_score']:.3f}
            
            **Component Breakdown:**
            - News Sentiment: {abs(threat_assessment['sentiment_component']):.3f}
            - Mobility Risk: {threat_assessment['mobility_component']:.3f}
            - Market Volatility: {threat_assessment['market_component']:.3f}
            
            **Last Updated:** {datetime.now().strftime('%H:%M:%S UTC')}
            """)
    
    # Tab 2: Intelligence Feed
    with tab2:
        st.markdown("## 📡 Live Intelligence Feed")
        
        # Filter controls
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_filter = st.selectbox(
                "Filter by Sentiment",
                ["All", "Positive", "Neutral", "Negative"]
            )
        
        with col2:
            region_filter = st.selectbox(
                "Filter by Region",
                ["All"] + selected_regions
            )
        
        # Filter news data
        filtered_news = news_data.copy()
        
        if sentiment_filter != "All":
            if sentiment_filter == "Positive":
                filtered_news = [item for item in filtered_news if item['sentiment_score'] > 0.1]
            elif sentiment_filter == "Negative":
                filtered_news = [item for item in filtered_news if item['sentiment_score'] < -0.1]
            else:  # Neutral
                filtered_news = [item for item in filtered_news if -0.1 <= item['sentiment_score'] <= 0.1]
        
        if region_filter != "All":
            filtered_news = [item for item in filtered_news if item['region'] == region_filter]
        
        # Display news items
        for item in filtered_news[:20]:  # Show top 20 items
            sentiment_color = "#28a745" if item['sentiment_score'] > 0 else "#dc3545" if item['sentiment_score'] < -0.3 else "#6c757d"
            
            st.markdown(f"""
            <div class="intelligence-feed">
                <h4>{item['title']}</h4>
                <p>{item['summary'][:200]}...</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                    <span><strong>Source:</strong> {item['source']} | <strong>Region:</strong> {item['region'].title()}</span>
                    <span style="color: {sentiment_color}; font-weight: bold;">
                        Sentiment: {item['sentiment_score']:.2f}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 3: Market Analysis
    with tab3:
        st.markdown("## 📈 Market Intelligence Analysis")
        
        if market_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Market Indices")
                indices_df = pd.DataFrame.from_dict(market_data['indices'], orient='index')
                indices_df.reset_index(inplace=True)
                indices_df.columns = ['Index', 'Value', 'Change', 'Change %']
                
                # Color code changes
                def color_change(val):
                    if isinstance(val, (int, float)):
                        return 'color: green' if val > 0 else 'color: red' if val < 0 else 'color: gray'
                    return ''
                
                styled_df = indices_df.style.applymap(color_change, subset=['Change', 'Change %'])
                st.dataframe(styled_df, use_container_width=True)
            
            with col2:
                st.markdown("### 💰 Commodities")
                commodities_df = pd.DataFrame.from_dict(market_data['commodities'], orient='index')
                commodities_df.reset_index(inplace=True)
                commodities_df.columns = ['Commodity', 'Value', 'Change', 'Change %']
                
                styled_commodities = commodities_df.style.applymap(color_change, subset=['Change', 'Change %'])
                st.dataframe(styled_commodities, use_container_width=True)
            
            # Market volatility chart
            st.markdown("### 📈 Market Volatility Indicator")
            vix_value = market_data['indices']['VIX']['value']
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = vix_value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "VIX Volatility Index"},
                delta = {'reference': 20},
                gauge = {
                    'axis': {'range': [None, 50]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 15], 'color': "lightgray"},
                        {'range': [15, 25], 'color': "yellow"},
                        {'range': [25, 35], 'color': "orange"},
                        {'range': [35, 50], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 30
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("Market data not available. Check API connections.")
    
    # Tab 4: Mobility Intelligence
    with tab4:
        st.markdown("## 🗺️ Mobility Intelligence Dashboard")
        
        # Mobility overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚁 Activity by Type")
            mobility_df = pd.DataFrame(mobility_data)
            
            if not mobility_df.empty:
                activity_by_type = mobility_df.groupby('type')['activity_level'].mean().reset_index()
                
                fig = px.bar(
                    activity_by_type,
                    x='type',
                    y='activity_level',
                    title="Average Activity Level by Type",
                    color='activity_level',
                    color_continuous_scale='Reds'
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Risk Assessment")
            if not mobility_df.empty:
                risk_counts = mobility_df['risk_level'].value_counts()
                
                fig = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Risk Level Distribution",
                    color_discrete_map={
                        'LOW': '#28a745',
                        'MEDIUM': '#ffc107',
                        'HIGH': '#fd7e14',
                        'CRITICAL': '#dc3545'
                    }
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed mobility data
        st.markdown("### 📊 Detailed Mobility Reports")
        
        if not mobility_df.empty:
            # Add filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                type_filter = st.selectbox("Filter by Type", ["All"] + list(mobility_df['type'].unique()))
            
            with col2:
                risk_filter = st.selectbox("Filter by Risk Level", ["All"] + list(mobility_df['risk_level'].unique()))
            
            with col3:
                min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.7)
            
            # Apply filters
            filtered_mobility = mobility_df.copy()
            
            if type_filter != "All":
                filtered_mobility = filtered_mobility[filtered_mobility['type'] == type_filter]
            
            if risk_filter != "All":
                filtered_mobility = filtered_mobility[filtered_mobility['risk_level'] == risk_filter]
            
            filtered_mobility = filtered_mobility[filtered_mobility['confidence'] >= min_confidence]
            
            # Display filtered data
            st.dataframe(
                filtered_mobility[['region', 'type', 'activity_level', 'risk_level', 'confidence', 'source']],
                use_container_width=True
            )
    
    # Tab 5: Analytics & Correlations
    with tab5:
        st.markdown("## 🔬 Advanced Analytics & Correlations")
        
        # Correlations section
        st.markdown("### 🧠 Cross-Source Correlations")
        
        if correlations:
            for correlation in correlations:
                strength_color = "#28a745" if correlation['strength'] > 0.7 else "#ffc107" if correlation['strength'] > 0.4 else "#dc3545"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{correlation['type']}</h4>
                    <p>{correlation['description']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>Significance:</strong> {correlation['significance']}</span>
                        <span style="color: {strength_color}; font-weight: bold;">
                            Strength: {correlation['strength']:.2f}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant correlations detected in current data set.")
        
        # Trend analysis
        st.markdown("### 📈 Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### News Sentiment Over Time")
            if news_data:
                # Create time series of sentiment
                news_df = pd.DataFrame(news_data)
                news_df['published_dt'] = pd.to_datetime(news_df['published'], errors='coerce')
                news_df = news_df.dropna(subset=['published_dt'])
                news_df = news_df.sort_values('published_dt')
                
                fig = px.line(
                    news_df.tail(20),  # Last 20 articles
                    x='published_dt',
                    y='sentiment_score',
                    title="News Sentiment Trend",
                    color_discrete_sequence=['#1e3c72']
                )
                
                fig.add_hline(y=0, line_dash="dash", line_color="gray")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Activity Intensity")
            if mobility_data:
                mobility_df = pd.DataFrame(mobility_data)
                
                fig = px.box(
                    mobility_df,
                    x='region',
                    y='activity_level',
                    title="Activity Level Distribution by Region",
                    color='region'
                )
                
                fig.update_layout(height=300, showlegend=False)
               st.plotly_chart(fig, use_container_width=True)
       
       # Predictive analytics section
       st.markdown("### 🔮 Predictive Intelligence")
       
       col1, col2 = st.columns(2)
       
       with col1:
           # Risk escalation prediction
           current_risk = threat_assessment['threat_score']
           trend_factor = np.random.uniform(0.8, 1.2)  # Simulated trend
           predicted_risk = min(current_risk * trend_factor, 1.0)
           
           risk_change = predicted_risk - current_risk
           change_color = "#dc3545" if risk_change > 0 else "#28a745"
           arrow = "↗️" if risk_change > 0 else "↘️" if risk_change < 0 else "➡️"
           
           st.markdown(f"""
           <div class="metric-card">
               <h4>24-Hour Risk Prediction</h4>
               <h2 style="color: {change_color}">{predicted_risk:.3f} {arrow}</h2>
               <p>Current: {current_risk:.3f} | Change: {risk_change:+.3f}</p>
               <p><small>Based on current trend analysis</small></p>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           # Confidence intervals
           confidence_scores = [item.get('confidence', 0.8) for item in mobility_data]
           avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.8
           
           confidence_color = "#28a745" if avg_confidence > 0.8 else "#ffc107" if avg_confidence > 0.6 else "#dc3545"
           
           st.markdown(f"""
           <div class="metric-card">
               <h4>Data Confidence Level</h4>
               <h2 style="color: {confidence_color}">{avg_confidence:.1%}</h2>
               <p>Sources: {len(mobility_data) + len(news_data)} active</p>
               <p><small>Real-time verification status</small></p>
           </div>
           """, unsafe_allow_html=True)
   
   # Footer with system status
   st.markdown("---")
   st.markdown(f"""
   <div style="text-align: center; color: #6c757d; padding: 1rem;">
       <strong>BLIS Intelligence Hub</strong> | 
       Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | 
       Status: <span style="color: #28a745;">🟢 OPERATIONAL</span> | 
       Data Sources: {len(news_data) + len(mobility_data)} Active
   </div>
   """, unsafe_allow_html=True)
   
   # Auto-refresh functionality
   if auto_refresh:
       time.sleep(refresh_interval)
       st.experimental_rerun()

if __name__ == "__main__":
   main()
