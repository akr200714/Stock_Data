"""
Trading Strategy Configuration
Defines different trading strategies: Scalping, Intraday, BTST, Swing, Momentum
Each strategy has optimized parameters for its timeframe and risk profile
"""

STRATEGIES = {
    "scalping": {
        "name": "Scalping",
        "description": "Ultra-short term trading (45 seconds to 15 minutes). Tight stops, quick profits.",
        "chart_timeframe": "1 Min / 3 Min",
        "timeframe": "1-3 min",
        "holding_period": "45 seconds - 15 minutes",
        "data_period": "1d",  # Get 1 day of data
        "data_interval": "5m",  # 5-minute candles
        "technical_indicators": {
            "rsi_period": 9,  # Faster RSI
            "rsi_overbought": 75,
            "rsi_oversold": 25,
            "macd_fast": 5,  # Faster MACD
            "macd_slow": 13,
            "macd_signal": 3,
            "bollinger_period": 14,
            "bollinger_std": 1.5,  # Tighter bands
            "atr_period": 7,
            "adx_period": 7,  # Faster ADX
        },
        "support_resistance": {
            "lookback_period": 50,  # Recent levels more important
            "min_touches": 1,  # Even single touches matter
            "tolerance_percent": 0.3,  # Tighter tolerance
        },
        "order_blocks": {
            "lookback_period": 50,
            "min_candles": 2,
            "break_distance": 0.01,  # 1% break
        },
        "liquidity": {
            "volume_ma_period": 10,  # Shorter MA
            "min_liquidity_volume": 50000,  # Lower thresholds
        },
        "profit_target_percent": 0.35,  # 0.20%-0.50% range (using middle 0.35%)
        "stop_loss_percent": 0.18,  # 0.10%-0.25% range (using middle 0.18%)
        "risk_reward_ratio": 2.0,
        "confidence_threshold": 0.70,  # 65-70% win rate required
        "min_win_rate": 0.65,  # Minimum 65% win rate
        "best_asset_class": "High-volume Large Caps, Major Forex Pairs, Crypto",
        "execution_window": "Peak morning volume (First 90 minutes of session)",
        "weights": {
            "technical": 0.50,  # Technical is most important
            "support_resistance": 0.20,
            "order_blocks": 0.15,
            "liquidity": 0.10,
            "risk_reward": 0.05,
        }
    },
    
    "intraday": {
        "name": "Intraday",
        "description": "Same-day trading (1-5 hour hold). Moderate risk, regular profits.",
        "chart_timeframe": "5 Min / 15 Min",
        "timeframe": "1-5 hours",
        "holding_period": "1-5 hours",
        "data_period": "20d",
        "data_interval": "5m",  # 5-minute candles for intraday
        "technical_indicators": {
            "rsi_period": 12,
            "rsi_overbought": 70,
            "rsi_oversold": 30,
            "macd_fast": 10,
            "macd_slow": 24,
            "macd_signal": 8,
            "bollinger_period": 18,
            "bollinger_std": 2.0,
            "atr_period": 12,
            "adx_period": 12,
        },
        "support_resistance": {
            "lookback_period": 50,
            "min_touches": 2,
            "tolerance_percent": 0.4,
        },
        "order_blocks": {
            "lookback_period": 50,
            "min_candles": 3,
            "break_distance": 0.015,  # 1.5% break
        },
        "liquidity": {
            "volume_ma_period": 15,
            "min_liquidity_volume": 100000,
        },
        "profit_target_percent": 1.15,  # 0.80%-1.50% range (using middle 1.15%)
        "stop_loss_percent": 0.58,  # 0.40%-0.75% range (using middle 0.58%)
        "risk_reward_ratio": 2.0,
        "confidence_threshold": 0.65,  # 50-55% win rate required
        "min_win_rate": 0.50,  # Minimum 50% win rate
        "best_asset_class": "Nifty 50 / Liquid Mid-caps, Index Futures",
        "execution_window": "Throughout the live session (Exit 30 mins before close)",
        "weights": {
            "technical": 0.40,
            "support_resistance": 0.25,
            "order_blocks": 0.20,
            "liquidity": 0.10,
            "risk_reward": 0.05,
        }
    },
    
    "btst": {
        "name": "BTST (Buy Today Sell Tomorrow)",
        "description": "Overnight holding (buy near close, sell next open/early). Momentum-based.",
        "chart_timeframe": "15 Min / 1 Hour",
        "timeframe": "15 Min - 1 Hour",
        "holding_period": "15 hours (overnight)",
        "data_period": "30d",
        "data_interval": "15m",  # 15-minute candles for BTST setup
        "technical_indicators": {
            "rsi_period": 13,
            "rsi_overbought": 70,
            "rsi_oversold": 30,
            "macd_fast": 11,
            "macd_slow": 25,
            "macd_signal": 8,
            "bollinger_period": 19,
            "bollinger_std": 2.0,
            "atr_period": 13,
            "adx_period": 13,
        },
        "support_resistance": {
            "lookback_period": 50,
            "min_touches": 2,
            "tolerance_percent": 0.5,
        },
        "order_blocks": {
            "lookback_period": 50,
            "min_candles": 3,
            "break_distance": 0.02,  # 2% break
        },
        "liquidity": {
            "volume_ma_period": 15,
            "min_liquidity_volume": 150000,
        },
        "profit_target_percent": 1.20,  # 1.2% target (standard)
        "stop_loss_percent": 0.80,  # 0.8% stop (standard)
        "risk_reward_ratio": 1.5,
        "confidence_threshold": 0.65,  # 55% win rate required
        "min_win_rate": 0.55,  # Minimum 55% win rate
        "momentum_strength_threshold": 0.70,  # Strong momentum needed
        "best_asset_class": "Strong Sector Stocks",
        "execution_window": "Final 15-30 minutes of trading day",
        "weights": {
            "technical": 0.45,
            "support_resistance": 0.20,
            "order_blocks": 0.15,
            "liquidity": 0.15,
            "risk_reward": 0.05,
        }
    },
    
    "swing": {
        "name": "Swing Trading",
        "description": "Medium-term holding (2-7 days). Strong trends, good risk/reward.",
        "chart_timeframe": "1 Hour / Daily",
        "timeframe": "1 Hour - Daily",
        "holding_period": "2 Days - 1 Week",
        "data_period": "6mo",
        "data_interval": "1h",  # Hourly candles for swing trading
        "technical_indicators": {
            "rsi_period": 14,  # Standard
            "rsi_overbought": 70,
            "rsi_oversold": 30,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "bollinger_period": 20,
            "bollinger_std": 2.0,
            "atr_period": 14,
            "adx_period": 14,
        },
        "support_resistance": {
            "lookback_period": 100,  # Longer lookback for swing levels
            "min_touches": 2,
            "tolerance_percent": 0.5,
        },
        "order_blocks": {
            "lookback_period": 100,
            "min_candles": 3,
            "break_distance": 0.02,
        },
        "liquidity": {
            "volume_ma_period": 20,
            "min_liquidity_volume": 500000,
        },
        "profit_target_percent": 6.0,  # 4.00%-8.00% range (using middle 6%)
        "stop_loss_percent": 2.0,  # 1.50%-2.50% range (using middle 2%)
        "risk_reward_ratio": 3.0,
        "confidence_threshold": 0.65,  # 45-50% win rate required
        "min_win_rate": 0.45,  # Minimum 45% win rate
        "best_asset_class": "All Mid & Large Caps, Sector ETFs, Commodities",
        "execution_window": "EOD (End of Day) analysis, entry on key structural retests",
        "weights": {
            "technical": 0.35,
            "support_resistance": 0.30,
            "order_blocks": 0.20,
            "liquidity": 0.10,
            "risk_reward": 0.05,
        }
    },
    
    "momentum": {
        "name": "Momentum Trading",
        "description": "Trend-following (5+ days). Strong directional moves, larger targets.",
        "chart_timeframe": "Daily / Weekly",
        "timeframe": "Daily - Weekly",
        "holding_period": "5 Days - 3 Weeks",
        "data_period": "1y",
        "data_interval": "1d",  # Daily candles
        "technical_indicators": {
            "rsi_period": 14,
            "rsi_overbought": 65,  # Less extreme
            "rsi_oversold": 35,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "bollinger_period": 20,
            "bollinger_std": 2.0,
            "atr_period": 14,
            "adx_period": 14,
        },
        "support_resistance": {
            "lookback_period": 200,  # Long-term levels
            "min_touches": 2,
            "tolerance_percent": 0.5,
        },
        "order_blocks": {
            "lookback_period": 200,
            "min_candles": 3,
            "break_distance": 0.02,
        },
        "liquidity": {
            "volume_ma_period": 20,
            "min_liquidity_volume": 1000000,  # High volume requirement
        },
        "profit_target_percent": 15.0,  # 10.00%-20.00% range (using middle 15%)
        "stop_loss_percent": 4.0,  # 3.50%-5.00% range (using middle 4%)
        "risk_reward_ratio": 3.75,
        "confidence_threshold": 0.60,  # 35-40% win rate required
        "min_win_rate": 0.35,  # Minimum 35% win rate
        "trend_strength_threshold": 0.75,  # Strong trend needed
        "best_asset_class": "High-Beta Growth Stocks, Breakouts at All-Time Highs",
        "execution_window": "Anytime during structural daily breakout confirmation",
        "weights": {
            "technical": 0.30,
            "support_resistance": 0.25,
            "order_blocks": 0.20,
            "liquidity": 0.15,
            "risk_reward": 0.10,
        }
    },
}


def get_strategy_config(strategy: str) -> dict:
    """
    Get configuration for a specific strategy
    
    Args:
        strategy: Strategy name (scalping, intraday, btst, swing, momentum)
        
    Returns:
        Strategy configuration dictionary
    """
    strategy_lower = strategy.lower()
    if strategy_lower not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy}. Available: {list(STRATEGIES.keys())}")
    return STRATEGIES[strategy_lower]


def list_all_strategies() -> dict:
    """Get all available strategies"""
    return {name: strategy["description"] for name, strategy in STRATEGIES.items()}


def get_strategy_details(strategy: str) -> dict:
    """Get full details for a strategy"""
    return get_strategy_config(strategy)


# Quick reference for trading parameters by strategy
STRATEGY_QUICK_REFERENCE = {
    "scalping": "5-15 min | 0.75% target | 0.35% stop | ₹₹ Tight | Ultra-fast",
    "intraday": "1-4 hours | 1.5% target | 0.75% stop | ₹₹ Moderate | Same day",
    "btst": "Overnight | 1.2% target | 0.8% stop | ₹₹ Momentum | Close to open",
    "swing": "2-5 days | 3% target | 1.5% stop | ₹₹₹ Strong | Mid-term",
    "momentum": "5+ days | 5% target | 2% stop | ₹₹₹₹ Trend | Long-term",
}


if __name__ == "__main__":
    print("Available Trading Strategies:")
    print("=" * 70)
    for name, details in STRATEGY_QUICK_REFERENCE.items():
        print(f"\n{name.upper():12s} | {details}")
    print("\n" + "=" * 70)
