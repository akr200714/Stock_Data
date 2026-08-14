"""
Configuration for Stock Recommendation AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Breeze Connect Configuration (Real-time Market Data)
BREEZE_API_KEY = os.getenv("BREEZE_API_KEY", "your-breeze-api-key")
BREEZE_SECRET_KEY = os.getenv("BREEZE_SECRET_KEY", "your-breeze-secret-key")
BREEZE_SESSION_KEY = os.getenv("BREEZE_SESSION_KEY", "")  # Will be generated on login
BREEZE_USE_PRODUCTION = os.getenv("BREEZE_USE_PRODUCTION", "True").lower() == "true"

# Technical Analysis Configuration
INDICATORS_CONFIG = {
    "RSI_PERIOD": 14,
    "MACD_FAST": 12,
    "MACD_SLOW": 26,
    "MACD_SIGNAL": 9,
    "BOLLINGER_PERIOD": 20,
    "BOLLINGER_STD": 2,
    "ADX_PERIOD": 14,
    "ATR_PERIOD": 14,
}

# Support & Resistance Configuration
SR_CONFIG = {
    "LOOKBACK_PERIOD": 50,
    "MIN_TOUCHES": 2,
    "TOLERANCE_PERCENT": 0.5,
}

# Liquidity Configuration
LIQUIDITY_CONFIG = {
    "VOLUME_MA_PERIOD": 20,
    "MIN_LIQUIDITY_VOLUME": 1000000,  # Minimum daily volume
}

# Order Blocks Configuration
ORDER_BLOCKS_CONFIG = {
    "LOOKBACK_PERIOD": 50,
    "MIN_CANDLES": 3,
    "BREAK_DISTANCE": 0.02,  # 2% break distance
}

# Recommendation Configuration
RECOMMENDATION_CONFIG = {
    "CONFIDENCE_THRESHOLD": 0.65,
    "MIN_SCORE": 40,  # Out of 100
    "PRICE_TARGET_PERCENT": 5.0,  # Default 5% target
}

# Timeframes
TIMEFRAMES = ["1h", "4h", "1d", "1wk"]
