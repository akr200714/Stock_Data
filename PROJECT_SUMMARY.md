# Stock Recommendation AI Agent - Project Summary

## 📋 Project Overview

This is a production-ready AI-powered stock recommendation system that analyzes market data, technical indicators, price action, and liquidity to generate precise investment recommendations with specific entry/exit targets and risk management levels.

## 🎯 Core Capabilities

### 1. Technical Analysis Engine
- **9+ Indicators**: RSI, MACD, Bollinger Bands, ATR, ADX, Stochastic, Moving Averages
- **Trend Analysis**: Multi-timeframe moving average alignment
- **Momentum**: RSI oversold/overbought detection, Stochastic oscillator
- **Volatility**: Bollinger Bands and ATR for volatility measurement

### 2. Price Action Analysis
- **Support & Resistance**: Automatic detection of key price levels
- **Order Blocks**: Identification of bullish and bearish order blocks
- **Trend Structures**: Impulsive moves and consolidation patterns
- **Level Confirmation**: Multiple touch validation

### 3. Liquidity Analysis
- **Volume Profiling**: High-volume price level identification
- **VWAP Calculation**: Volume-weighted average price
- **Liquidity Grading**: A+ to D grading system
- **Volume Trend**: Increasing/decreasing volume patterns

### 4. AI Recommendation Engine
- **Multi-factor Scoring**: Weighted analysis across 5 dimensions (35%-35%-20%-10%-10%)
- **Confidence Ratings**: 0-100% confidence based on signal alignment
- **Precise Targets**: Take profit calculated from resistance levels
- **Risk Management**: Stop loss from support levels with ATR confirmation
- **Risk/Reward Ratios**: Quantified position quality (e.g., 2.5:1)

## 📂 Project Structure

```
Stock_Data/
│
├── Core Analysis Modules
│   ├── data_handler.py           # Data fetching & preprocessing
│   ├── technical_analysis.py     # Technical indicators
│   ├── support_resistance.py     # SR level detection
│   ├── order_blocks.py           # Order block analysis
│   ├── liquidity_analysis.py     # Liquidity metrics
│   └── recommendation_engine.py  # Main AI engine
│
├── User Interfaces
│   ├── cli.py                    # Command-line interface
│   ├── api_server.py             # Flask REST API
│   └── chart_generator.py        # Technical charts
│
├── Configuration & Examples
│   ├── config.py                 # All settings & parameters
│   ├── examples.py               # 7 usage examples
│   ├── quickstart.py             # Setup & testing
│   └── .env.example              # Environment variables
│
├── Deployment
│   ├── requirements.txt          # Python dependencies
│   ├── Makefile                  # Build commands
│   ├── Dockerfile                # Container image
│   └── docker-compose.yml        # Multi-container setup
│
└── Documentation
    ├── README.md                 # Quick start guide
    └── DOCUMENTATION.md          # Full documentation
```

## 🚀 Getting Started (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Quick Start
```bash
python quickstart.py
```

### Step 3: Analyze Your First Stock
```bash
# CLI
python cli.py -s AAPL --chart

# OR API
python api_server.py
# Then: curl http://localhost:5000/api/analyze -X POST -H "Content-Type: application/json" -d '{"symbol":"AAPL"}'
```

## 📊 Recommendation Output Format

```json
{
  "action": "BUY",
  "confidence": 78.5,
  "score": 74.3,
  "current_price": 150.25,
  "take_profit": 158.50,
  "stop_loss": 147.00,
  "profit_target_percent": 5.47,
  "risk_percent": 2.16,
  "risk_reward_ratio": 2.53,
  "signals": {
    "technical": [
      "Oversold (RSI < 30) - Bullish reversal potential",
      "MACD bullish (above signal line)",
      "Price below lower Bollinger Band (oversold)",
      ...
    ],
    "structure": [
      "Very close to support ($147.50, 0.5% away)",
      ...
    ],
    "liquidity": [
      "Liquidity grade: A",
      ...
    ]
  }
}
```

## 🛠️ Usage Modes

### 1. Command Line Interface (CLI)
```bash
# Single stock
python cli.py -s AAPL

# With charts
python cli.py -s AAPL --chart

# Multiple stocks
python cli.py -s AAPL MSFT GOOGL

# Custom timeframe
python cli.py -s AAPL -p 3mo -i 1d

# JSON output
python cli.py -s AAPL --json
```

### 2. REST API Server
```bash
python api_server.py
# Endpoints:
# POST   /api/analyze
# GET    /api/recommendation/<symbol>
# GET    /api/indicators/<symbol>
# GET    /api/levels/<symbol>
# GET    /api/orderblocks/<symbol>
# GET    /api/liquidity/<symbol>
# POST   /api/compare
```

### 3. Python Integration
```python
from recommendation_engine import StockRecommendationEngine

engine = StockRecommendationEngine("AAPL")
results = engine.run_full_analysis()
engine.print_recommendation()
```

### 4. Makefile Commands
```bash
make install          # Install dependencies
make quickstart       # Run setup tests
make run-aapl        # Analyze AAPL with chart
make run-compare     # Compare stocks
make run-api         # Start API server
make run-examples    # Run examples
```

## 📈 Analysis Scoring Breakdown

| Component | Weight | Factors |
|-----------|--------|---------|
| Technical Indicators | 35% | RSI, MACD, Bollinger, ADX, ATR, Stochastic, MAs |
| Price Structure | 25% | Support/Resistance distance, Order Blocks |
| Order Blocks | 20% | Bullish/Bearish block proximity |
| Liquidity | 10% | Volume grade, Volume trend, Volume ratio |
| Risk/Reward | 10% | Position quality, TP/SL ratio |

**Final Score**: 0-100 → Converted to **BUY/SELL/HOLD** with **Confidence %**

## 🎯 Key Features

✅ **Precise Entry/Exit Points**
- Calculated from support/resistance levels
- ATR confirmation for volatility
- Order block alignment

✅ **Risk Management**
- Automatic stop loss placement
- Risk/reward ratio calculation
- Position sizing recommendations

✅ **Multiple Analysis Dimensions**
- Technical indicators (trends, momentum, volatility)
- Price action (levels, blocks, structures)
- Volume analysis (liquidity, confirmation)
- Market structure (support, resistance, order blocks)

✅ **Professional Output**
- Confidence-weighted recommendations
- Detailed signal list for each recommendation
- Professional technical analysis charts
- JSON API for system integration

✅ **Flexible Input/Output**
- CLI for quick analysis
- REST API for integrations
- JSON export for data pipelines
- Multiple chart formats

## 📊 Supported Data

### Timeframes
- **Intraday**: 1m, 5m, 15m, 30m, 60m (requires -i flag)
- **Daily**: 1d (default)
- **Weekly**: 1wk
- **Monthly**: 1mo

### Historical Periods
- 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y

### Data Source
- Yahoo Finance (free, no API key needed)
- CSV file import (via CSVDataHandler)

## 🔧 Configuration

All settings in `config.py`:
- Indicator periods (RSI, MACD, Bollinger, etc.)
- Support/Resistance sensitivity
- Order block detection parameters
- Liquidity thresholds
- Recommendation confidence levels

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/health | Server health check |
| POST | /api/analyze | Analyze single stock |
| GET | /api/recommendation/<symbol> | Get cached recommendation |
| GET | /api/indicators/<symbol> | Get technical indicators |
| GET | /api/levels/<symbol> | Get support/resistance levels |
| GET | /api/orderblocks/<symbol> | Get order blocks |
| GET | /api/liquidity/<symbol> | Get liquidity analysis |
| POST | /api/compare | Compare multiple stocks |
| GET | /api/cache | View cache status |
| DELETE | /api/cache/<symbol> | Clear cache for symbol |

## 🐳 Docker Deployment

```bash
# Build image
docker build -t stock-agent .

# Run container
docker run -p 5000:5000 stock-agent

# OR with docker-compose
docker-compose up -d
```

## 📚 Example Use Cases

### 1. Quick Stock Check
```bash
python cli.py -s AAPL
```

### 2. Generate Trading Charts
```bash
python cli.py -s AAPL --chart
```

### 3. Screen Multiple Stocks
```bash
python cli.py -s AAPL MSFT GOOGL AMZN NVDA
```

### 4. Intraday Analysis
```bash
python cli.py -s AAPL -p 3mo -i 4h
```

### 5. Automated Integration
```bash
# Start API server
python api_server.py

# Query from any language
curl http://localhost:5000/api/analyze -X POST \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","period":"1y"}'
```

## ⚙️ System Requirements

- Python 3.8+
- ~200MB for dependencies
- Internet connection (for data fetching)
- 2GB RAM (recommended)

## 📈 Performance

- **Analysis Time**: ~2-5 seconds per stock
- **API Response**: ~3-8 seconds first time, <1s cached
- **Chart Generation**: ~5-10 seconds per chart
- **Batch Processing**: Can analyze 10+ stocks sequentially

## 🔐 Security Notes

- No sensitive data stored
- No API keys required (Yahoo Finance)
- No trading execution capability
- Educational/analysis only

## ⚠️ Disclaimer

This tool is for **educational and analytical purposes only**. It is not financial advice. Always:
- Do your own research
- Consult a financial advisor
- Never risk more than you can afford to lose
- Past performance ≠ future results

## 📝 Output Examples

### CLI Output
```
============================================================
RECOMMENDATION: BUY
============================================================
Current Price:        $150.25
Take Profit:          $158.50 (+5.47%)
Stop Loss:            $147.00 (-2.16%)
Risk/Reward Ratio:    2.53:1

Confidence:           78.5%
Analysis Score:       74.3/100
Bullish Signals:      12
Bearish Signals:      2
```

### JSON Output
```json
{
  "symbol": "AAPL",
  "current_price": 150.25,
  "recommendation": {
    "action": "BUY",
    "confidence": 78.5,
    "score": 74.3,
    "take_profit": 158.50,
    "stop_loss": 147.00,
    "risk_reward_ratio": 2.53
  }
}
```

## 🚀 Future Enhancement Ideas

- Real-time data streaming
- Machine learning model optimization
- Multi-market analysis
- Options strategy recommendations
- Portfolio analysis
- Risk management alerts
- Trading bot integration
- Mobile app

## 📞 Support & Documentation

- **Full Docs**: See [DOCUMENTATION.md](DOCUMENTATION.md)
- **Examples**: Run [examples.py](examples.py)
- **Setup**: Run [quickstart.py](quickstart.py)
- **Issues**: Create GitHub issue

---

**Stock Recommendation AI Agent v1.0** - Professional-Grade Technical Analysis System
