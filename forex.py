from datetime import datetime
import pandas as pd

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
        
def generate_sample_data(self):#sample data for testing
    sample_data = {
        '2023-10-01 00:00:00': {'open': 1.1, 'high': 1.2, 'low': 1.0, 'close': 1.15},
        '2023-10-01 01:00:00': {'open': 1.15, 'high': 1.25, 'low': 1.05, 'close': 1.2},
        '2023-10-01 02:00:00': {'open': 1.2, 'high': 1.3, 'low': 1.15, 'close': 1.25},
    }
    df = pd.DataFrame(sample_data).T
    df.index = pd.to_datetime(df.index)
    return df.sort_index()
    
