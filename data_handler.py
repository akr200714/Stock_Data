"""
Data Handler Module - Manages stock data input and preprocessing
Supports: Breeze Connect (real-time), CSV files
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from config import BREEZE_API_KEY, BREEZE_SECRET_KEY, BREEZE_SESSION_KEY, BREEZE_USE_PRODUCTION


class BreezeConnectDataHandler:
    """Handles real-time stock data from Breeze Connect API"""
    
    def __init__(self, symbol: str, lookback_days: int = 365):
        """
        Initialize Breeze Connect data handler
        
        Args:
            symbol: Stock ticker symbol (NSE format, e.g., 'SBIN-EQ')
            lookback_days: Number of days of historical data to fetch
        """
        self.symbol = symbol.upper()
        self.lookback_days = lookback_days
        self.df = None
        self.raw_df = None
        self.session_key = BREEZE_SESSION_KEY
        
        try:
            from breeze_connect import BreezeConnect
            self.breeze = BreezeConnect(api_key=BREEZE_API_KEY)
        except ImportError:
            raise ImportError("breeze-connect not installed. Run: pip install breeze-connect")
        except Exception as e:
            raise Exception(f"Failed to initialize Breeze Connect: {str(e)}")
    
    def login(self, api_secret: str) -> bool:
        """
        Authenticate with Breeze Connect
        
        Args:
            api_secret: Breeze API secret key
        
        Returns:
            True if login successful
        """
        try:
            response = self.breeze.generate_session(
                api_secret=api_secret,
                secret_key=BREEZE_SECRET_KEY
            )
            self.session_key = response
            print(f"✓ Breeze Connect authenticated successfully")
            return True
        except Exception as e:
            print(f"✗ Breeze authentication failed: {str(e)}")
            return False
    
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical stock data from Breeze Connect
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            if not self.session_key:
                raise ValueError("Not authenticated. Call login() first.")
            
            print(f"Fetching data for {self.symbol} from Breeze Connect...")
            
            # Convert symbol to Breeze format if needed (e.g., AAPL -> AAPL-EQ)
            breeze_symbol = self._convert_to_breeze_format(self.symbol)
            
            # Fetch historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days)
            
            # Use Breeze historical data endpoint
            response = self.breeze.get_historical_data(
                stock_token=breeze_symbol,
                interval='1d',  # Daily candles
                from_date=start_date.strftime('%Y-%m-%d'),
                to_date=end_date.strftime('%Y-%m-%d')
            )
            
            if not response or 'success' not in response or not response['success']:
                raise Exception(f"Failed to fetch data: {response}")
            
            # Convert to DataFrame
            self.raw_df = pd.DataFrame(response['data'])
            self.df = self.raw_df.copy()
            
            self._preprocess_data()
            print(f"✓ Successfully fetched {len(self.df)} candles for {self.symbol}")
            return self.df
        
        except Exception as e:
            print(f"✗ Error fetching data: {str(e)}")
            raise
    
    def fetch_realtime(self, symbol: str = None) -> Dict:
        """
        Fetch real-time quote for a symbol
        
        Args:
            symbol: Stock symbol (uses initialized symbol if None)
        
        Returns:
            Dict with real-time data (LTP, bid, ask, volume, etc.)
        """
        try:
            if not self.session_key:
                raise ValueError("Not authenticated. Call login() first.")
            
            target_symbol = symbol or self.symbol
            breeze_symbol = self._convert_to_breeze_format(target_symbol)
            
            response = self.breeze.get_quotes(
                stock_token=breeze_symbol
            )
            
            if response and 'success' in response and response['success']:
                data = response['data'][0] if isinstance(response['data'], list) else response['data']
                return {
                    'symbol': target_symbol,
                    'ltp': float(data.get('ltp', 0)),
                    'bid': float(data.get('bid', 0)),
                    'ask': float(data.get('ask', 0)),
                    'volume': int(data.get('volume', 0)),
                    'timestamp': data.get('timestamp'),
                    'open': float(data.get('open', 0)),
                    'high': float(data.get('high', 0)),
                    'low': float(data.get('low', 0)),
                    'close': float(data.get('close', 0))
                }
            else:
                raise Exception(f"Failed to fetch quote: {response}")
        
        except Exception as e:
            print(f"✗ Error fetching real-time data: {str(e)}")
            return None
    
    def _preprocess_data(self):
        """Preprocess data: handle missing values, ensure proper columns"""
        # Standardize column names
        column_mapping = {
            'date': 'timestamp',
            'Date': 'timestamp',
            'open': 'open',
            'Open': 'open',
            'high': 'high',
            'High': 'high',
            'low': 'low',
            'Low': 'low',
            'close': 'close',
            'Close': 'close',
            'volume': 'volume',
            'Volume': 'volume'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in self.df.columns:
                self.df.rename(columns={old_name: new_name}, inplace=True)
        
        # Fill missing values
        self.df = self.df.fillna(method='ffill').fillna(method='bfill')
        
        # Ensure we have required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Set timestamp as index
        if 'timestamp' in self.df.columns:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            self.df.set_index('timestamp', inplace=True)
        elif not isinstance(self.df.index, pd.DatetimeIndex):
            self.df.index = pd.to_datetime(self.df.index)
        
        # Sort by date
        self.df = self.df.sort_index()
    
    def _convert_to_breeze_format(self, symbol: str) -> str:
        """Convert symbol to Breeze format (e.g., AAPL -> AAPL-EQ for NSE stocks)"""
        # If already in Breeze format, return as-is
        if '-' in symbol:
            return symbol
        
        # Indian stocks use -EQ suffix for NSE, -BE for BSE
        # Adjust based on your stock exchange
        return f"{symbol}-EQ"
    
    def get_current_price(self) -> float:
        """Get the current/latest price"""
        if self.df is None or self.df.empty:
            # Try to fetch real-time price
            rt_data = self.fetch_realtime()
            if rt_data:
                return rt_data['ltp']
            raise ValueError("No data loaded. Call fetch_data() first.")
        return float(self.df['close'].iloc[-1])
    
    def get_data(self) -> pd.DataFrame:
        """Get the processed dataframe"""
        if self.df is None:
            self.fetch_data()
        return self.df.copy()
    
    def get_ohlcv(self, lookback: int = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Get OHLCV data as separate arrays"""
        if self.df is None:
            self.fetch_data()
        
        data = self.df.iloc[-lookback:] if lookback else self.df
        
        return (
            data['open'].values,
            data['high'].values,
            data['low'].values,
            data['close'].values,
            data['volume'].values
        )


class StockDataHandler:
    """Legacy interface - now uses Breeze Connect (can fallback to CSV)"""
    
    def __init__(self, symbol: str, period: str = "1y", interval: str = "1d"):
        """
        Initialize data handler
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (kept for compatibility, Breeze calculates from lookback_days)
            interval: Data interval (kept for compatibility)
        """
        self.symbol = symbol.upper()
        self.period = period
        self.interval = interval
        self.handler = None
        self.df = None
        
        # Calculate lookback days from period
        lookback_map = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825, '10y': 3650
        }
        self.lookback_days = lookback_map.get(period, 365)
        
        # Try Breeze Connect first
        try:
            self.handler = BreezeConnectDataHandler(symbol, self.lookback_days)
            self.use_breeze = True
        except Exception as e:
            print(f"⚠️  Breeze Connect initialization failed: {str(e)}")
            print("   Install breeze-connect: pip install breeze-connect")
            print("   Add BREEZE_API_KEY to .env file")
            self.use_breeze = False
    
    def fetch_data(self) -> pd.DataFrame:
        """Fetch data using configured handler"""
        if self.use_breeze and self.handler:
            try:
                self.df = self.handler.fetch_data()
                return self.df
            except Exception as e:
                print(f"Error with Breeze Connect: {str(e)}")
                print("Please ensure you've authenticated with Breeze Connect")
                raise
        else:
            raise Exception("No data handler available. Configure Breeze Connect credentials in .env")
    
    def get_current_price(self) -> float:
        """Get current price"""
        if self.use_breeze and self.handler:
            return self.handler.get_current_price()
        raise ValueError("Handler not initialized")
    
    def get_data(self) -> pd.DataFrame:
        """Get processed data"""
        if self.df is None:
            self.fetch_data()
        return self.df.copy()
    
    def get_ohlcv(self, lookback: int = None):
        """Get OHLCV arrays"""
        if self.use_breeze and self.handler:
            return self.handler.get_ohlcv(lookback)
        raise ValueError("Handler not initialized")


class CSVDataHandler:
    """Handle data from CSV files"""
    
    def __init__(self, csv_path: str):
        """
        Initialize with CSV file
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = csv_path
        self.symbol = "CSV_DATA"
        self.df = None
    
    def fetch_data(self) -> pd.DataFrame:
        """Load data from CSV"""
        try:
            print(f"Loading data from {self.csv_path}...")
            self.df = pd.read_csv(self.csv_path)
            
            # Try to parse date column
            date_cols = [col for col in self.df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                self.df[date_cols[0]] = pd.to_datetime(self.df[date_cols[0]])
                self.df.set_index(date_cols[0], inplace=True)
            
            self._preprocess_data()
            print(f"✓ Successfully loaded {len(self.df)} rows from CSV")
            return self.df
        
        except Exception as e:
            print(f"✗ Error loading CSV: {str(e)}")
            raise
    
    def _preprocess_data(self):
        """Preprocess CSV data"""
        self.df.columns = [col.lower() for col in self.df.columns]
        self.df = self.df.fillna(method='ffill').fillna(method='bfill')
        
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
    
    def get_data(self) -> pd.DataFrame:
        """Get data"""
        if self.df is None:
            self.fetch_data()
        return self.df.copy()


# Example usage
if __name__ == "__main__":
    # Using Breeze Connect (requires authentication)
    print("Breeze Connect Data Handler - Setup Required")
    print("=" * 60)
    print("\n1. Get API credentials from Angel Broking:")
    print("   https://www.angelbroking.com/breeze/")
    print("\n2. Add to .env file:")
    print("   BREEZE_API_KEY=your-key")
    print("   BREEZE_SECRET_KEY=your-secret")
    print("\n3. Usage:")
    print("   handler = StockDataHandler('SBIN-EQ')")  # NSE format
    print("   df = handler.fetch_data()")
    print("\n4. For real-time data:")
    print("   breeze_handler = BreezeConnectDataHandler('SBIN-EQ')")
    print("   realtime = breeze_handler.fetch_realtime()")

