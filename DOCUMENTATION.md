# Stock Recommendation AI Agent

A sophisticated AI-powered stock analysis and recommendation system that analyzes technical indicators, support/resistance levels, order blocks, liquidity, and price action to generate precise investment recommendations.

## 📊 Features

### Advanced Technical Analysis
- **Indicators**: RSI, MACD, Bollinger Bands, ADX, ATR, Stochastic Oscillator
- **Moving Averages**: 10, 20, 50, 100, 200 period MAs
- **Volume Analysis**: On-Balance Volume (OBV), Volume Moving Average

### Price Action Analysis
- **Support & Resistance**: Automatic identification of key price levels
- **Order Blocks**: Detection of bullish and bearish order blocks
- **Liquidity Analysis**: Volume profile and liquidity grading (A+ to D)

### AI Recommendation Engine
- **Multi-factor Scoring**: Weighted analysis across 5 key dimensions
- **Precise Targets**: Calculated take profit and stop loss levels
- **Risk/Reward Ratios**: Quantified risk assessment
- **Confidence Scoring**: 0-100% confidence ratings

### Visualization
- **Technical Charts**: Multi-panel analysis charts with all indicators
- **Order Block Charts**: Visual representation of price action levels
- **Real-time Updates**: Chart generation with latest data

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Stock_Data.git
cd Stock_Data

# Install dependencies
pip install -r requirements.txt
```

### Command Line Interface

```bash
# Analyze a single stock
python cli.py -s AAPL

# Analyze with custom timeframe
python cli.py -s MSFT -p 6mo -i 1d

# Generate technical analysis charts
python cli.py -s TSLA --chart

# Compare multiple stocks
python cli.py -s AAPL MSFT GOOGL

# Output as JSON
python cli.py -s AAPL --json
```

### API Server

```bash
# Start the Flask server
python api_server.py

# Server runs on http://localhost:5000
```

#### API Endpoints

**Health Check**
```bash
curl http://localhost:5000/api/health
```

**Analyze Stock**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "period": "1y", "interval": "1d", "generate_chart": true}'
```

**Get Recommendation**
```bash
curl http://localhost:5000/api/recommendation/AAPL
```

**Compare Multiple Stocks**
```bash
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"], "period": "1y"}'
```

**Get Technical Indicators**
```bash
curl http://localhost:5000/api/indicators/AAPL?period=1y&interval=1d
```

**Get Support & Resistance Levels**
```bash
curl http://localhost:5000/api/levels/AAPL
```

**Get Order Blocks**
```bash
curl http://localhost:5000/api/orderblocks/AAPL
```

**Get Liquidity Analysis**
```bash
curl http://localhost:5000/api/liquidity/AAPL
```

## 📈 Analysis Framework

### Scoring System (Weighted)

1. **Technical Indicators (35%)**
   - RSI (oversold/overbought)
   - MACD crossovers
   - Bollinger Bands positioning
   - Moving average alignment
   - ADX trend strength

2. **Price Structure (25%)**
   - Distance to support/resistance
   - Risk/reward range
   - Level confirmation touches

3. **Order Blocks (20%)**
   - Bullish order block proximity
   - Bearish order block proximity
   - Block confirmation

4. **Liquidity (10%)**
   - Average volume
   - Current vs average volume ratio
   - Volume trend direction

5. **Risk/Reward (10%)**
   - Support/resistance distance
   - Potential upside vs downside
   - Position quality

### Recommendation Output

```json
{
  "action": "BUY|SELL|HOLD",
  "confidence": 75.5,
  "score": 72.3,
  "current_price": 150.25,
  "take_profit": 158.50,
  "stop_loss": 147.00,
  "profit_target_percent": 5.47,
  "risk_percent": 2.16,
  "risk_reward_ratio": 2.53,
  "signals": {
    "technical": [...],
    "structure": [...],
    "liquidity": [...]
  }
}
```

## 📊 Module Documentation

### `data_handler.py`
Handles data retrieval and preprocessing from Yahoo Finance or CSV files.

```python
from data_handler import StockDataHandler

handler = StockDataHandler("AAPL", period="1y", interval="1d")
df = handler.fetch_data()
```

### `technical_analysis.py`
Calculates 9+ technical indicators.

```python
from technical_analysis import TechnicalAnalyzer

analyzer = TechnicalAnalyzer(df)
indicators = analyzer.calculate_all_indicators()
latest = analyzer.get_latest_indicators()
```

### `support_resistance.py`
Identifies key support and resistance levels.

```python
from support_resistance import SupportResistanceAnalyzer

sr_analyzer = SupportResistanceAnalyzer(df)
levels = sr_analyzer.find_levels()
support, distance = sr_analyzer.get_nearest_support(current_price)
```

### `order_blocks.py`
Detects order blocks from price action.

```python
from order_blocks import OrderBlockAnalyzer

ob_analyzer = OrderBlockAnalyzer(df)
blocks = ob_analyzer.find_order_blocks()
```

### `liquidity_analysis.py`
Analyzes market liquidity and volume profiles.

```python
from liquidity_analysis import LiquidityAnalyzer

liq_analyzer = LiquidityAnalyzer(df)
liquidity = liq_analyzer.analyze_liquidity()
vwap = liq_analyzer.get_volume_weighted_price()
```

### `recommendation_engine.py`
Main engine combining all analyses.

```python
from recommendation_engine import StockRecommendationEngine

engine = StockRecommendationEngine("AAPL")
results = engine.run_full_analysis()
engine.print_recommendation()
```

### `chart_generator.py`
Generates professional analysis charts.

```python
from chart_generator import ChartGenerator

generator = ChartGenerator("AAPL", df)
generator.generate_main_chart(indicators, sr_levels, price, recommendation)
generator.generate_order_blocks_chart(ob_data)
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Technical indicators periods
INDICATORS_CONFIG = {
    "RSI_PERIOD": 14,
    "MACD_FAST": 12,
    "BOLLINGER_PERIOD": 20,
    # ...
}

# Support & Resistance detection
SR_CONFIG = {
    "LOOKBACK_PERIOD": 50,
    "MIN_TOUCHES": 2,
    "TOLERANCE_PERCENT": 0.5,
}

# Recommendation thresholds
RECOMMENDATION_CONFIG = {
    "CONFIDENCE_THRESHOLD": 0.65,
    "MIN_SCORE": 40,
}
```

## 📈 Example Workflow

```python
from recommendation_engine import StockRecommendationEngine

# Create engine
engine = StockRecommendationEngine("AAPL", period="6mo", interval="1d")

# Run analysis
results = engine.run_full_analysis()

# Access recommendation
rec = results['recommendation']
print(f"Action: {rec['action']}")
print(f"Take Profit: ${rec['take_profit']:.2f}")
print(f"Stop Loss: ${rec['stop_loss']:.2f}")
print(f"Confidence: {rec['confidence']:.1f}%")

# Get detailed signals
for signal in rec['signals']['technical']:
    print(f"  • {signal}")
```

## 📋 Supported Timeframes

- **Daily**: 1d
- **Weekly**: 1wk
- **Monthly**: 1mo
- **Intraday**: 1m, 5m, 15m, 30m, 60m

Historical periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y

## 🎯 Recommendation Signals

### BUY Signals (Action = "BUY")
- Multiple bullish technical confirmations
- Price near support levels
- Bullish order block proximity
- Favorable risk/reward ratio
- Increasing volume

### SELL Signals (Action = "SELL")
- Multiple bearish technical confirmations
- Price near resistance levels
- Bearish order block proximity
- Unfavorable risk/reward ratio
- Decreasing volume

### HOLD Signals (Action = "HOLD")
- Mixed technical signals
- Consolidation pattern
- Unclear price structure
- Low confidence

## ⚠️ Risk Disclaimer

This tool provides analysis and recommendations for educational purposes. Always conduct your own research and consult with a financial advisor before making investment decisions. Past performance does not guarantee future results.

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Note**: This agent requires an internet connection to fetch stock data from Yahoo Finance. Ensure proper API rate limiting when making multiple requests.
