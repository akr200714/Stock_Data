"""
Order Blocks Module - Identifies order blocks and breakout levels
"""
import numpy as np
import pandas as pd
from config import ORDER_BLOCKS_CONFIG
from typing import List, Dict, Tuple


class OrderBlockAnalyzer:
    """Identifies order blocks from price action"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer
        
        Args:
            df: DataFrame with OHLCV data
        """
        self.df = df.copy()
        self.bullish_blocks = []
        self.bearish_blocks = []
        
    def find_order_blocks(self, lookback: int = None) -> Dict:
        """
        Find bullish and bearish order blocks
        
        Args:
            lookback: Number of candles to analyze
        
        Returns:
            Dict with identified order blocks
        """
        lookback = lookback or ORDER_BLOCKS_CONFIG["LOOKBACK_PERIOD"]
        data = self.df.iloc[-lookback:]
        
        opens = data['open'].values
        highs = data['high'].values
        lows = data['low'].values
        closes = data['close'].values
        
        self.bullish_blocks = self._find_bullish_blocks(opens, highs, lows, closes)
        self.bearish_blocks = self._find_bearish_blocks(opens, highs, lows, closes)
        
        return {
            'bullish_blocks': self.bullish_blocks,
            'bearish_blocks': self.bearish_blocks,
            'bullish_count': len(self.bullish_blocks),
            'bearish_count': len(self.bearish_blocks)
        }
    
    def _find_bullish_blocks(self, opens: np.ndarray, highs: np.ndarray, 
                             lows: np.ndarray, closes: np.ndarray) -> List[Dict]:
        """Find bullish order blocks"""
        blocks = []
        min_candles = ORDER_BLOCKS_CONFIG["MIN_CANDLES"]
        break_distance = ORDER_BLOCKS_CONFIG["BREAK_DISTANCE"]
        
        for i in range(min_candles, len(closes) - 1):
            # Look for impulsive move down followed by consolidation
            if closes[i-min_candles] > closes[i-1]:  # Downtrend
                # Check if price is breaking above the block
                block_high = max(highs[i-min_candles:i])
                block_low = min(lows[i-min_candles:i])
                
                if closes[i] > block_high * (1 + break_distance):
                    blocks.append({
                        'type': 'bullish',
                        'index': i,
                        'high': block_high,
                        'low': block_low,
                        'range': block_high - block_low,
                        'price': closes[i]
                    })
        
        return blocks[-3:] if len(blocks) > 3 else blocks  # Return recent blocks
    
    def _find_bearish_blocks(self, opens: np.ndarray, highs: np.ndarray, 
                             lows: np.ndarray, closes: np.ndarray) -> List[Dict]:
        """Find bearish order blocks"""
        blocks = []
        min_candles = ORDER_BLOCKS_CONFIG["MIN_CANDLES"]
        break_distance = ORDER_BLOCKS_CONFIG["BREAK_DISTANCE"]
        
        for i in range(min_candles, len(closes) - 1):
            # Look for impulsive move up followed by consolidation
            if closes[i-min_candles] < closes[i-1]:  # Uptrend
                # Check if price is breaking below the block
                block_high = max(highs[i-min_candles:i])
                block_low = min(lows[i-min_candles:i])
                
                if closes[i] < block_low * (1 - break_distance):
                    blocks.append({
                        'type': 'bearish',
                        'index': i,
                        'high': block_high,
                        'low': block_low,
                        'range': block_high - block_low,
                        'price': closes[i]
                    })
        
        return blocks[-3:] if len(blocks) > 3 else blocks  # Return recent blocks
    
    def get_latest_block(self, block_type: str = 'bullish') -> Dict:
        """Get the most recent order block"""
        blocks = self.bullish_blocks if block_type == 'bullish' else self.bearish_blocks
        return blocks[-1] if blocks else None
    
    def get_all_blocks(self) -> Dict:
        """Get all identified blocks"""
        return {
            'bullish': self.bullish_blocks,
            'bearish': self.bearish_blocks
        }
    
    def is_at_order_block(self, current_price: float, tolerance: float = 0.01) -> Tuple[bool, Dict]:
        """
        Check if current price is at an order block
        
        Returns:
            Tuple of (is_at_block, block_info)
        """
        for block in self.bullish_blocks + self.bearish_blocks:
            block_range = block['range'] * tolerance
            block_mid = (block['high'] + block['low']) / 2
            
            if abs(current_price - block_mid) <= block_range:
                return True, block
        
        return False, None


if __name__ == "__main__":
    import yfinance as yf
    df = yf.download("AAPL", period="1y", interval="1d", progress=False)
    analyzer = OrderBlockAnalyzer(df)
    blocks = analyzer.find_order_blocks()
    print("Order Blocks:", blocks)
