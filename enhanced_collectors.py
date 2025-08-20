import yfinance as yf
import requests
from datetime import datetime, timedelta
import pandas as pd

class EnhancedDataCollector:
    """Enhanced real-time data collection"""
    
    def __init__(self):
        self.session = requests.Session()
        
    def get_real_stock_data(self, symbols=['SPY', 'QQQ', 'VIX', 'GLD']):
        """Get real stock market data using yfinance"""
        try:
            data = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d", interval="1m")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[0]
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100
                    
                    data[symbol] = {
                        'price': current_price,
                        'change': change,
                        'change_pct': change_pct,
                        'volume': hist['Volume'].iloc[-1],
                        'timestamp': datetime.now().isoformat()
                    }
            return data
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return {}
    
    def get_crypto_data(self, symbols=['BTC-USD', 'ETH-USD']):
        """Get cryptocurrency data"""
        try:
            # Using CoinGecko API (free)
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    'BTC': {
                        'price': data['bitcoin']['usd'],
                        'change_24h': data['bitcoin']['usd_24h_change']
                    },
                    'ETH': {
                        'price': data['ethereum']['usd'],
                        'change_24h': data['ethereum']['usd_24h_change']
                    }
                }
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return {}
    
    def get_satellite_data_firms(self):
        """Get real NASA FIRMS satellite data"""
        try:
            # NASA FIRMS API for fire/thermal anomalies
            api_key = "your_nasa_firms_api_key"  # Sign up at https://firms.modaps.eosdis.nasa.gov/api/
            
            # Get data for last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            today = datetime.now().strftime('%Y-%m-%d')
            
            url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/VIIRS_SNPP_NRT/UKR,RUS,ISR,PSE/{yesterday}"
            
            response = requests.get(url)
            if response.status_code == 200:
                # Parse CSV data
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                return df.to_dict('records')
        except Exception as e:
            print(f"Error fetching FIRMS data: {e}")
            return []
