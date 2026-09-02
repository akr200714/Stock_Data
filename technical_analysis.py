"""
Technical Analysis Module - Calculates technical indicators
"""
import numpy as np
import pandas as pd
from config import INDICATORS_CONFIG
from typing import Dict, Tuple


class TechnicalAnalyzer:
    """Calculates and manages technical indicators"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer with OHLCV data
        
        Args:
            df: DataFrame with OHLCV columns
        """
        self.df = df.copy()
        self.indicators = {}
        
    def calculate_all_indicators(self) -> Dict:
        """Calculate all technical indicators"""
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_atr()
        self.calculate_adx()
        self.calculate_stochastic()
        self.calculate_moving_averages()
        self.calculate_volume_indicators()
        
        return self.indicators
    
    def calculate_rsi(self, period: int = None) -> np.ndarray:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            period: RSI period
        
        Returns:
            RSI values array
        """
        period = period or INDICATORS_CONFIG["RSI_PERIOD"]
        close = self.df['close'].values
        
        deltas = np.diff(close)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = np.zeros_like(close)
        rsi[:period] = 100. - 100. / (1. + rs)
        
        for i in range(period, len(close)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            
            rs = up / down if down != 0 else 0
            rsi[i] = 100. - 100. / (1. + rs)
        
        self.indicators['RSI'] = rsi
        return rsi
    
    def calculate_macd(self, fast: int = None, slow: int = None, signal: int = None) -> Dict:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Returns:
            Dict with macd_line, signal_line, histogram
        """
        fast = fast or INDICATORS_CONFIG["MACD_FAST"]
        slow = slow or INDICATORS_CONFIG["MACD_SLOW"]
        signal = signal or INDICATORS_CONFIG["MACD_SIGNAL"]
        
        close = self.df['close'].values
        ema_fast = self._ema(close, fast)
        ema_slow = self._ema(close, slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = self._ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        self.indicators['MACD'] = macd_line
        self.indicators['MACD_SIGNAL'] = signal_line
        self.indicators['MACD_HISTOGRAM'] = histogram
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(self, period: int = None, std_dev: float = None) -> Dict:
        """Calculate Bollinger Bands"""
        period = period or INDICATORS_CONFIG["BOLLINGER_PERIOD"]
        std_dev = std_dev or INDICATORS_CONFIG["BOLLINGER_STD"]
        
        close = self.df['close'].values
        sma = self._sma(close, period)
        std = pd.Series(close).rolling(period).std().values
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        self.indicators['BB_UPPER'] = upper_band
        self.indicators['BB_MIDDLE'] = sma
        self.indicators['BB_LOWER'] = lower_band
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def calculate_atr(self, period: int = None) -> np.ndarray:
        """Calculate Average True Range"""
        period = period or INDICATORS_CONFIG["ATR_PERIOD"]
        
        high = self.df['high'].values
        low = self.df['low'].values
        close = self.df['close'].values
        
        tr = np.zeros_like(high)
        tr[0] = high[0] - low[0]
        
        for i in range(1, len(close)):
            tr[i] = max(
                high[i] - low[i],
                abs(high[i] - close[i-1]),
                abs(low[i] - close[i-1])
            )
        
        atr = self._sma(tr, period)
        self.indicators['ATR'] = atr
        return atr
    
    def calculate_adx(self, period: int = None) -> np.ndarray:
        """Calculate Average Directional Index"""
        period = period or INDICATORS_CONFIG["ADX_PERIOD"]
        
        high = self.df['high'].values
        low = self.df['low'].values
        
        plus_dm = np.zeros_like(high)
        minus_dm = np.zeros_like(high)
        
        for i in range(1, len(high)):
            up_move = high[i] - high[i-1]
            down_move = low[i-1] - low[i]
            
            if up_move > down_move and up_move > 0:
                plus_dm[i] = up_move
            if down_move > up_move and down_move > 0:
                minus_dm[i] = down_move
        
        tr = np.zeros_like(high)
        tr[0] = high[0] - low[0]
        for i in range(1, len(high)):
            tr[i] = max(
                high[i] - low[i],
                abs(high[i] - (high[i-1] if i > 0 else 0)),
                abs(low[i] - (high[i-1] if i > 0 else 0))
            )
        
        # Simplified ADX calculation
        adx = np.abs(plus_dm - minus_dm) / tr
        adx = self._sma(adx, period) * 100
        
        self.indicators['ADX'] = adx
        return adx
    
    def calculate_stochastic(self, period: int = 14) -> Dict:
        """Calculate Stochastic Oscillator"""
        low_min = pd.Series(self.df['low'].values).rolling(period).min().values
        high_max = pd.Series(self.df['high'].values).rolling(period).max().values
        close = self.df['close'].values
        
        k_percent = np.zeros_like(close, dtype=float)
        for i in range(len(close)):
            if high_max[i] != low_min[i]:
                k_percent[i] = 100 * ((close[i] - low_min[i]) / (high_max[i] - low_min[i]))
            else:
                k_percent[i] = 50
        
        d_percent = self._sma(k_percent, 3)
        
        self.indicators['STOCH_K'] = k_percent
        self.indicators['STOCH_D'] = d_percent
        
        return {'k': k_percent, 'd': d_percent}
    
    def calculate_moving_averages(self) -> Dict:
        """Calculate moving averages"""
        close = self.df['close'].values
        
        ma_periods = [10, 20, 50, 100, 200]
        mas = {}
        
        for period in ma_periods:
            ma = self._sma(close, period)
            mas[f'MA{period}'] = ma
            self.indicators[f'MA{period}'] = ma
        
        return mas
    
    def calculate_volume_indicators(self) -> Dict:
        """Calculate volume-based indicators"""
        volume = self.df['volume'].values
        close = self.df['close'].values
        
        # Volume Moving Average
        vol_ma = self._sma(volume, 20)
        self.indicators['VOL_MA'] = vol_ma
        
        # On-Balance Volume (OBV)
        obv = np.zeros_like(volume, dtype=float)
        obv[0] = volume[0]
        
        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                obv[i] = obv[i-1] + volume[i]
            elif close[i] < close[i-1]:
                obv[i] = obv[i-1] - volume[i]
            else:
                obv[i] = obv[i-1]
        
        self.indicators['OBV'] = obv
        
        return {'vol_ma': vol_ma, 'obv': obv}
    
    @staticmethod
    def _sma(data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Simple Moving Average"""
        return pd.Series(data).rolling(period).mean().values
    
    @staticmethod
    def _ema(data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        return pd.Series(data).ewm(span=period, adjust=False).mean().values
    
    def get_indicator(self, name: str) -> np.ndarray:
        """Get calculated indicator by name"""
        if name not in self.indicators:
            raise ValueError(f"Indicator {name} not calculated")
        return self.indicators[name]
    
    def get_latest_indicators(self) -> Dict:
        """Get the latest values of all calculated indicators"""
        latest = {}
        for name, values in self.indicators.items():
            if isinstance(values, np.ndarray):
                latest[name] = float(values[-1])
        return latest


if __name__ == "__main__":
    # Test example
    import yfinance as yf
    df = yf.download("AAPL", period="1y", interval="1d", progress=False)
    analyzer = TechnicalAnalyzer(df)
    indicators = analyzer.calculate_all_indicators()
    print("Latest Indicators:", analyzer.get_latest_indicators())
