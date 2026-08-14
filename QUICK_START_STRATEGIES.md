# Quick Start: Multi-Strategy Trading Recommendations

## 🎯 What You Can Do Now

Your Stock Recommendation AI Agent now supports **5 trading strategies**, each optimized for different trading styles and timeframes:

| Strategy | Duration | Target | Best For |
|----------|----------|--------|----------|
| 🏃 **Scalping** | 5-60 min | 0.75% | Professional day traders |
| 📊 **Intraday** | 1-4 hours | 1.5% | Part-time traders |
| 🌙 **BTST** | Overnight | 1.2% | Evening traders |
| 📈 **Swing** | 2-5 days | 3% | Standard traders (DEFAULT) |
| 🚀 **Momentum** | 5+ days | 5% | Trend followers |

---

## ⚡ Quick Commands

### List All Strategies
```bash
python cli.py --strategies
```
Output:
```
SCALPING    - Ultra-short term trading (5-15 min), tight stops
INTRADAY    - Same-day trading (1-4 hours), moderate risk
BTST        - Overnight (buy close, sell open), momentum-based
SWING       - Medium-term (2-5 days), strong trends
MOMENTUM    - Long-term (5+ days), trend following
```

### Analyze Stock with Specific Strategy

**Scalping** (5-minute trades):
```bash
python cli.py -s SBIN-EQ --strategy scalping
```

**Intraday** (1-4 hour trades):
```bash
python cli.py -s INFY-EQ --strategy intraday
```

**BTST** (Overnight trades):
```bash
python cli.py -s TCS-EQ --strategy btst
```

**Swing** (2-5 day trades, DEFAULT):
```bash
python cli.py -s RELIANCE-EQ --strategy swing
# OR just:
python cli.py -s RELIANCE-EQ
```

**Momentum** (1-4 week trades):
```bash
python cli.py -s BHARTIARTL-EQ --strategy momentum
```

### Compare Multiple Stocks
```bash
# Compare 3 stocks using intraday strategy
python cli.py -s SBIN-EQ INFY-EQ TCS-EQ --strategy intraday
```

### Generate Charts
```bash
python cli.py -s SBIN-EQ --strategy scalping --chart
```

### Get JSON Output
```bash
python cli.py -s INFY-EQ --strategy swing --json
```

---

## 📖 Understanding the Output

### Scalping Trade
```
RECOMMENDATION: BUY
Strategy:             Scalping (5-15 min)
Holding Period:       5-60 minutes
Current Price:        ₹550.25
Take Profit:          ₹554.38 (+0.75%)
Stop Loss:            ₹549.08 (-0.35%)
Risk/Reward Ratio:    2.14:1

Confidence:           78.5%
```

**What it means:**
- Enter at ₹550.25
- Exit at ₹554.38 (goal)
- Exit at ₹549.08 (max loss)
- Hold for 5-60 minutes
- 78.5% confidence in this setup

### Swing Trade
```
RECOMMENDATION: BUY
Strategy:             Swing (2-5 days)
Holding Period:       2-5 days
Current Price:        ₹1,250.50
Take Profit:          ₹1,288.26 (+3.02%)
Stop Loss:            ₹1,231.98 (-1.48%)
Risk/Reward Ratio:    2.04:1

Confidence:           72.3%
```

**What it means:**
- Enter at ₹1,250.50
- Hold for 2-5 days
- Target: ₹1,288.26 (+3%)
- Stop: ₹1,231.98 (-1.5%)
- 72.3% confidence

---

## 🐍 Python API Usage

### Single Strategy Analysis
```python
from recommendation_engine import StockRecommendationEngine

# Create engine with strategy
engine = StockRecommendationEngine("SBIN-EQ", strategy="intraday")

# Run analysis
results = engine.run_full_analysis()

# Access recommendation
rec = results['recommendation']
print(f"Action: {rec['action']}")
print(f"Target: ₹{rec['take_profit']:.2f}")
print(f"Stop: ₹{rec['stop_loss']:.2f}")
```

### Compare All Strategies
```python
from strategy_config import STRATEGIES
from recommendation_engine import StockRecommendationEngine

symbol = "SBIN-EQ"

print(f"{'Strategy':<12} {'Action':<8} {'Conf%':<8} {'Target%':<8}")
print("─" * 40)

for strategy_name in STRATEGIES.keys():
    engine = StockRecommendationEngine(symbol, strategy=strategy_name)
    results = engine.run_full_analysis()
    rec = results['recommendation']
    
    print(f"{strategy_name:12s} {rec['action']:<8} "
          f"{rec['confidence']:6.1f}%  {rec['profit_target_percent']:6.2f}%")
```

Output:
```
Strategy     Action   Conf%   Target%
───────────────────────────────────────
scalping     BUY      78.5%    0.75%
intraday     BUY      72.3%    1.50%
btst         HOLD     65.0%    1.20%
swing        BUY      68.9%    3.00%
momentum     SELL     71.2%    5.00%
```

### Portfolio Analysis
```python
from strategy_config import STRATEGIES
from recommendation_engine import StockRecommendationEngine

portfolio = ["SBIN-EQ", "INFY-EQ", "TCS-EQ"]
strategy = "swing"

for symbol in portfolio:
    engine = StockRecommendationEngine(symbol, strategy=strategy)
    results = engine.run_full_analysis()
    rec = results['recommendation']
    
    print(f"{symbol:12s} | {rec['action']:4s} | "
          f"Conf: {rec['confidence']:5.1f}% | Target: +{rec['profit_target_percent']:.2f}%")
```

---

## 🎓 Strategy Selection Guide

### "I Trade Every Day, Multiple Times"
→ Use **Scalping**
```bash
python cli.py -s SYMBOL --strategy scalping
```
- Very tight stops (0.35%)
- Quick entries/exits (5-60 min)
- 5-minute candles
- Requires constant monitoring

### "I Trade After Work (1-4 Hours)"
→ Use **Intraday**
```bash
python cli.py -s SYMBOL --strategy intraday
```
- Moderate targets (1.5%)
- 1-4 hour holding
- Hourly candles
- Check once daily

### "I Trade Before Market Close"
→ Use **BTST**
```bash
python cli.py -s SYMBOL --strategy btst
```
- Trade near close
- Hold overnight
- Sell next open/early
- Momentum-based signals

### "I'm a Standard Trader (DEFAULT)"
→ Use **Swing**
```bash
python cli.py -s SYMBOL --strategy swing
# or just:
python cli.py -s SYMBOL
```
- Hold 2-5 days
- Good risk:reward (2:1)
- Daily candles
- Best for beginners

### "I Follow Trends (1-4 Weeks)"
→ Use **Momentum**
```bash
python cli.py -s SYMBOL --strategy momentum
```
- Large targets (5%)
- Requires strong trends
- 1-year data analysis
- Long holding periods

---

## 📊 Output Interpretation

### Signal Analysis
```
Bullish Signals:      7
Bearish Signals:      2
Net Sentiment:        BULLISH
```
**More bullish than bearish = Good setup**

### Confidence Score
```
Confidence:           78.5%
Analysis Score:       72.3/100
```
- 80%+ = Very Strong
- 70-79% = Strong
- 60-69% = Moderate
- Below 60% = Weak

### Risk Management
```
Risk:Reward Ratio:    2.14:1
Profit Target %:      0.75%
Risk %:               0.35%
```
**Good setups have R:R of 2:1 or better**

---

## ⚠️ Risk Management Rules

### Position Sizing
- Risk only 2% of account per trade
- Scalping: Max 10 trades/day
- Intraday: Max 5 trades/day
- Swing: 3-5 positions at a time
- Momentum: 1-2 positions at a time

### Stop Loss
- **NEVER** move stops lower (on BUY)
- **NEVER** exceed strategy stop %
- Scalping: 0.35% max
- Intraday: 0.75% max
- Swing: 1.5% max

### Take Profit
- Take partial profits at 50% of target
- Let remaining run for bigger gains
- Don't be greedy

---

## 📈 Example Trade

### Scalping Setup
```bash
python cli.py -s SBIN-EQ --strategy scalping
```

Output:
```
Current Price:   ₹550.25
Action:          BUY
Take Profit:     ₹554.38 (+0.75%)
Stop Loss:       ₹549.08 (-0.35%)
Confidence:      78.5%
```

**Execution:**
1. Wait for candle close
2. BUY at ₹550.25
3. Set stop at ₹549.08
4. Set target at ₹554.38
5. Exit when either level is hit
6. **Time**: 5-60 minutes

---

## 🚀 Next Steps

### 1. Choose Your Strategy
```bash
python cli.py --strategies
```

### 2. Analyze a Stock
```bash
python cli.py -s SBIN-EQ --strategy YOUR_STRATEGY
```

### 3. Review the Signals
- Look at confidence score (70%+ is good)
- Check support/resistance levels
- Verify bullish vs bearish signals

### 4. Execute with Risk Management
- Size position for 2% max risk
- Set stops exactly as indicated
- Don't move stops against you
- Take profits according to plan

### 5. Track Results
- Maintain trading journal
- Record entry/exit prices
- Track win rate per strategy
- Review monthly performance

---

## 📚 More Information

- **Full Strategy Guide**: See `STRATEGIES.md`
- **Configuration Details**: See `strategy_config.py`
- **Code Examples**: Run `python examples.py`
- **API Reference**: See `DOCUMENTATION.md`
- **Setup Guide**: See `BREEZE_SETUP.md`

---

## ✅ You're Ready!

Your Stock Recommendation AI Agent now supports:

✅ 5 Complete Trading Strategies
✅ Breeze Connect Real-Time Data
✅ Professional Technical Analysis
✅ Dynamic Risk Management
✅ Multi-Strategy Comparison
✅ Production-Ready Code

**Start analyzing stocks with your preferred strategy!** 🎯

---

**Command Cheat Sheet:**
```bash
# List all strategies
python cli.py --strategies

# Scalping
python cli.py -s SYMBOL --strategy scalping

# Intraday
python cli.py -s SYMBOL --strategy intraday

# BTST (Overnight)
python cli.py -s SYMBOL --strategy btst

# Swing (Default)
python cli.py -s SYMBOL --strategy swing
python cli.py -s SYMBOL  # Same thing

# Momentum (Trend Following)
python cli.py -s SYMBOL --strategy momentum

# Compare stocks
python cli.py -s SYM1 SYM2 SYM3 --strategy swing

# With chart
python cli.py -s SYMBOL --strategy swing --chart

# JSON output
python cli.py -s SYMBOL --strategy swing --json

# Examples
python examples.py
```

Good luck trading! 📊🚀
