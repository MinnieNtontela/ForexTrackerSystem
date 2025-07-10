from datetime import datetime
import pandas as pd
import requests
import numpy as np

def get_forex_data(self, from_currency="EUR", to_currency="USD", interval="5min"):#Fetch real-time forex data
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': from_currency,
            'to_symbol': to_currency,
            'interval': interval,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()

            time_series_key = f"Time Series FX ({interval})"
            if time_series_key in data:
                df = pd.DataFrame(data[time_series_key]).T
                df.index = pd.to_datetime(df.index)
                df = df.astype(float)
                df.columns = ['open', 'high', 'low', 'close']
                return df.sort_index()
            else:
                print("Error fetching data:", data.get('Error Message', 'Unknown error'))
                return self.generate_sample_data()
                
        except Exception as e:
            print(f"API Error: {e}")
            return self.generate_sample_data()
        
def generate_sample_data(self):
    # Generate sample data for EUR/USD with realistic price movements
    dates = pd.date_range(start=datetime.now() - timedelta(days=5), 
                         end=datetime.now(), freq='5T')
    
    # Simulate realistic EUR/USD price movement
    np.random.seed(42)
    base_price = 1.0850
    price_changes = np.random.normal(0, 0.0005, len(dates))
    prices = base_price + np.cumsum(price_changes)
    prices = np.clip(prices, 1.0800, 1.0900)  # Keep prices within a realistic range
    data = []
    for i, price in enumerate(prices):
        high = price + abs(np.random.normal(0, 0.0003))
        low = price - abs(np.random.normal(0, 0.0003))
        open_price = prices[i-1] if i > 0 else price
        
        data.append({
            'open': open_price,
            'high': high,
            'low': low,
            'close': price
        })
    
    df = pd.DataFrame(data, index=dates)
    return df