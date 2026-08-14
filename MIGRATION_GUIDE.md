# Migration Guide: Yahoo Finance → Breeze Connect

## Overview

The Stock Recommendation AI Agent has been migrated from Yahoo Finance to **Breeze Connect** for real-time market data. This guide explains the changes and how to migrate your existing code.

## 🔄 What Changed

### Before (Yahoo Finance)
```python
from data_handler import StockDataHandler

# Fetch US stock data
engine = StockRecommendationEngine("AAPL", period="1y", interval="1d")
df = engine.data_handler.fetch_data()
```

### After (Breeze Connect)
```python
from data_handler import StockDataHandler

# Fetch Indian stock data (NSE/BSE)
engine = StockRecommendationEngine("SBIN-EQ", period="1y")
df = engine.data_handler.fetch_data()
```

## 📋 Key Differences

| Aspect | Yahoo Finance | Breeze Connect |
|--------|---------------|----------------|
| **Data Source** | Yahoo Finance | Angel Broking |
| **Market** | US stocks | Indian stocks (NSE/BSE) |
| **Symbol Format** | AAPL, MSFT | SBIN-EQ, INFY-EQ |
| **Data Freshness** | Daily (free) | Real-time (live) |
| **Latency** | Delayed | Sub-100ms |
| **Credentials Required** | No | Yes (API key) |
| **Best For** | Historical analysis | Live trading |

## 🚀 Migration Steps

### Step 1: Update Credentials

Get Breeze Connect API credentials:

1. Visit https://www.angelbroking.com/breeze/
2. Sign up or log in
3. Generate API credentials
4. Add to `.env`:

```bash
BREEZE_API_KEY=your-api-key
BREEZE_SECRET_KEY=your-secret-key
```

### Step 2: Update Symbol Format

Convert your stock symbols to Breeze format:

```
AAPL        → AAPL-EQ      (for international stocks, use country)
MSFT        → MSFT-EQ
GOOGL       → GOOGL-EQ

SBIN        → SBIN-EQ      (Indian NSE stocks)
INFY        → INFY-EQ
TCS         → TCS-EQ
```

**How to determine format:**
- NSE stocks: Add `-EQ` suffix
- BSE stocks: Add `-BE` suffix
- Futures: Add `-FUT` suffix
- Options: Add `-OPT` suffix

The system automatically converts if you just use the base symbol.

### Step 3: Update Your Code

**Old Code (Yahoo Finance)**
```python
from recommendation_engine import StockRecommendationEngine

engine = StockRecommendationEngine("AAPL")
results = engine.run_full_analysis()
```

**New Code (Breeze Connect)**
```python
from recommendation_engine import StockRecommendationEngine

# For Indian stocks
engine = StockRecommendationEngine("SBIN-EQ")
results = engine.run_full_analysis()

# OR use base symbol (auto-converted)
engine = StockRecommendationEngine("SBIN")
results = engine.run_full_analysis()
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install `breeze-connect` instead of `yfinance`.

## 📊 Symbol Examples

### Indian Stocks (NSE)

```python
# Bank sector
"SBIN-EQ"       # State Bank of India
"HDFC-EQ"       # HDFC Bank
"ICICIBANK-EQ"  # ICICI Bank

# IT sector
"INFY-EQ"       # Infosys
"TCS-EQ"        # Tata Consultancy Services
"WIPRO-EQ"      # Wipro

# Large cap
"RELIANCE-EQ"   # Reliance Industries
"BHARTIARTL-EQ" # Bharti Airtel
"LT-EQ"         # Larsen & Toubro
```

### CLI Usage

```bash
# Single stock
python cli.py -s SBIN-EQ

# Multiple stocks
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ

# Auto-convert symbol
python cli.py -s SBIN  # Becomes SBIN-EQ
```

### API Usage

```bash
# Real-time analysis
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol":"SBIN-EQ"}'

# Get recommendation
curl http://localhost:5000/api/recommendation/SBIN-EQ
```

## 🔍 Verifying Migration

Run the verification script:

```bash
python quickstart.py
```

This will:
- ✓ Check dependencies
- ✓ Verify Breeze credentials
- ✓ Test data handler
- ✓ Provide setup guidance

## ⚠️ Important Notes

### Market Hours
Breeze Connect provides live data during:
- **NSE/BSE**: 9:15 AM - 3:30 PM IST (Mon-Fri)
- **Outside hours**: Last close price available

### Rate Limits
Angel Broking has per-account rate limits:
- Check your dashboard for limits
- Implement caching for repeated requests
- Use batch operations when possible

### Historical Data
You can access up to 10 years of historical data from Breeze Connect.

### CSV Fallback
If Breeze credentials aren't available, you can still use CSV data:

```python
from data_handler import CSVDataHandler

handler = CSVDataHandler('your_data.csv')
df = handler.fetch_data()
```

## 🆘 Troubleshooting

### "Breeze authentication failed"

**Check:**
1. Credentials in `.env` file are correct
2. API key is active (not revoked)
3. Network connection is stable

### "No data found for symbol"

**Check:**
1. Symbol format is correct (e.g., `SBIN-EQ`)
2. Stock is available on Angel Broking
3. Market is currently open
4. Symbol exists (typo check)

### "API rate limit exceeded"

**Solution:**
1. Wait a few minutes
2. Reduce request frequency
3. Implement caching
4. Check your API plan limits

## 📈 New Features with Breeze Connect

✨ **Real-time Data** - Live market updates
✨ **Better Accuracy** - Direct from exchange
✨ **Faster Updates** - Sub-100ms latency
✨ **More Instruments** - Futures, options support
✨ **Volume Profiling** - Better liquidity analysis

## 📚 Resources

- [Breeze Setup Guide](BREEZE_SETUP.md)
- [Breeze API Documentation](https://angel-breeze-api.readme.io/)
- [Main Documentation](DOCUMENTATION.md)

## ❓ FAQ

**Q: Can I still use Yahoo Finance data?**
A: No, but you can import CSV files with historical data using `CSVDataHandler`.

**Q: Do I need to change my analysis logic?**
A: No! The analysis engine remains the same. Only the data source changed.

**Q: What if I don't have Breeze credentials?**
A: Use CSV data or set up free Angel Broking account for Breeze access.

**Q: Can I analyze international stocks?**
A: Breeze Connect focuses on Indian markets. Use CSV data for international stocks.

**Q: Is there a free tier?**
A: Yes! Angel Broking offers free Breeze API access.

## 🔄 Rollback to CSV

If you need to use CSV data temporarily:

```python
from data_handler import CSVDataHandler

handler = CSVDataHandler('my_stock_data.csv')
df = handler.fetch_data()

# Use with analysis
from technical_analysis import TechnicalAnalyzer
analyzer = TechnicalAnalyzer(df)
indicators = analyzer.calculate_all_indicators()
```

---

**Migration Complete!** Now you have real-time market data. 🎯
