# Multi-Strategy Trading Recommendations

## Overview

The Stock Recommendation AI Agent now supports **5 distinct trading strategies**, each optimized for different market conditions, timeframes, and risk profiles.

## 🎯 Available Strategies

### 1. **Scalping** - Ultra-Short Term Trading
**Best for:** Active day traders with tight risk management

| Parameter | Value |
|-----------|-------|
| **Timeframe** | 5-15 minutes |
| **Holding Period** | 5-60 minutes |
| **Data Period** | 1 day |
| **Data Interval** | 5-minute candles |
| **Profit Target** | 0.75% |
| **Stop Loss** | 0.35% |
| **Risk:Reward** | 2.0:1 |
| **Confidence Threshold** | 70% |

**Characteristics:**
- ✓ Very fast entry/exit
- ✓ Tight stop losses
- ✓ Quick profit taking
- ✗ Requires active monitoring
- ✗ High transaction costs
- ✗ Needs discipline

**Best Used For:**
- High-volume stocks (NSE)
- Liquid options with tight spreads
- Intraday momentum trades
- Fed time announcements (US markets)

**Technical Indicators Priority:**
1. RSI (9-period) - Oversold/Overbought
2. MACD (5/13/3) - Fast crossovers
3. Bollinger Bands (14, 1.5σ) - Tight bands
4. Volume (real-time) - Confirmation

**Example CLI:**
```bash
python cli.py -s SBIN-EQ --strategy scalping
```

---

### 2. **Intraday** - Same-Day Trading
**Best for:** Day traders with moderate experience

| Parameter | Value |
|-----------|-------|
| **Timeframe** | 1-4 hours |
| **Holding Period** | 1-4 hours |
| **Data Period** | 20 days |
| **Data Interval** | 1-hour candles |
| **Profit Target** | 1.5% |
| **Stop Loss** | 0.75% |
| **Risk:Reward** | 2.0:1 |
| **Confidence Threshold** | 65% |

**Characteristics:**
- ✓ Moderate pace trading
- ✓ Reasonable profit targets
- ✓ Daily close-out (no overnight risk)
- ✓ Good for part-time traders
- ✗ Still requires active monitoring
- ✗ Emotional pressure from quick moves

**Best Used For:**
- Banking, IT, Finance stocks
- Morning breakouts
- Asian market open trades
- FOMC decision days (volatility)

**Technical Indicators Priority:**
1. MACD (10/24/8) - Signal line crosses
2. RSI (12) - Extreme levels
3. Support/Resistance (50-period)
4. Volume Profile - Resistance zones

**Example CLI:**
```bash
python cli.py -s INFY-EQ --strategy intraday --chart
```

---

### 3. **BTST** - Buy Today, Sell Tomorrow
**Best for:** Overnight momentum traders

| Parameter | Value |
|-----------|-------|
| **Timeframe** | 1-4 hours |
| **Holding Period** | 4-16 hours (overnight) |
| **Data Period** | 30 days |
| **Data Interval** | 1-hour candles |
| **Profit Target** | 1.2% |
| **Stop Loss** | 0.8% |
| **Risk:Reward** | 1.5:1 |
| **Confidence Threshold** | 65% |
| **Momentum Strength** | 70% required |

**Characteristics:**
- ✓ Trade near market close
- ✓ Sell at next open/early
- ✓ Avoids end-of-day panic
- ✓ Momentum-based (strong signals required)
- ✗ Gap risk (unexpected opening)
- ✗ Overnight news risk

**Best Used For:**
- Strong momentum stocks
- Breakout above resistance
- Post-earnings rallies
- Major macroeconomic announcements

**Technical Indicators Priority:**
1. Momentum Indicators (ROC, CCI)
2. Volume Surge Detection
3. End-of-day Support/Resistance
4. Order Blocks (bullish/bearish)

**Example CLI:**
```bash
python cli.py -s TCS-EQ --strategy btst
```

---

### 4. **Swing Trading** - Medium-Term Trend Trading
**Best for:** Traders with 2-5 day holding periods

| Parameter | Value |
|-----------|-------|
| **Timeframe** | 1 day |
| **Holding Period** | 2-5 days |
| **Data Period** | 6 months |
| **Data Interval** | Daily candles |
| **Profit Target** | 3.0% |
| **Stop Loss** | 1.5% |
| **Risk:Reward** | 2.0:1 |
| **Confidence Threshold** | 65% |

**Characteristics:**
- ✓ Standard timeframe
- ✓ Good risk:reward ratios
- ✓ Trend following
- ✓ Ideal for most traders
- ✗ Overnight gap risk
- ✗ Holding period stress

**Best Used For:**
- Strong trending markets
- Support/Resistance bounces
- Sector rotations
- Fundamental catalyst trades

**Technical Indicators Priority:**
1. Moving Averages (Golden/Death Cross)
2. Support/Resistance (100-period lookback)
3. ADX (trend strength)
4. MACD (trend confirmation)

**Example CLI:**
```bash
python cli.py -s RELIANCE-EQ --strategy swing
# Default strategy
python cli.py -s HDFC-EQ
```

---

### 5. **Momentum Trading** - Long-Term Trend Following
**Best for:** Swing/position traders with 1-4 week horizon

| Parameter | Value |
|-----------|-------|
| **Timeframe** | 1 day to 1 week |
| **Holding Period** | 5+ days (1-4 weeks) |
| **Data Period** | 1 year |
| **Data Interval** | Daily candles |
| **Profit Target** | 5.0% |
| **Stop Loss** | 2.0% |
| **Risk:Reward** | 2.5:1 |
| **Confidence Threshold** | 60% |
| **Trend Strength** | 75% required |

**Characteristics:**
- ✓ Large profit potential
- ✓ Following strong trends
- ✓ Less emotional trading
- ✓ Lower transaction costs
- ✗ Larger stop losses
- ✗ Endurance testing
- ✗ Major trend reversal risk

**Best Used For:**
- Strong uptrends/downtrends
- Sector outperformers
- Long-term breakouts
- Portfolio-level positions

**Technical Indicators Priority:**
1. Long-term MAs (50/100/200)
2. ADX > 40 (strong trend)
3. Volume confirmation (increasing)
4. Order blocks (major support)

**Example CLI:**
```bash
python cli.py -s BHARTIARTL-EQ --strategy momentum
```

---

## 📊 Strategy Comparison Table

| Aspect | Scalping | Intraday | BTST | Swing | Momentum |
|--------|----------|----------|------|-------|----------|
| **Duration** | Minutes | Hours | Overnight | 2-5 days | 1-4 weeks |
| **Target %** | 0.75% | 1.5% | 1.2% | 3% | 5% |
| **Stop Loss %** | 0.35% | 0.75% | 0.8% | 1.5% | 2% |
| **R:R Ratio** | 2.0:1 | 2.0:1 | 1.5:1 | 2.0:1 | 2.5:1 |
| **Monitoring** | Constant | Active | Pre-close | Daily | Weekly |
| **Stress Level** | Very High | High | Medium | Low | Very Low |
| **Win Rate %** | 60-65% | 55-60% | 50-55% | 50-60% | 45-55% |
| **Drawdown Risk** | Low | Low-Med | Med | Med-High | High |
| **Best For** | Professionals | Part-time | Evening traders | Standard | Long-term |

---

## 🚀 Usage Examples

### Example 1: Quick Scalping Alert
```bash
# Check SBIN for scalping opportunities
python cli.py -s SBIN-EQ --strategy scalping --json

# Output: Tight stops, quick targets, live signals
```

### Example 2: Intraday Comparison
```bash
# Compare 3 stocks for intraday trades
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ --strategy intraday

# Shows 1-4 hour moves with hourly data
```

### Example 3: BTST Setup Near Close
```bash
# Find overnight momentum trade
python cli.py -s HDFC-EQ --strategy btst --chart

# Generates hourly chart with entry near close
```

### Example 4: Swing Trade Research
```bash
# Detailed swing analysis (default)
python cli.py -s RELIANCE-EQ --strategy swing

# 2-5 day holding with daily candl

es
```

### Example 5: Momentum Confirmation
```bash
# Check if strong trend exists
python cli.py -s BHARTIARTL-EQ --strategy momentum

# Requires 75% trend strength (ADX)
```

### Example 6: All Strategies at Once
```python
from recommendation_engine import StockRecommendationEngine
from strategy_config import STRATEGIES

symbol = "SBIN-EQ"

for strategy in STRATEGIES.keys():
    engine = StockRecommendationEngine(symbol, strategy=strategy)
    results = engine.run_full_analysis()
    rec = results['recommendation']
    print(f"{strategy:12s} | {rec['action']:4s} | Conf: {rec['confidence']:5.1f}%")
```

---

## 🎓 Strategy Selection Guide

### "I'm a Professional Day Trader"
→ Use **Scalping** or **Intraday**
- Multiple trades per day
- Tight risk management
- Real-time monitoring
- High win rates expected

### "I Trade After Regular Hours"
→ Use **BTST (Buy Today Sell Tomorrow)**
- Trade near market close
- Sell next morning
- Catch overnight momentum
- Lower stress than scalping

### "I Trade Part-Time"
→ Use **Swing Trading** (default)
- Hold 2-5 days
- Good risk:reward
- Check once daily
- Standard technical analysis

### "I'm a Long-Term Investor"
→ Use **Momentum Trading**
- Hold 1-4 weeks
- Follow strong trends
- Check weekly
- Large profit targets

### "I Want to Compare Everything"
→ Use **REST API** with all strategies
```bash
curl -X POST http://localhost:5000/api/analyze_multi_strategy \
  -d '{"symbol":"SBIN-EQ"}'

# Returns recommendation for all 5 strategies
```

---

## 📈 Strategy Performance Metrics

### Expected Win Rate
- **Scalping**: 60-65% (needs high accuracy)
- **Intraday**: 55-60% (good consistency)
- **BTST**: 50-55% (momentum-based)
- **Swing**: 50-60% (trend-following)
- **Momentum**: 45-55% (catching trends)

### Risk Management by Strategy
```
Scalping:   |█████| Tight  (0.35% SL)
Intraday:   |██████| Moderate (0.75% SL)
BTST:       |███████| Med-High (0.8% SL)
Swing:      |███████████| High (1.5% SL)
Momentum:   |█████████████| Very High (2% SL)
```

### Annual Return Potential (with consistent execution)
```
Scalping:   20-40% (very disciplined)
Intraday:   15-30% (consistent trader)
BTST:       12-25% (good timing)
Swing:      20-50% (trend catching)
Momentum:   30-100%+ (strong trends)
```

---

## 🛠️ Advanced: API Integration

### REST API Endpoint
```bash
POST /api/analyze_strategy
Content-Type: application/json

{
  "symbol": "SBIN-EQ",
  "strategy": "intraday",
  "period": "20d",
  "interval": "1h"
}
```

### Response Example
```json
{
  "symbol": "SBIN-EQ",
  "strategy": "intraday",
  "strategy_name": "Intraday",
  "timeframe": "1-4 hours",
  "holding_period": "1-4 hours",
  "recommendation": {
    "action": "BUY",
    "confidence": 78.5,
    "score": 72.3,
    "take_profit": 412.50,
    "stop_loss": 409.00,
    "profit_target_percent": 1.54,
    "risk_percent": 0.73,
    "risk_reward_ratio": 2.11
  }
}
```

---

## ⚠️ Important Notes

### Choose Your Strategy Wisely
- Don't switch strategies mid-trade
- Match strategy to your lifestyle
- Test strategy before real money
- Keep trading hours consistent

### Risk Management is Key
- Never exceed stop loss
- Position size based on risk
- Max 2% account risk per trade
- Maintain trading journal

### Market Conditions Matter
- Scalping: Best in high volatility
- Intraday: All conditions
- BTST: End-of-day momentum only
- Swing: Strong trending markets
- Momentum: Very strong trends

---

## 📚 References

- [strategy_config.py](strategy_config.py) - Configuration details
- [recommendation_engine.py](recommendation_engine.py) - Engine logic
- [DOCUMENTATION.md](DOCUMENTATION.md) - Full API reference
- [examples.py](examples.py) - Code examples

---

**Ready to trade?** Choose your strategy and run:
```bash
python cli.py -s SYMBOL --strategy [strategy_name]
```

Good luck! 📊🚀
