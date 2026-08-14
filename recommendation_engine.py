"""
Stock Recommendation Engine - AI-powered stock analysis and recommendations
Uses Breeze Connect for real-time market data
Supports multiple trading strategies: Scalping, Intraday, BTST, Swing, Momentum
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from data_handler import StockDataHandler
from technical_analysis import TechnicalAnalyzer
from support_resistance import SupportResistanceAnalyzer
from order_blocks import OrderBlockAnalyzer
from liquidity_analysis import LiquidityAnalyzer
from config import RECOMMENDATION_CONFIG
from strategy_config import get_strategy_config, STRATEGIES
from datetime import datetime


class StockRecommendationEngine:
    """Main engine for stock analysis and recommendations"""
    
    def __init__(self, symbol: str, period: str = "1y", interval: str = "1d", strategy: str = "swing"):
        """
        Initialize recommendation engine
        
        Args:
            symbol: Stock ticker symbol in Breeze format (e.g., 'SBIN-EQ' for NSE)
                   or base symbol (e.g., 'SBIN', auto-converts to 'SBIN-EQ')
            period: Historical period for lookback (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y)
            interval: Data interval (kept for compatibility)
            strategy: Trading strategy - "scalping", "intraday", "btst", "swing", "momentum"
        """
        self.symbol = symbol.upper()
        self.strategy = strategy.lower()
        
        # Validate and load strategy config
        if self.strategy not in STRATEGIES:
            raise ValueError(f"Unknown strategy: {strategy}. Available: {list(STRATEGIES.keys())}")
        
        self.strategy_config = get_strategy_config(self.strategy)
        
        # Use strategy-specific data period and interval if not overridden
        strategy_period = self.strategy_config.get("data_period", period)
        strategy_interval = self.strategy_config.get("data_interval", interval)
        
        self.data_handler = StockDataHandler(symbol, strategy_period, strategy_interval)
        self.df = None
        self.current_price = None
        
        # Analysis modules
        self.technical_analyzer = None
        self.sr_analyzer = None
        self.ob_analyzer = None
        self.liquidity_analyzer = None
        
        # Results
        self.analysis_results = {}
        self.recommendation = None
    
    def run_full_analysis(self) -> Dict:
        """
        Run complete analysis pipeline for selected strategy
        
        Returns:
            Complete analysis results with strategy-specific recommendation
        """
        print(f"\n{'='*60}")
        print(f"STOCK ANALYSIS REPORT: {self.symbol}")
        print(f"STRATEGY: {self.strategy_config['name'].upper()}")
        print(f"TIMEFRAME: {self.strategy_config['timeframe']}")
        print(f"{'='*60}\n")
        
        # Step 1: Fetch data
        print("Step 1: Fetching market data...")
        self.df = self.data_handler.fetch_data()
        self.current_price = self.data_handler.get_current_price()
        print(f"✓ Current price: ₹{self.current_price:.2f}")
        print(f"✓ Data points: {len(self.df)} candles ({self.strategy_config['data_interval']} interval)\n")
        
        # Step 2: Technical Analysis
        print("Step 2: Analyzing technical indicators...")
        self.technical_analyzer = TechnicalAnalyzer(self.df)
        tech_indicators = self.technical_analyzer.calculate_all_indicators()
        self.analysis_results['technical'] = self.technical_analyzer.get_latest_indicators()
        print(f"✓ {len(self.analysis_results['technical'])} indicators calculated\n")
        
        # Step 3: Support & Resistance
        print("Step 3: Identifying support and resistance levels...")
        self.sr_analyzer = SupportResistanceAnalyzer(self.df)
        sr_levels = self.sr_analyzer.find_levels()
        self.analysis_results['support_resistance'] = sr_levels
        print(f"✓ Found {sr_levels['support_count']} support and {sr_levels['resistance_count']} resistance levels\n")
        
        # Step 4: Order Blocks
        print("Step 4: Finding order blocks...")
        self.ob_analyzer = OrderBlockAnalyzer(self.df)
        ob_levels = self.ob_analyzer.find_order_blocks()
        self.analysis_results['order_blocks'] = ob_levels
        print(f"✓ Found {ob_levels['bullish_count']} bullish and {ob_levels['bearish_count']} bearish blocks\n")
        
        # Step 5: Liquidity Analysis
        print("Step 5: Analyzing liquidity...")
        self.liquidity_analyzer = LiquidityAnalyzer(self.df)
        liquidity = self.liquidity_analyzer.analyze_liquidity()
        self.analysis_results['liquidity'] = liquidity
        print(f"✓ Liquidity grade: {liquidity['liquidity_grade']}\n")
        
        # Step 6: Generate Recommendation
        print("Step 6: Generating AI recommendation...")
        self.recommendation = self._generate_strategy_recommendation()
        
        return {
            'symbol': self.symbol,
            'strategy': self.strategy,
            'strategy_name': self.strategy_config['name'],
            'current_price': self.current_price,
            'analysis': self.analysis_results,
            'recommendation': self.recommendation,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendation(self) -> Dict:
        """
        Generate investment recommendation based on all analyses
        
        Returns:
            Recommendation with action, target price, and confidence
        """
        score = 0
        signals = {
            'technical': [],
            'structure': [],
            'liquidity': [],
            'risk_reward': []
        }
        
        # Technical signals
        tech_score, tech_signals = self._analyze_technical_signals()
        score += tech_score * 0.35  # 35% weight
        signals['technical'] = tech_signals
        
        # Support & Resistance signals
        sr_score, sr_signals = self._analyze_sr_signals()
        score += sr_score * 0.25  # 25% weight
        signals['structure'] = sr_signals
        
        # Order blocks signals
        ob_score, ob_signals = self._analyze_ob_signals()
        score += ob_score * 0.20  # 20% weight
        signals['structure'].extend(ob_signals)
        
        # Liquidity signals
        liq_score, liq_signals = self._analyze_liquidity_signals()
        score += liq_score * 0.10  # 10% weight
        signals['liquidity'] = liq_signals
        
        # Risk/Reward signals
        rr_score, rr_signals = self._analyze_risk_reward()
        score += rr_score * 0.10  # 10% weight
        signals['risk_reward'] = rr_signals
        
        # Determine action and targets
        action, confidence = self._determine_action(score)
        take_profit, stop_loss = self._calculate_targets(action)
        
        return {
            'action': action,  # BUY, SELL, or HOLD
            'confidence': confidence,  # 0-100
            'score': round(score, 2),  # Weighted score
            'current_price': round(self.current_price, 2),
            'take_profit': round(take_profit, 2),
            'stop_loss': round(stop_loss, 2),
            'profit_target_percent': round(((take_profit - self.current_price) / self.current_price) * 100, 2),
            'risk_percent': round(((self.current_price - stop_loss) / self.current_price) * 100, 2),
            'risk_reward_ratio': round(
                ((take_profit - self.current_price) / (self.current_price - stop_loss)), 2
            ) if stop_loss != self.current_price else 0,
            'signals': signals,
            'signal_count': {
                'bullish': sum(1 for s in signals['technical'] if 'bullish' in s.lower()),
                'bearish': sum(1 for s in signals['technical'] if 'bearish' in s.lower()),
            }
        }
    
    def _analyze_technical_signals(self) -> Tuple[float, List[str]]:
        """Analyze technical indicators for trading signals"""
        score = 50  # Neutral baseline
        signals = []
        indicators = self.analysis_results['technical']
        
        # RSI analysis
        rsi = indicators.get('RSI', 50)
        if rsi < 30:
            signals.append("Oversold (RSI < 30) - Bullish reversal potential")
            score += 8
        elif rsi > 70:
            signals.append("Overbought (RSI > 70) - Bearish reversal potential")
            score -= 8
        elif rsi < 50:
            signals.append("RSI shows weakness")
            score -= 3
        else:
            signals.append("RSI shows strength")
            score += 3
        
        # MACD analysis
        macd = indicators.get('MACD', 0)
        macd_signal = indicators.get('MACD_SIGNAL', 0)
        if macd > macd_signal:
            signals.append("MACD bullish (above signal line)")
            score += 6
        else:
            signals.append("MACD bearish (below signal line)")
            score -= 6
        
        # Bollinger Bands analysis
        close = self.df['close'].iloc[-1]
        bb_upper = indicators.get('BB_UPPER', close)
        bb_lower = indicators.get('BB_LOWER', close)
        bb_middle = indicators.get('BB_MIDDLE', close)
        
        if close > bb_upper:
            signals.append("Price above Bollinger Bands (overbought)")
            score -= 5
        elif close < bb_lower:
            signals.append("Price below Bollinger Bands (oversold)")
            score += 5
        elif close > bb_middle:
            signals.append("Price above middle Bollinger Band")
            score += 3
        else:
            signals.append("Price below middle Bollinger Band")
            score -= 3
        
        # Moving Averages
        ma10 = indicators.get('MA10', close)
        ma20 = indicators.get('MA20', close)
        ma50 = indicators.get('MA50', close)
        
        if close > ma50 > ma20 > ma10:
            signals.append("Golden cross - Strong uptrend")
            score += 10
        elif close < ma50 < ma20 < ma10:
            signals.append("Death cross - Strong downtrend")
            score -= 10
        elif close > ma20:
            signals.append("Price above 20-MA - Bullish structure")
            score += 4
        else:
            signals.append("Price below 20-MA - Bearish structure")
            score -= 4
        
        # ADX analysis
        adx = indicators.get('ADX', 25)
        if adx > 50:
            signals.append("Strong trend (ADX > 50)")
            score += 5
        elif adx < 20:
            signals.append("Weak trend/Consolidation (ADX < 20)")
            score -= 2
        
        return max(0, min(100, score)), signals
    
    def _analyze_sr_signals(self) -> Tuple[float, List[str]]:
        """Analyze support and resistance for trading signals"""
        score = 50
        signals = []
        sr_data = self.analysis_results['support_resistance']
        
        support_nearby, support_dist = self.sr_analyzer.get_nearest_support(self.current_price)
        resistance_nearby, resistance_dist = self.sr_analyzer.get_nearest_resistance(self.current_price)
        
        if support_nearby:
            if support_dist < 1.0:
                signals.append(f"Very close to support (${support_nearby:.2f}, {support_dist:.2f}% away)")
                score += 7
            elif support_dist < 3.0:
                signals.append(f"Near support (${support_nearby:.2f}, {support_dist:.2f}% away)")
                score += 4
        
        if resistance_nearby:
            if resistance_dist < 1.0:
                signals.append(f"Very close to resistance (${resistance_nearby:.2f}, {resistance_dist:.2f}% away)")
                score -= 7
            elif resistance_dist < 3.0:
                signals.append(f"Near resistance (${resistance_nearby:.2f}, {resistance_dist:.2f}% away)")
                score -= 4
        
        if support_nearby and resistance_nearby:
            rr_range = (resistance_nearby - support_nearby) / self.current_price * 100
            if rr_range > 5:
                signals.append(f"Good risk/reward range between support and resistance")
                score += 5
            else:
                signals.append(f"Tight range between support and resistance")
                score -= 3
        
        return max(0, min(100, score)), signals
    
    def _analyze_ob_signals(self) -> Tuple[float, List[str]]:
        """Analyze order blocks for trading signals"""
        score = 50
        signals = []
        ob_data = self.analysis_results['order_blocks']
        
        if ob_data['bullish_count'] > 0:
            latest_bull = ob_data['bullish_blocks'][-1] if ob_data['bullish_blocks'] else None
            if latest_bull:
                signals.append(f"Bullish order block near ${latest_bull['low']:.2f}-${latest_bull['high']:.2f}")
                if self.current_price > latest_bull['high']:
                    score += 8
                elif abs(self.current_price - latest_bull['high']) / self.current_price * 100 < 2:
                    score += 5
        
        if ob_data['bearish_count'] > 0:
            latest_bear = ob_data['bearish_blocks'][-1] if ob_data['bearish_blocks'] else None
            if latest_bear:
                signals.append(f"Bearish order block near ${latest_bear['low']:.2f}-${latest_bear['high']:.2f}")
                if self.current_price < latest_bear['low']:
                    score -= 8
                elif abs(self.current_price - latest_bear['low']) / self.current_price * 100 < 2:
                    score -= 5
        
        return max(0, min(100, score)), signals
    
    def _analyze_liquidity_signals(self) -> Tuple[float, List[str]]:
        """Analyze liquidity for trading signals"""
        score = 50
        signals = []
        liq_data = self.analysis_results['liquidity']
        
        score_adjustment = (liq_data['liquidity_score'] - 50) * 0.5
        score += score_adjustment
        
        signals.append(f"Liquidity grade: {liq_data['liquidity_grade']}")
        signals.append(f"Volume trend: {liq_data['volume_trend']}")
        
        if liq_data['volume_vs_average'] > 1.5:
            signals.append(f"High volume activity ({liq_data['volume_vs_average']:.2f}x average)")
            score += 5
        elif liq_data['volume_vs_average'] < 0.5:
            signals.append(f"Low volume activity ({liq_data['volume_vs_average']:.2f}x average)")
            score -= 5
        
        if not liq_data['is_liquid']:
            signals.append("Low liquidity - Higher risk")
            score -= 10
        else:
            signals.append("Adequate liquidity")
            score += 3
        
        return max(0, min(100, score)), signals
    
    def _analyze_risk_reward(self) -> Tuple[float, List[str]]:
        """Analyze risk/reward setup"""
        score = 50
        signals = []
        
        support = self.sr_analyzer.get_nearest_support(self.current_price)[0]
        resistance = self.sr_analyzer.get_nearest_resistance(self.current_price)[0]
        
        if support and resistance:
            potential_upside = (resistance - self.current_price) / self.current_price * 100
            potential_downside = (self.current_price - support) / self.current_price * 100
            
            if potential_upside > potential_downside:
                rr_ratio = potential_upside / potential_downside
                signals.append(f"Favorable risk/reward ratio: {rr_ratio:.2f}:1")
                score += min(20, rr_ratio * 5)
            else:
                signals.append(f"Unfavorable risk/reward setup")
                score -= 10
        
        return max(0, min(100, score)), signals
    
    def _determine_action(self, score: float) -> Tuple[str, float]:
        """Determine BUY, SELL, or HOLD action"""
        confidence_threshold = RECOMMENDATION_CONFIG["CONFIDENCE_THRESHOLD"]
        
        if score >= 70:
            confidence = min(100, (score - 50) * 2)
            return "BUY", confidence
        elif score <= 30:
            confidence = min(100, (50 - score) * 2)
            return "SELL", confidence
        else:
            confidence = (50 - abs(score - 50)) * 2
            return "HOLD", confidence
    
    def _calculate_targets(self, action: str) -> Tuple[float, float]:
        """Calculate take profit and stop loss levels"""
        if action == "BUY":
            # Take profit: nearest resistance or ATR multiple
            resistance = self.sr_analyzer.get_nearest_resistance(self.current_price)[0]
            if resistance:
                take_profit = resistance
            else:
                atr = self.analysis_results['technical'].get('ATR', self.current_price * 0.02)
                take_profit = self.current_price + atr * 2
            
            # Stop loss: nearest support
            support = self.sr_analyzer.get_nearest_support(self.current_price)[0]
            if support:
                stop_loss = support * 0.995  # Slightly below support
            else:
                atr = self.analysis_results['technical'].get('ATR', self.current_price * 0.02)
                stop_loss = self.current_price - atr * 2
        
        elif action == "SELL":
            # Take profit: nearest support
            support = self.sr_analyzer.get_nearest_support(self.current_price)[0]
            if support:
                take_profit = support
            else:
                atr = self.analysis_results['technical'].get('ATR', self.current_price * 0.02)
                take_profit = self.current_price - atr * 2
            
            # Stop loss: nearest resistance
            resistance = self.sr_analyzer.get_nearest_resistance(self.current_price)[0]
            if resistance:
                stop_loss = resistance * 1.005  # Slightly above resistance
            else:
                atr = self.analysis_results['technical'].get('ATR', self.current_price * 0.02)
                stop_loss = self.current_price + atr * 2
        
        else:  # HOLD
            resistance = self.sr_analyzer.get_nearest_resistance(self.current_price)[0]
            support = self.sr_analyzer.get_nearest_support(self.current_price)[0]
            take_profit = resistance if resistance else self.current_price * 1.05
            stop_loss = support if support else self.current_price * 0.95
        
        return take_profit, stop_loss
    
    def print_recommendation(self):
        """Print formatted recommendation report"""
        if not self.recommendation:
            print("No recommendation available. Run run_full_analysis() first.")
            return
        
        rec = self.recommendation
        print(f"\n{'='*60}")
        print(f"RECOMMENDATION: {rec['action']}")
        print(f"{'='*60}")
        print(f"Current Price:        ${rec['current_price']:.2f}")
        print(f"Take Profit:          ${rec['take_profit']:.2f} (+{rec['profit_target_percent']:.2f}%)")
        print(f"Stop Loss:            ${rec['stop_loss']:.2f} (-{rec['risk_percent']:.2f}%)")
        print(f"Risk/Reward Ratio:    {rec['risk_reward_ratio']:.2f}:1")
        print(f"\nConfidence:           {rec['confidence']:.1f}%")
        print(f"Analysis Score:       {rec['score']:.1f}/100")
        print(f"Bullish Signals:      {rec['signal_count']['bullish']}")
        print(f"Bearish Signals:      {rec['signal_count']['bearish']}")
        
        print(f"\n{'─'*60}")
        print("DETAILED SIGNALS:")
        print(f"{'─'*60}")
        
        for category, signals in rec['signals'].items():
            if signals:
                print(f"\n{category.upper()}:")
                for signal in signals:
                    print(f"  • {signal}")
        
        print(f"\n{'='*60}\n")
    
    def _generate_strategy_recommendation(self) -> Dict:
        """
        Generate strategy-specific recommendation with dynamic weights
        
        Returns:
            Strategy-tuned recommendation with appropriate targets and confidence
        """
        weights = self.strategy_config.get('weights', {
            'technical': 0.35,
            'support_resistance': 0.25,
            'order_blocks': 0.20,
            'liquidity': 0.10,
            'risk_reward': 0.10,
        })
        
        score = 0
        signals = {
            'technical': [],
            'structure': [],
            'liquidity': [],
            'risk_reward': []
        }
        
        # Technical signals
        tech_score, tech_signals = self._analyze_technical_signals()
        score += tech_score * weights['technical']
        signals['technical'] = tech_signals
        
        # Support & Resistance signals
        sr_score, sr_signals = self._analyze_sr_signals()
        score += sr_score * weights['support_resistance']
        signals['structure'] = sr_signals
        
        # Order blocks signals
        ob_score, ob_signals = self._analyze_ob_signals()
        score += ob_score * weights['order_blocks']
        signals['structure'].extend(ob_signals)
        
        # Liquidity signals
        liq_score, liq_signals = self._analyze_liquidity_signals()
        score += liq_score * weights['liquidity']
        signals['liquidity'] = liq_signals
        
        # Risk/Reward signals
        rr_score, rr_signals = self._analyze_risk_reward()
        score += rr_score * weights['risk_reward']
        signals['risk_reward'] = rr_signals
        
        # Determine action and targets
        action, confidence = self._determine_strategy_action(score)
        take_profit, stop_loss = self._calculate_strategy_targets(action)
        
        # Calculate strategy-specific metrics
        profit_pct = ((take_profit - self.current_price) / self.current_price) * 100 if self.current_price > 0 else 0
        risk_pct = ((self.current_price - stop_loss) / self.current_price) * 100 if self.current_price > 0 else 0
        risk_reward_ratio = (profit_pct / risk_pct) if risk_pct > 0 else 0
        
        return {
            'action': action,
            'confidence': confidence,
            'score': round(score, 2),
            'strategy': self.strategy,
            'strategy_name': self.strategy_config['name'],
            'timeframe': self.strategy_config['timeframe'],
            'holding_period': self.strategy_config['holding_period'],
            'current_price': round(self.current_price, 2),
            'take_profit': round(take_profit, 2),
            'stop_loss': round(stop_loss, 2),
            'profit_target_percent': round(profit_pct, 2),
            'risk_percent': round(risk_pct, 2),
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'strategy_target_percent': self.strategy_config.get('profit_target_percent', 5.0),
            'strategy_stop_percent': self.strategy_config.get('stop_loss_percent', 2.0),
            'signals': signals,
            'signal_count': {
                'bullish': sum(1 for s in signals['technical'] if 'bullish' in s.lower()),
                'bearish': sum(1 for s in signals['technical'] if 'bearish' in s.lower()),
            },
            'weights': weights
        }
    
    def _determine_strategy_action(self, score: float) -> Tuple[str, float]:
        """Determine BUY, SELL, or HOLD action based on strategy"""
        confidence_threshold = self.strategy_config.get('confidence_threshold', 0.65)
        
        if score >= 70:
            confidence = min(100, (score - 50) * 2)
            return "BUY", confidence
        elif score <= 30:
            confidence = min(100, (50 - score) * 2)
            return "SELL", confidence
        else:
            confidence = (50 - abs(score - 50)) * 2
            return "HOLD", confidence
    
    def _calculate_strategy_targets(self, action: str) -> Tuple[float, float]:
        """Calculate strategy-specific take profit and stop loss"""
        strategy_tp_pct = self.strategy_config.get('profit_target_percent', 3.0) / 100
        strategy_sl_pct = self.strategy_config.get('stop_loss_percent', 1.0) / 100
        
        if action == "BUY":
            take_profit = self.current_price * (1 + strategy_tp_pct)
            stop_loss = self.current_price * (1 - strategy_sl_pct)
        elif action == "SELL":
            take_profit = self.current_price * (1 - strategy_tp_pct)
            stop_loss = self.current_price * (1 + strategy_sl_pct)
        else:  # HOLD
            take_profit = self.current_price * 1.05
            stop_loss = self.current_price * 0.95
        
        return take_profit, stop_loss


if __name__ == "__main__":
    engine = StockRecommendationEngine("AAPL", period="6mo", interval="1d")
    results = engine.run_full_analysis()
    engine.print_recommendation()
