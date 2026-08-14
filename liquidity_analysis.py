"""
Liquidity Module - Analyzes market liquidity and volume profiles
"""
import numpy as np
import pandas as pd
from config import LIQUIDITY_CONFIG
from typing import Dict, Tuple


class LiquidityAnalyzer:
    """Analyzes market liquidity and volume characteristics"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer
        
        Args:
            df: DataFrame with OHLCV data
        """
        self.df = df.copy()
        self.volume_profile = None
        
    def analyze_liquidity(self) -> Dict:
        """
        Comprehensive liquidity analysis
        
        Returns:
            Dict with liquidity metrics
        """
        volume = self.df['volume'].values
        close = self.df['close'].values
        
        # Calculate volume metrics
        avg_volume = np.mean(volume)
        vol_ma_20 = pd.Series(volume).rolling(20).mean().iloc[-1]
        current_volume = volume[-1]
        vol_vs_avg = (current_volume / avg_volume) if avg_volume > 0 else 0
        
        # Volume trend
        recent_vols = volume[-10:]
        vol_trend = "increasing" if recent_vols[-1] > np.mean(recent_vols[:-1]) else "decreasing"
        
        # Liquidity quality score (0-100)
        liquidity_score = self._calculate_liquidity_score(
            avg_volume, 
            vol_vs_avg, 
            vol_trend
        )
        
        # Price-volume analysis
        pv_correlation = self._calculate_price_volume_correlation(close, volume)
        
        # Volume clusters (support/resistance by volume)
        volume_clusters = self._find_volume_clusters(close, volume)
        
        return {
            'average_volume': float(avg_volume),
            'volume_ma_20': float(vol_ma_20),
            'current_volume': float(current_volume),
            'volume_vs_average': float(vol_vs_avg),
            'volume_trend': vol_trend,
            'liquidity_score': liquidity_score,
            'price_volume_correlation': float(pv_correlation),
            'volume_clusters': volume_clusters,
            'is_liquid': liquidity_score >= 60,
            'liquidity_grade': self._get_liquidity_grade(liquidity_score)
        }
    
    def get_volume_profile(self, lookback: int = 50) -> Dict:
        """
        Get volume profile for price levels
        
        Args:
            lookback: Number of candles to analyze
        
        Returns:
            Dict with price levels and their associated volumes
        """
        data = self.df.iloc[-lookback:]
        closes = data['close'].values
        volumes = data['volume'].values
        
        # Create price bins
        price_min = np.min(closes)
        price_max = np.max(closes)
        bins = np.linspace(price_min, price_max, 20)
        
        volume_at_price = {}
        for i in range(len(bins) - 1):
            mask = (closes >= bins[i]) & (closes < bins[i+1])
            vol = np.sum(volumes[mask])
            if vol > 0:
                price_level = (bins[i] + bins[i+1]) / 2
                volume_at_price[f"{price_level:.2f}"] = float(vol)
        
        self.volume_profile = volume_at_price
        return volume_at_price
    
    def get_volume_weighted_price(self, lookback: int = 20) -> float:
        """
        Calculate Volume Weighted Average Price (VWAP)
        
        Args:
            lookback: Number of candles
        
        Returns:
            VWAP value
        """
        data = self.df.iloc[-lookback:]
        typical_price = ((data['high'] + data['low'] + data['close']) / 3).values
        volume = data['volume'].values
        
        vwap = np.sum(typical_price * volume) / np.sum(volume)
        return float(vwap)
    
    def analyze_volume_at_price_levels(self, support_resistance_levels: list) -> Dict:
        """
        Analyze volume at support and resistance levels
        
        Args:
            support_resistance_levels: List of price levels to analyze
        
        Returns:
            Dict with volume analysis for each level
        """
        close = self.df['close'].values
        volume = self.df['volume'].values
        
        analysis = {}
        for level in support_resistance_levels:
            # Find candles near this price level (±0.5%)
            near_level = (close >= level * 0.995) & (close <= level * 1.005)
            vol_at_level = np.sum(volume[near_level])
            avg_vol = np.mean(volume)
            
            analysis[f"Level_{level:.2f}"] = {
                'volume': float(vol_at_level),
                'volume_ratio': float(vol_at_level / avg_vol) if avg_vol > 0 else 0,
                'touches': int(np.sum(near_level)),
                'is_high_volume': vol_at_level > avg_vol * 1.5
            }
        
        return analysis
    
    @staticmethod
    def _calculate_liquidity_score(avg_volume: float, vol_vs_avg: float, 
                                   vol_trend: str) -> int:
        """Calculate overall liquidity score (0-100)"""
        score = 0
        
        # Volume size (0-40 points)
        if avg_volume > LIQUIDITY_CONFIG["MIN_LIQUIDITY_VOLUME"]:
            score += 40
        else:
            score += max(0, int((avg_volume / LIQUIDITY_CONFIG["MIN_LIQUIDITY_VOLUME"]) * 40))
        
        # Volume vs average (0-40 points)
        if vol_vs_avg >= 1.0:
            score += 40
        else:
            score += int(vol_vs_avg * 40)
        
        # Volume trend (0-20 points)
        if vol_trend == "increasing":
            score += 20
        else:
            score += 10
        
        return min(100, score)
    
    @staticmethod
    def _get_liquidity_grade(score: int) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    @staticmethod
    def _calculate_price_volume_correlation(close: np.ndarray, volume: np.ndarray) -> float:
        """Calculate correlation between price changes and volume"""
        price_changes = np.diff(close)
        vol_changes = np.diff(volume)
        
        if len(price_changes) < 2:
            return 0.0
        
        correlation = np.corrcoef(price_changes, vol_changes)[0, 1]
        return np.nan_to_num(correlation, 0.0)
    
    @staticmethod
    def _find_volume_clusters(close: np.ndarray, volume: np.ndarray, 
                             num_clusters: int = 5) -> list:
        """Find price levels with high volume concentration"""
        # Create price bins and sum volumes
        price_min, price_max = np.min(close), np.max(close)
        bins = np.linspace(price_min, price_max, num_clusters)
        
        clusters = []
        for i in range(len(bins) - 1):
            mask = (close >= bins[i]) & (close < bins[i+1])
            vol = np.sum(volume[mask])
            if vol > 0:
                clusters.append({
                    'price_range': f"${bins[i]:.2f}-${bins[i+1]:.2f}",
                    'center': float((bins[i] + bins[i+1]) / 2),
                    'volume': float(vol),
                    'candles': int(np.sum(mask))
                })
        
        # Sort by volume
        clusters.sort(key=lambda x: x['volume'], reverse=True)
        return clusters[:3]  # Top 3 clusters


if __name__ == "__main__":
    import yfinance as yf
    df = yf.download("AAPL", period="1y", interval="1d", progress=False)
    analyzer = LiquidityAnalyzer(df)
    liquidity = analyzer.analyze_liquidity()
    print("Liquidity Analysis:", liquidity)
