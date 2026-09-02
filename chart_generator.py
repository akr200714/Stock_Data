"""
Chart Visualization Module - Generate technical analysis charts
Supports: Swing Trading, Intraday, BTST, Scalping, and Options Scalping
Timeframes: 1m, 3m, 5m, 15m, 1h, 4h, 1d
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, Patch
import os
from datetime import datetime, timedelta


class ChartGenerator:
    """Generate technical analysis charts for all trading strategies"""
    
    # Supported timeframes for all strategies
    SUPPORTED_TIMEFRAMES = {
        '1m': '1 minute',       # Options scalping
        '3m': '3 minutes',      # Options scalping
        '5m': '5 minutes',      # Scalping
        '15m': '15 minutes',    # BTST/Scalping
        '1h': '1 hour',         # Intraday/Swing
        '4h': '4 hours',        # Swing
        '1d': '1 day',          # Swing/Momentum
    }
    
    # Chart display settings by timeframe
    TIMEFRAME_CONFIG = {
        '1m': {'candles': 50, 'rsi_period': 7, 'macd_fast': 5, 'title_suffix': '[ULTRA-FAST]'},
        '3m': {'candles': 50, 'rsi_period': 9, 'macd_fast': 8, 'title_suffix': '[SUPER-FAST]'},
        '5m': {'candles': 60, 'rsi_period': 9, 'macd_fast': 10, 'title_suffix': '[FAST]'},
        '15m': {'candles': 70, 'rsi_period': 12, 'macd_fast': 12, 'title_suffix': '[MEDIUM]'},
        '1h': {'candles': 100, 'rsi_period': 14, 'macd_fast': 12, 'title_suffix': '[INTRADAY]'},
        '4h': {'candles': 100, 'rsi_period': 14, 'macd_fast': 12, 'title_suffix': '[SWING]'},
        '1d': {'candles': 100, 'rsi_period': 14, 'macd_fast': 12, 'title_suffix': '[DAILY]'},
    }
    
    def __init__(self, symbol: str, df: pd.DataFrame, output_dir: str = "charts", 
                 timeframe: str = '1d', strategy: str = 'swing'):
        """
        Initialize chart generator
        
        Args:
            symbol: Stock symbol
            df: OHLCV DataFrame
            output_dir: Directory to save charts
            timeframe: Chart timeframe ('1m', '3m', '5m', '15m', '1h', '4h', '1d')
            strategy: Trading strategy ('scalping', 'options_scalping', 'intraday', 'btst', 'swing', 'momentum')
        """
        self.symbol = symbol
        self.df = df
        self.output_dir = output_dir
        self.timeframe = timeframe if timeframe in self.SUPPORTED_TIMEFRAMES else '1d'
        self.strategy = strategy
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_main_chart(self, indicators_dict: dict, sr_levels: dict, 
                           current_price: float, recommendation: dict):
        """
        Generate main analysis chart with all indicators
        
        Args:
            indicators_dict: Dictionary of calculated indicators
            sr_levels: Support and resistance levels
            current_price: Current stock price
            recommendation: Recommendation data
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
        
        # Get last 100 candles for display
        data = self.df.iloc[-100:]
        dates = data.index
        
        # Chart 1: Price with Bollinger Bands
        ax1 = axes[0]
        closes = data['close'].values
        highs = data['high'].values
        lows = data['low'].values
        
        ax1.plot(dates, closes, label='Close', color='black', linewidth=1.5)
        
        # Bollinger Bands
        if 'BB_UPPER' in indicators_dict and 'BB_LOWER' in indicators_dict:
            bb_upper = indicators_dict['BB_UPPER'][-len(data):]
            bb_middle = indicators_dict['BB_MIDDLE'][-len(data):]
            bb_lower = indicators_dict['BB_LOWER'][-len(data):]
            
            ax1.plot(dates, bb_upper, '--', color='red', alpha=0.5, label='BB Upper')
            ax1.plot(dates, bb_middle, '--', color='orange', alpha=0.5, label='BB Middle')
            ax1.plot(dates, bb_lower, '--', color='green', alpha=0.5, label='BB Lower')
            ax1.fill_between(dates, bb_upper, bb_lower, alpha=0.1, color='gray')
        
        # Support & Resistance
        for sr in sr_levels.get('support', []):
            ax1.axhline(y=sr, color='green', linestyle=':', alpha=0.5, linewidth=1)
            ax1.text(dates[0], sr, f' S: ${sr:.2f}', fontsize=8, color='green')
        
        for sr in sr_levels.get('resistance', []):
            ax1.axhline(y=sr, color='red', linestyle=':', alpha=0.5, linewidth=1)
            ax1.text(dates[0], sr, f' R: ${sr:.2f}', fontsize=8, color='red')
        
        # Target and Stop Loss
        if recommendation:
            ax1.axhline(y=recommendation['take_profit'], color='darkgreen', 
                        linestyle='-', alpha=0.7, linewidth=2, label=f"TP: ${recommendation['take_profit']:.2f}")
            ax1.axhline(y=recommendation['stop_loss'], color='darkred', 
                        linestyle='-', alpha=0.7, linewidth=2, label=f"SL: ${recommendation['stop_loss']:.2f}")
        
        ax1.set_title(f'{self.symbol} - Technical Analysis', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=10)
        ax1.legend(loc='upper left', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # Chart 2: RSI and Stochastic
        ax2 = axes[1]
        if 'RSI' in indicators_dict:
            rsi = indicators_dict['RSI'][-len(data):]
            ax2.plot(dates, rsi, label='RSI', color='blue', linewidth=1.5)
            ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5)
            ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5)
            ax2.fill_between(dates, 30, 70, alpha=0.1, color='gray')
        
        if 'STOCH_K' in indicators_dict:
            stoch_k = indicators_dict['STOCH_K'][-len(data):]
            ax2.plot(dates, stoch_k, label='Stochastic %K', color='purple', linewidth=1, alpha=0.7)
        
        ax2.set_ylabel('Oscillators', fontsize=10)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='upper left', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # Chart 3: Volume and MACD
        ax3 = axes[2]
        volume = data['volume'].values
        colors = ['green' if closes[i] >= closes[i-1] else 'red' 
                 for i in range(1, len(closes))]
        colors.insert(0, 'gray')
        
        ax3.bar(dates, volume, color=colors, alpha=0.6, label='Volume')
        
        if 'MACD' in indicators_dict:
            macd = indicators_dict['MACD'][-len(data):]
            macd_signal = indicators_dict['MACD_SIGNAL'][-len(data):]
            
            ax3_twin = ax3.twinx()
            ax3_twin.plot(dates, macd, label='MACD', color='blue', linewidth=1.5)
            ax3_twin.plot(dates, macd_signal, label='Signal', color='red', linewidth=1.5)
            ax3_twin.set_ylabel('MACD', fontsize=10)
            ax3_twin.legend(loc='upper right', fontsize=8)
        
        ax3.set_ylabel('Volume', fontsize=10)
        ax3.set_xlabel('Date', fontsize=10)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax3.legend(loc='upper left', fontsize=8)
        ax3.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save chart
        filename = f"{self.output_dir}/{self.symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Chart saved: {filename}")
        plt.close()
        
        return filename
    
    def generate_scalping_chart(self, indicators_dict: dict, sr_levels: dict, 
                               current_price: float, recommendation: dict):
        """
        Generate optimized chart for scalping and options scalping
        Compact layout with fast indicators and micro-trend analysis
        
        Args:
            indicators_dict: Dictionary of calculated indicators
            sr_levels: Support and resistance levels
            current_price: Current stock price
            recommendation: Recommendation data
        """
        # Get config for current timeframe
        config = self.TIMEFRAME_CONFIG.get(self.timeframe, self.TIMEFRAME_CONFIG['5m'])
        num_candles = config['candles']
        title_suffix = config['title_suffix']
        
        # Create compact 2-row layout for faster decision making
        fig, axes = plt.subplots(2, 1, figsize=(16, 8), 
                                 gridspec_kw={'height_ratios': [2, 1]}, sharex=True)
        
        # Get last N candles for display
        data = self.df.iloc[-num_candles:]
        dates = data.index
        
        # Chart 1: Price with Bollinger Bands and Support/Resistance
        ax1 = axes[0]
        closes = data['close'].values
        opens = data['open'].values
        highs = data['high'].values
        lows = data['low'].values
        
        # Draw candlesticks with enhanced colors
        width = 0.6
        for i, (date, o, h, l, c) in enumerate(zip(dates, opens, highs, lows, closes)):
            color = 'lime' if c >= o else 'red'
            ax1.plot([date, date], [l, h], color=color, linewidth=0.8, alpha=0.8)
            ax1.bar(date, c - o, bottom=min(o, c), width=0.5*width, 
                   color=color, edgecolor='black', linewidth=0.5, alpha=0.9)
        
        # Plot close price line
        ax1.plot(dates, closes, label='Close', color='black', linewidth=2, alpha=0.7, zorder=5)
        
        # Bollinger Bands with tighter visualization
        if 'BB_UPPER' in indicators_dict and 'BB_LOWER' in indicators_dict:
            bb_upper = indicators_dict['BB_UPPER'][-len(data):]
            bb_middle = indicators_dict['BB_MIDDLE'][-len(data):]
            bb_lower = indicators_dict['BB_LOWER'][-len(data):]
            
            ax1.plot(dates, bb_upper, '--', color='red', alpha=0.6, linewidth=1.5, label='BB Upper')
            ax1.plot(dates, bb_middle, '--', color='orange', alpha=0.5, linewidth=1, label='BB Middle')
            ax1.plot(dates, bb_lower, '--', color='green', alpha=0.6, linewidth=1.5, label='BB Lower')
            ax1.fill_between(dates, bb_upper, bb_lower, alpha=0.08, color='gray')
        
        # Support & Resistance with distance labels
        sr_count = {'support': 0, 'resistance': 0}
        
        for sr in sr_levels.get('support', []):
            ax1.axhline(y=sr, color='green', linestyle=':', alpha=0.6, linewidth=1.5)
            distance = ((current_price - sr) / current_price) * 100
            ax1.text(dates[0], sr, f' S: {sr:.2f} ({distance:.2f}%)', 
                    fontsize=7, color='darkgreen', fontweight='bold')
            sr_count['support'] += 1
        
        for sr in sr_levels.get('resistance', []):
            ax1.axhline(y=sr, color='red', linestyle=':', alpha=0.6, linewidth=1.5)
            distance = ((sr - current_price) / current_price) * 100
            ax1.text(dates[0], sr, f' R: {sr:.2f} ({distance:.2f}%)', 
                    fontsize=7, color='darkred', fontweight='bold')
            sr_count['resistance'] += 1
        
        # Current price indicator
        ax1.axhline(y=current_price, color='blue', linestyle='-', alpha=0.8, linewidth=2, 
                   label=f'Current: ${current_price:.2f}')
        
        # Target and Stop Loss (thick lines for scalping visibility)
        if recommendation:
            tp = recommendation.get('take_profit', current_price * 1.01)
            sl = recommendation.get('stop_loss', current_price * 0.99)
            
            ax1.axhline(y=tp, color='darkgreen', linestyle='-', alpha=0.9, linewidth=2.5, 
                        label=f"TP: ${tp:.2f} ({((tp-current_price)/current_price*100):+.2f}%)")
            ax1.axhline(y=sl, color='darkred', linestyle='-', alpha=0.9, linewidth=2.5, 
                        label=f"SL: ${sl:.2f} ({((sl-current_price)/current_price*100):+.2f}%)")
            
            # Highlight profit/loss zones
            ax1.fill_between(dates, current_price, tp, alpha=0.15, color='green', label='Profit Zone')
            ax1.fill_between(dates, sl, current_price, alpha=0.15, color='red', label='Loss Zone')
        
        # Add confidence indicator
        if recommendation and 'confidence' in recommendation:
            confidence = recommendation['confidence'] * 100
            ax1.text(0.02, 0.98, f"Confidence: {confidence:.1f}%", 
                    transform=ax1.transAxes, fontsize=10, fontweight='bold',
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Format and style
        ax1.set_title(f'{self.symbol} - {self.SUPPORTED_TIMEFRAMES[self.timeframe]} Scalping Chart {title_suffix}\n' + 
                     f'S/R Levels: Support={sr_count["support"]}, Resistance={sr_count["resistance"]}',
                     fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=10, fontweight='bold')
        ax1.legend(loc='upper left', fontsize=7, ncol=2)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_facecolor('#f8f9fa')
        
        # Chart 2: RSI + Stochastic (Combined momentum indicators)
        ax2 = axes[1]
        
        rsi_present = 'RSI' in indicators_dict
        stoch_present = 'STOCH_K' in indicators_dict
        
        if rsi_present:
            rsi = indicators_dict['RSI'][-len(data):]
            ax2.plot(dates, rsi, label='RSI(14)', color='blue', linewidth=2, alpha=0.8)
            ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5, linewidth=1)
            ax2.fill_between(dates, 30, 70, alpha=0.1, color='gray')
            ax2.fill_between(dates, 70, 100, alpha=0.1, color='red', label='Overbought Zone')
            ax2.fill_between(dates, 0, 30, alpha=0.1, color='green', label='Oversold Zone')
        
        if stoch_present:
            stoch_k = indicators_dict['STOCH_K'][-len(data):]
            stoch_d = indicators_dict.get('STOCH_D', [np.nan]*len(stoch_k))[-len(data):]
            
            ax2_alt = ax2.twinx()
            ax2_alt.plot(dates, stoch_k, label='Stoch %K', color='purple', linewidth=1.5, alpha=0.7, linestyle='-')
            if len(stoch_d) > 0 and not np.isnan(stoch_d).all():
                ax2_alt.plot(dates, stoch_d, label='Stoch %D', color='orange', linewidth=1.5, alpha=0.7, linestyle='--')
            ax2_alt.set_ylim(0, 100)
            ax2_alt.set_ylabel('Stochastic', fontsize=9, fontweight='bold')
            ax2_alt.legend(loc='center right', fontsize=7)
        
        ax2.set_ylabel('RSI', fontsize=9, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.set_xlabel('Time', fontsize=10, fontweight='bold')
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M' if self.timeframe in ['1m', '3m', '5m', '15m'] else '%m-%d'))
        ax2.legend(loc='upper left', fontsize=7)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.set_facecolor('#f8f9fa')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        strategy_label = 'options_scalping' if self.strategy == 'options_scalping' else 'scalping'
        filename = f"{self.output_dir}/{self.symbol}_{strategy_label}_{self.timeframe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Scalping chart saved: {filename}")
        plt.close()
        
        return filename
    
    def generate_order_blocks_chart(self, ob_data: dict):
        """Generate chart highlighting order blocks"""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        data = self.df.iloc[-100:]
        dates = data.index
        closes = data['close'].values
        highs = data['high'].values
        lows = data['low'].values
        opens = data['open'].values
        
        # Candlesticks
        width = 0.6
        width2 = 0.05
        
        colors = ['green' if closes[i] >= opens[i] else 'red' 
                 for i in range(len(closes))]
        
        # Draw candlesticks
        for i, (date, o, h, l, c, color) in enumerate(zip(dates, opens, highs, lows, closes, colors)):
            ax.plot([date, date], [l, h], color=color, linewidth=1)
            ax.bar(date, c - o, bottom=min(o, c), width=width2, color=color, edgecolor='black')
        
        # Highlight bullish order blocks
        for block in ob_data.get('bullish_blocks', []):
            rect = Rectangle((dates[min(block.get('index', 0), len(dates)-1)], block['low']), 
                            width=2, height=block['high'] - block['low'],
                            alpha=0.2, color='green', label='Bullish OB')
            ax.add_patch(rect)
        
        # Highlight bearish order blocks
        for block in ob_data.get('bearish_blocks', []):
            rect = Rectangle((dates[min(block.get('index', 0), len(dates)-1)], block['low']), 
                            width=2, height=block['high'] - block['low'],
                            alpha=0.2, color='red', label='Bearish OB')
            ax.add_patch(rect)
        
        ax.set_title(f'{self.symbol} - Order Blocks', fontsize=12, fontweight='bold')
        ax.set_ylabel('Price ($)', fontsize=10)
        ax.set_xlabel('Date', fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        filename = f"{self.output_dir}/{self.symbol}_order_blocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Order blocks chart saved: {filename}")
        plt.close()
        
        return filename
    
    def generate_multi_timeframe_scalping(self, timeframe_data: dict):
        """
        Generate multi-timeframe comparison for options scalping
        Shows 1m, 3m, 5m, 15m side by side for quick decision making
        
        Args:
            timeframe_data: Dictionary with keys '1m', '3m', '5m', '15m'
                           Each containing: {'df': DataFrame, 'rsi': array, 'price': float, 'recommendation': dict}
        """
        fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=False)
        timeframes = ['1m', '3m', '5m', '15m']
        colors_tf = {'1m': '#FF6B6B', '3m': '#FF9999', '5m': '#4ECDC4', '15m': '#45B7D1'}
        
        for idx, timeframe in enumerate(timeframes):
            if timeframe not in timeframe_data:
                continue
            
            ax = axes[idx]
            tf_info = timeframe_data[timeframe]
            df = tf_info['df']
            
            # Show last 30 candles for each timeframe
            data = df.iloc[-30:]
            dates = data.index
            closes = data['close'].values
            opens = data['open'].values
            highs = data['high'].values
            lows = data['low'].values
            
            # Draw candlesticks
            for i, (date, o, h, l, c) in enumerate(zip(dates, opens, highs, lows, closes)):
                color = 'lime' if c >= o else 'red'
                ax.plot([date, date], [l, h], color=color, linewidth=0.8)
                ax.bar(date, c - o, bottom=min(o, c), width=0.4, 
                      color=color, edgecolor='black', linewidth=0.5)
            
            # Plot close line
            ax.plot(dates, closes, color=colors_tf[timeframe], linewidth=2, label='Close')
            
            # RSI from indicators
            rsi = tf_info.get('rsi', [])
            if len(rsi) > 0:
                ax2 = ax.twinx()
                ax2.plot(dates[-len(rsi):], rsi[-len(dates):], 'o-', 
                        color='purple', alpha=0.5, linewidth=1.5, markersize=3)
                ax2.set_ylim(0, 100)
                ax2.axhline(y=70, color='red', linestyle='--', alpha=0.3)
                ax2.axhline(y=30, color='green', linestyle='--', alpha=0.3)
                ax2.set_ylabel('RSI', fontsize=8)
            
            # Current price
            current_price = tf_info.get('price', closes[-1])
            ax.axhline(y=current_price, color='blue', linestyle='-', alpha=0.7, linewidth=2)
            
            # Recommendation info
            rec = tf_info.get('recommendation', {})
            if rec:
                action = rec.get('action', 'HOLD').upper()
                confidence = rec.get('confidence', 0) * 100
                tp = rec.get('take_profit', current_price)
                sl = rec.get('stop_loss', current_price)
                
                title_text = f'{self.SUPPORTED_TIMEFRAMES[timeframe]} | Action: {action} | Conf: {confidence:.0f}% | TP: ${tp:.2f} | SL: ${sl:.2f}'
                ax.set_title(title_text, fontsize=10, fontweight='bold', 
                           color='darkgreen' if action == 'BUY' else 'darkred' if action == 'SELL' else 'gray')
            
            ax.set_ylabel('Price ($)', fontsize=9)
            ax.grid(True, alpha=0.2)
            ax.legend(loc='upper left', fontsize=8)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M' if timeframe in ['1m', '3m', '5m'] else '%H:%M'))
        
        axes[-1].set_xlabel('Time', fontsize=10)
        fig.suptitle(f'{self.symbol} - Multi-Timeframe Options Scalping Analysis\n' + 
                    '1m (Ultra-Fast) | 3m (Super-Fast) | 5m (Fast) | 15m (Medium)', 
                    fontsize=13, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save
        filename = f"{self.output_dir}/{self.symbol}_multi_tf_scalping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Multi-timeframe scalping chart saved: {filename}")
        plt.close()
        
        return filename
    
    def get_timeframe_info(self) -> dict:
        """Get current timeframe configuration"""
        return self.TIMEFRAME_CONFIG.get(self.timeframe, self.TIMEFRAME_CONFIG['1d'])
    
    def is_scalping_timeframe(self) -> bool:
        """Check if current timeframe is suitable for scalping"""
        return self.timeframe in ['1m', '3m', '5m', '15m']
    
    def is_options_scalping_timeframe(self) -> bool:
        """Check if current timeframe is suitable for options scalping"""
        return self.timeframe in ['1m', '3m', '5m']
    
    def get_supported_timeframes(self) -> list:
        """Get list of all supported timeframes"""
        return list(self.SUPPORTED_TIMEFRAMES.keys())


if __name__ == "__main__":
    import yfinance as yf
    df = yf.download("AAPL", period="3mo", interval="1d", progress=False)
    generator = ChartGenerator("AAPL", df, timeframe='1d', strategy='swing')
    print("✅ Chart generator initialized successfully")
    print(f"📊 Supported timeframes: {generator.get_supported_timeframes()}")
    print(f"🏃 Options scalping timeframes available: {[tf for tf in generator.get_supported_timeframes() if generator.timeframe == tf and generator.is_options_scalping_timeframe()]}")

