# Breeze Connect Real-Time Data Setup Guide

## 🔌 Overview

The Stock Recommendation AI Agent now uses **Breeze Connect** for real-time market data instead of Yahoo Finance. Breeze Connect provides low-latency, real-time data directly from Angel Broking's market data feed.

## 📋 Prerequisites

- Angel Broking account (free or premium)
- Breeze API credentials

## ✅ Setup Steps

### Step 1: Get Angel Broking Credentials

1. Visit [Angel Broking Breeze API](https://www.angelbroking.com/breeze/)
2. Sign up or log in to your account
3. Navigate to API/Developer Settings
4. Generate your API credentials:
   - **API Key**: Your unique API identifier
   - **Secret Key**: Your API secret (keep this confidential!)

### Step 2: Update Environment File

Copy the template and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Breeze credentials:

```bash
# Breeze Connect Configuration
BREEZE_API_KEY=your-actual-breeze-api-key
BREEZE_SECRET_KEY=your-actual-breeze-secret-key
BREEZE_USE_PRODUCTION=True
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `breeze-connect==2.0.5` along with other dependencies.

### Step 4: Verify Installation

```bash
python quickstart.py
```

The quickstart script will verify that Breeze Connect is properly configured.

## 🚀 Usage Examples

### Basic Usage (Python)

```python
from data_handler import BreezeConnectDataHandler

# Initialize handler
handler = BreezeConnectDataHandler('SBIN-EQ')  # Sbin stock on NSE

# Fetch historical data
df = handler.fetch_data()

# Get real-time quote
realtime = handler.fetch_realtime('SBIN-EQ')
print(f"LTP: ${realtime['ltp']}")
print(f"Volume: {realtime['volume']}")
```

### Using with Recommendation Engine

```python
from recommendation_engine import StockRecommendationEngine

# Will automatically use Breeze Connect
engine = StockRecommendationEngine('SBIN-EQ')
results = engine.run_full_analysis()
engine.print_recommendation()
```

### Command Line

```bash
# Analyze Indian stock (NSE format)
python cli.py -s SBIN-EQ

# Generate chart
python cli.py -s SBIN-EQ --chart

# Compare multiple stocks
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ
```

### REST API

```bash
# Start server
python api_server.py

# Analyze stock
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol":"SBIN-EQ"}'

# Get real-time quote
curl http://localhost:5000/api/recommendation/SBIN-EQ
```

## 📊 Supported Stock Formats

Breeze Connect uses the following naming conventions:

### NSE (National Stock Exchange)
- Format: `SYMBOL-EQ`
- Examples: `SBIN-EQ`, `INFY-EQ`, `TCS-EQ`, `RELIANCE-EQ`

### BSE (Bombay Stock Exchange)
- Format: `SYMBOL-BE`
- Examples: `SBIN-BE`, `INFY-BE`

### Futures & Options
- Format: `SYMBOL-FUT`, `SYMBOL-OPT`

**The system automatically converts symbol formats** - you can use just `SBIN` and it will be converted to `SBIN-EQ` for NSE stocks.

## 🔄 Real-Time Data Features

Breeze Connect provides:

✅ **Real-time Level 1 data**: LTP, bid, ask, volume
✅ **Historical candle data**: 1-minute to daily
✅ **Low latency**: Sub-100ms updates
✅ **Multiple instruments**: Stocks, futures, options
✅ **High reliability**: Angel Broking's proven infrastructure

## 🛠️ Troubleshooting

### Error: "Breeze authentication failed"

**Solution**: Verify your credentials in `.env` file

```bash
# Check your .env file
cat .env | grep BREEZE
```

### Error: "No data found for symbol"

**Possible causes**:
1. Wrong symbol format (use `SBIN-EQ`, not `SBIN`)
2. Market is closed (Indian market hours: 9:15 AM - 3:30 PM IST, Mon-Fri)
3. Stock is not available in the API

**Solution**: Verify symbol format and market status

### Error: "API rate limit exceeded"

**Solution**: Implement request caching or reduce polling frequency

### Session expires

The session key is managed automatically, but you can refresh it:

```python
handler = BreezeConnectDataHandler('SBIN-EQ')
handler.login(BREEZE_SECRET_KEY)
```

## 📈 Data Available

### Historical Data
- Up to 10 years of daily data
- Intraday data (1-minute candles)
- OHLCV (Open, High, Low, Close, Volume)

### Real-time Data
- Last Traded Price (LTP)
- Bid-Ask spread
- Volume and open interest
- Timestamp

## 🔐 Security Best Practices

1. **Keep `.env` file private**
   - Add to `.gitignore`: `echo ".env" >> .gitignore`

2. **Use separate API keys for different environments**
   - Development key
   - Production key

3. **Rotate credentials periodically**
   - Regenerate keys in Angel Broking settings

4. **Never commit credentials to version control**

## 🌐 API Documentation

For complete Breeze Connect API documentation, visit:
- [Breeze API Documentation](https://angel-breeze-api.readme.io/)
- [Angel Broking Developer Portal](https://www.angelbroking.com/breeze/)

## 📞 Support

### If you encounter issues:

1. **Check Angel Broking status**: https://status.angelbroking.com/
2. **Review API limits**: Check dashboard for rate limits
3. **Verify market hours**: Breeze provides live data during market hours only
4. **Contact Angel Broking Support**: support@angelbroking.com

## ⚡ Performance Tips

1. **Cache data** - The API caches results to avoid repeated calls
2. **Use appropriate intervals** - Don't request data more frequently than needed
3. **Batch requests** - Analyze multiple stocks sequentially
4. **Monitor rate limits** - Angel Broking has per-account rate limits

## 🔄 Migration from Yahoo Finance

If you previously used Yahoo Finance:

1. **Update imports**: Already handled in `data_handler.py`
2. **Update credentials**: Add Breeze API keys to `.env`
3. **Update symbols**: Use NSE format (e.g., `SBIN-EQ` instead of `SBIN.NS`)
4. **No code changes needed**: The engine automatically uses Breeze Connect

## 📝 CSV Fallback

If you don't have Breeze Connect credentials, you can still use the system with CSV files:

```python
from data_handler import CSVDataHandler

handler = CSVDataHandler('your_data.csv')
df = handler.fetch_data()
```

## 🚀 Next Steps

1. Get Angel Broking account credentials
2. Add credentials to `.env`
3. Run `python quickstart.py` to verify setup
4. Start analyzing with `python cli.py -s SBIN-EQ`
5. Read [DOCUMENTATION.md](DOCUMENTATION.md) for detailed API reference

---

**Ready to use real-time market data!** 🎯
