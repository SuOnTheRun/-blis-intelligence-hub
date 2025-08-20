import sqlite3
import json
from datetime import datetime
import pandas as pd

class IntelligenceDatabase:
    """SQLite database for storing intelligence data"""
    
    def __init__(self, db_path="intelligence.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # News intelligence table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                summary TEXT,
                source TEXT,
                region TEXT,
                sentiment_score REAL,
                relevance_score REAL,
                timestamp DATETIME,
                raw_data TEXT
            )
        ''')
        
        # Mobility intelligence table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mobility_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT,
                type TEXT,
                activity_level REAL,
                risk_level TEXT,
                latitude REAL,
                longitude REAL,
                confidence REAL,
                source TEXT,
                timestamp DATETIME
            )
        ''')
        
        # Market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                price REAL,
                change_value REAL,
                change_percent REAL,
                volume INTEGER,
                data_type TEXT,
                timestamp DATETIME
            )
        ''')
        
        # Threat assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                threat_score REAL,
                threat_level TEXT,
                sentiment_component REAL,
                mobility_component REAL,
                market_component REAL,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_news_data(self, news_data):
        """Store news intelligence data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in news_data:
            cursor.execute('''
                INSERT INTO news_intelligence 
                (title, summary, source, region, sentiment_score, relevance_score, timestamp, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('title'),
                item.get('summary'),
                item.get('source'),
                item.get('region'),
                item.get('sentiment_score'),
                item.get('relevance_score'),
                item.get('timestamp'),
                json.dumps(item)
            ))
        
        conn.commit()
        conn.close()
    
    def get_historical_threat_levels(self, days=7):
        """Get historical threat assessment data"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT threat_score, threat_level, timestamp 
            FROM threat_assessments 
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_dict('records')
