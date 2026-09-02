"""
Support & Resistance Module - Identifies key support and resistance levels
"""
import numpy as np
import pandas as pd
from config import SR_CONFIG
from typing import List, Dict, Tuple


class SupportResistanceAnalyzer:
    """Identifies support and resistance levels"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer
        
        Args:
            df: DataFrame with OHLCV data
        """
        self.df = df.copy()
        self.support_levels = []
        self.resistance_levels = []
        
    def find_levels(self, lookback: int = None, min_touches: int = None, tolerance: float = None) -> Dict:
        """
        Find support and resistance levels
        
        Args:
            lookback: Number of candles to analyze
            min_touches: Minimum touches to confirm level
            tolerance: Price tolerance in percent
        
        Returns:
            Dict with support and resistance levels
        """
        lookback = lookback or SR_CONFIG["LOOKBACK_PERIOD"]
        min_touches = min_touches or SR_CONFIG["MIN_TOUCHES"]
        tolerance = tolerance or SR_CONFIG["TOLERANCE_PERCENT"]
        
        data = self.df.iloc[-lookback:]
        highs = data['high'].values
        lows = data['low'].values
        closes = data['close'].values
        
        # Find local peaks and troughs
        peaks = self._find_peaks(highs)
        troughs = self._find_troughs(lows)
        
        # Group similar levels
        resistance_candidates = highs[peaks] if len(peaks) > 0 else np.array([])
        support_candidates = lows[troughs] if len(troughs) > 0 else np.array([])
        
        self.resistance_levels = self._cluster_levels(resistance_candidates, tolerance)
        self.support_levels = self._cluster_levels(support_candidates, tolerance)
        
        # Filter by minimum touches
        self.resistance_levels = self._filter_by_touches(
            self.resistance_levels, data, min_touches, "resistance"
        )
        self.support_levels = self._filter_by_touches(
            self.support_levels, data, min_touches, "support"
        )
        
        return {
            'support': sorted(self.support_levels),
            'resistance': sorted(self.resistance_levels, reverse=True),
            'support_count': len(self.support_levels),
            'resistance_count': len(self.resistance_levels)
        }
    
    @staticmethod
    def _find_peaks(data: np.ndarray, window: int = 3) -> np.ndarray:
        """Find local peaks (resistance)"""
        peaks = []
        for i in range(window, len(data) - window):
            if data[i] == np.max(data[i-window:i+window+1]):
                peaks.append(i)
        return np.array(peaks)
    
    @staticmethod
    def _find_troughs(data: np.ndarray, window: int = 3) -> np.ndarray:
        """Find local troughs (support)"""
        troughs = []
        for i in range(window, len(data) - window):
            if data[i] == np.min(data[i-window:i+window+1]):
                troughs.append(i)
        return np.array(troughs)
    
    @staticmethod
    def _cluster_levels(prices: np.ndarray, tolerance: float) -> List[float]:
        """Cluster similar price levels"""
        if len(prices) == 0:
            return []
        
        prices = sorted(prices)
        clusters = []
        current_cluster = [prices[0]]
        
        for price in prices[1:]:
            price_change_percent = abs(price - current_cluster[-1]) / current_cluster[-1] * 100
            
            if price_change_percent <= tolerance:
                current_cluster.append(price)
            else:
                # Average the cluster
                clusters.append(np.mean(current_cluster))
                current_cluster = [price]
        
        if current_cluster:
            clusters.append(np.mean(current_cluster))
        
        return clusters
    
    @staticmethod
    def _filter_by_touches(levels: List[float], df: pd.DataFrame, 
                          min_touches: int, level_type: str) -> List[float]:
        """Filter levels by number of touches"""
        filtered = []
        highs = df['high'].values
        lows = df['low'].values
        
        for level in levels:
            if level_type == "resistance":
                touches = np.sum((highs >= level * 0.995) & (highs <= level * 1.005))
            else:  # support
                touches = np.sum((lows >= level * 0.995) & (lows <= level * 1.005))
            
            if touches >= min_touches:
                filtered.append(level)
        
        return filtered
    
    def get_nearest_support(self, price: float) -> Tuple[float, float]:
        """
        Get nearest support level below current price
        
        Returns:
            Tuple of (level, distance)
        """
        supports_below = [s for s in self.support_levels if s < price]
        if not supports_below:
            return None, None
        
        nearest = max(supports_below)
        distance = (price - nearest) / price * 100
        return nearest, distance
    
    def get_nearest_resistance(self, price: float) -> Tuple[float, float]:
        """
        Get nearest resistance level above current price
        
        Returns:
            Tuple of (level, distance)
        """
        resistances_above = [r for r in self.resistance_levels if r > price]
        if not resistances_above:
            return None, None
        
        nearest = min(resistances_above)
        distance = (nearest - price) / price * 100
        return nearest, distance
    
    def get_all_levels(self) -> Dict:
        """Get all identified levels"""
        return {
            'support': sorted(self.support_levels),
            'resistance': sorted(self.resistance_levels, reverse=True)
        }


if __name__ == "__main__":
    import yfinance as yf
    df = yf.download("AAPL", period="1y", interval="1d", progress=False)
    analyzer = SupportResistanceAnalyzer(df)
    levels = analyzer.find_levels()
    print("Support & Resistance Levels:", levels)
