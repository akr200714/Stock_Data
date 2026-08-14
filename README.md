# 📊 Stock Recommendation AI Agent

An advanced, AI-powered stock analysis system that combines technical analysis, price action, liquidity analysis, and machine learning to generate precise investment recommendations with specific entry/exit targets.

## 🎯 Key Features

✅ **Real-time Data from Breeze Connect** - Low-latency market data feed
✅ **Real-time Technical Analysis** - 9+ indicators (RSI, MACD, Bollinger Bands, etc.)
✅ **Support & Resistance Detection** - Automatic key level identification
✅ **Order Block Analysis** - Bullish and bearish order blocks
✅ **Liquidity Scoring** - A+ to D grading system
✅ **Precise Recommendations** - BUY/SELL/HOLD with exact targets
✅ **Risk/Reward Calculation** - Quantified position sizing
✅ **Professional Charts** - Multi-panel technical analysis visualization
✅ **REST API** - Easy integration for automated trading
✅ **CLI Tool** - Command-line interface for quick analysis
✅ **Batch Analysis** - Compare multiple stocks simultaneously

## 🚀 Quick Start

### 1. Setup Breeze Connect (Real-time Data)

Get your API credentials from [Angel Broking Breeze](https://www.angelbroking.com/breeze/)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Breeze credentials
# BREEZE_API_KEY=your-key
# BREEZE_SECRET_KEY=your-secret
```

See [BREEZE_SETUP.md](BREEZE_SETUP.md) for detailed setup instructions.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Setup

```bash
python quickstart.py
```

### 4. Analyze Stocks (NSE Format)

```bash
# Simple analysis
python cli.py -s SBIN-EQ

# With chart generation
python cli.py -s SBIN-EQ --chart

# Compare multiple stocks
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ

# JSON output
python cli.py -s SBIN-EQ --json
```

### 5. Start API Server

```bash
python api_server.py
# API available at http://localhost:5000
```

## 📊 What It Analyzes

| Category | Components |
|----------|-----------|
| **Technical** | RSI, MACD, Bollinger Bands, ADX, ATR, Stochastic, MAs |
| **Price Action** | Support/Resistance, Order Blocks, Trend Structure |
| **Volume** | OBV, Volume MA, VWAP, Volume Clusters |
| **Liquidity** | Volume Analysis, Liquidity Grade, Price-Volume Correlation |
| **Risk/Reward** | TP/SL Calculation, Risk Ratios, Position Quality |

## 📈 Output Example

```
RECOMMENDATION: BUY
Current Price:        ₹450.25
Take Profit:          ₹475.50 (+5.61%)
Stop Loss:            ₹440.00 (-2.27%)
Risk/Reward Ratio:    2.47:1

Confidence:           78.5%
Analysis Score:       74.3/100
Bullish Signals:      12
Bearish Signals:      2
```

## 🛠️ Project Structure

```
Stock_Data/
├── config.py                  # Configuration & parameters
├── data_handler.py            # Breeze Connect data fetching
├── technical_analysis.py      # Technical indicators
├── support_resistance.py      # SR level detection
├── order_blocks.py            # Order block analysis
├── liquidity_analysis.py      # Liquidity metrics
├── recommendation_engine.py   # Main AI engine
├── chart_generator.py         # Visualization
├── cli.py                     # Command-line interface
├── api_server.py              # Flask REST API
├── requirements.txt           # Dependencies
├── BREEZE_SETUP.md            # Breeze Connect setup
├── DOCUMENTATION.md           # Full documentation
└── README.md                  # This file
```

## 📡 API Endpoints

```bash
POST   /api/analyze              # Analyze a stock
POST   /api/compare              # Compare multiple stocks
GET    /api/recommendation/<symbol>  # Get recommendation
GET    /api/indicators/<symbol>  # Get technical indicators
GET    /api/levels/<symbol>      # Get support/resistance
GET    /api/orderblocks/<symbol> # Get order blocks
GET    /api/liquidity/<symbol>   # Get liquidity analysis
```

## 💡 How It Works

1. **Real-time Data Ingestion** - Fetches data from Breeze Connect API
2. **Technical Analysis** - Calculates 9+ technical indicators
3. **Price Structure** - Identifies support, resistance, and order blocks
4. **Liquidity Check** - Analyzes volume and market depth
5. **Signal Generation** - Combines all analyses into weighted score
6. **Recommendation** - Generates BUY/SELL/HOLD with targets (precise numbers)
7. **Visualization** - Creates professional trading charts

## 📊 Scoring Breakdown

| Factor | Weight | Details |
|--------|--------|---------|
| Technical Indicators | 35% | RSI, MACD, Bollinger, ADX, etc. |
| Price Structure | 25% | Support/Resistance + Order Blocks |
| Liquidity | 10% | Volume analysis & grading |
| Risk/Reward | 10% | Position quality metrics |

**Final Score**: 0-100 → Action with Confidence %

## ⚙️ Configuration

All parameters in `config.py`:
- Indicator periods (RSI, MACD, etc.)
- Support/Resistance detection sensitivity
- Order block lookback periods
- Minimum liquidity thresholds
- Recommendation confidence levels

## 📦 Requirements

- Python 3.8+
- pandas, numpy, scikit-learn
- ta-lib (technical analysis)
- breeze-connect (real-time data)
- Flask (API server)
- matplotlib (charts)

See requirements.txt for complete list.

## 📖 Usage Examples

### Single Stock Analysis
```python
engine = StockRecommendationEngine("SBIN-EQ")
results = engine.run_full_analysis()
engine.print_recommendation()
```

### Custom Analysis
```python
engine = StockRecommendationEngine("INFY-EQ")
results = engine.run_full_analysis()
rec = results['recommendation']
print(f"Take Profit: ₹{rec['take_profit']:.2f}")
print(f"Stop Loss: ₹{rec['stop_loss']:.2f}")
```

### Batch Comparison
```bash
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ RELIANCE-EQ
```

### API Integration
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "SBIN-EQ"}'
```

## 📚 Documentation

- **[BREEZE_SETUP.md](BREEZE_SETUP.md)** - Breeze Connect setup guide
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete API documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
- **[FILE_INDEX.md](FILE_INDEX.md)** - File descriptions

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# API available at http://localhost:5000
```

## ⚠️ Disclaimer

This is an educational tool. Do not use this as your sole basis for investment decisions. Always do your own research and consult financial professionals before trading. Past performance does not guarantee future results.

## 📝 Key Differences from Yahoo Finance Version

✅ **Real-time Data** - Breeze Connect provides live market data
✅ **Lower Latency** - Sub-100ms updates vs daily data
✅ **Indian Market Focus** - Perfect for NSE/BSE stocks
✅ **More Accurate** - Direct from exchange data feed
❌ **Requires Credentials** - Need Angel Broking account
❌ **Market Hours Only** - Data during trading hours only

## 🤝 Contributing

Contributions welcome! Fork, create a feature branch, and submit a PR.

## 📧 Support

For issues or questions:
1. Check [BREEZE_SETUP.md](BREEZE_SETUP.md)
2. Review [DOCUMENTATION.md](DOCUMENTATION.md)
3. Create a GitHub issue

---

**Stock Recommendation AI Agent** - Real-time Analysis. Precise Recommendations. Professional Grade.
