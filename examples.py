"""
Multi-Strategy Trading Examples
Demonstrates the Stock Recommendation AI Agent with all 5 trading strategies:
- Scalping, Intraday, BTST, Swing, Momentum
"""

from recommendation_engine import StockRecommendationEngine
from strategy_config import STRATEGIES, list_all_strategies
import json


def example_1_all_strategies_comparison():
    """Example 1: Analyze same stock with all strategies"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Multi-Strategy Analysis - Compare All Strategies")
    print("="*80)
    
    symbol = "SBIN-EQ"
    print(f"\nAnalyzing {symbol} with all 5 strategies...\n")
    
    results = {}
    for strategy_name in STRATEGIES.keys():
        try:
            print(f"  {strategy_name.upper():12s}... ", end='', flush=True)
            engine = StockRecommendationEngine(symbol, strategy=strategy_name)
            analysis = engine.run_full_analysis()
            rec = analysis['recommendation']
            results[strategy_name] = rec
            print("✓")
        except Exception as e:
            print(f"✗ ({str(e)[:30]})")
    
    # Display comparison table
    print(f"\n{'─'*100}")
    print(f"{'Strategy':<15} {'Action':<8} {'Conf%':<8} {'Target%':<9} {'Stop%':<8} {'R:R':<7} {'Holding':<20}")
    print(f"{'─'*100}")
    
    for strategy, rec in results.items():
        print(f"{strategy.upper():<15} {rec['action']:<8} {rec['confidence']:<8.1f} "
              f"{rec['profit_target_percent']:<9.2f} {rec['risk_percent']:<8.2f} "
              f"{rec['risk_reward_ratio']:<7.2f} {rec['holding_period']:<20}")
    
    print(f"{'─'*100}\n")
    
    # Find strongest signal
    strongest = max(results.items(), key=lambda x: x[1]['confidence'])
    print(f"🎯 STRONGEST SIGNAL: {strongest[0].upper()} with {strongest[1]['confidence']:.1f}% confidence\n")


def example_2_scalping_strategy():
    """Example 2: Scalping - Ultra-short term trading"""
    print("\n" + "="*80)
    print("EXAMPLE 2: SCALPING Strategy - 5-15 Minute Trades")
    print("="*80)
    
    print("\nScalping characteristics:")
    print("  • Duration: 5-60 minutes")
    print("  • Target: 0.75% profit")
    print("  • Stop: 0.35% loss")
    print("  • Risk:Reward: 2.0:1")
    print("  • Uses: 5-minute candles\n")
    
    symbols = ["SBIN-EQ", "INFY-EQ", "TCS-EQ"]
    
    print(f"Scalping setup for: {', '.join(symbols)}\n")
    
    for symbol in symbols:
        try:
            print(f"  {symbol}... ", end='', flush=True)
            engine = StockRecommendationEngine(symbol, strategy="scalping")
            results = engine.run_full_analysis()
            rec = results['recommendation']
            
            if rec['action'] == "BUY":
                entry = rec['current_price']
                tp = rec['take_profit']
                sl = rec['stop_loss']
                gain = ((tp - entry) / entry) * 100
                loss = ((entry - sl) / entry) * 100
                print(f"✓ BUY @ ₹{entry:.2f} | TP: ₹{tp:.2f} (+{gain:.2f}%) | SL: ₹{sl:.2f} (-{loss:.2f}%)")
            else:
                print(f"  {rec['action']} (Conf: {rec['confidence']:.0f}%)")
        except Exception as e:
            print(f"✗ Error: {str(e)[:40]}")
    
    print()


def example_3_intraday_strategy():
    """Example 3: Intraday - 1-4 hour trading"""
    print("\n" + "="*80)
    print("EXAMPLE 3: INTRADAY Strategy - 1-4 Hour Trades")
    print("="*80)
    
    print("\nIntraday characteristics:")
    print("  • Duration: 1-4 hours")
    print("  • Target: 1.5% profit")
    print("  • Stop: 0.75% loss")
    print("  • Risk:Reward: 2.0:1")
    print("  • Uses: 1-hour candles\n")
    
    symbol = "INFY-EQ"
    print(f"Detailed intraday analysis for {symbol}:\n")
    
    try:
        engine = StockRecommendationEngine(symbol, strategy="intraday")
        results = engine.run_full_analysis()
        rec = results['recommendation']
        
        print(f"Current Price:        ₹{rec['current_price']:.2f}")
        print(f"Action:               {rec['action']} (Confidence: {rec['confidence']:.1f}%)")
        print(f"Take Profit:          ₹{rec['take_profit']:.2f} (+{rec['profit_target_percent']:.2f}%)")
        print(f"Stop Loss:            ₹{rec['stop_loss']:.2f} (-{rec['risk_percent']:.2f}%)")
        print(f"Risk:Reward Ratio:    {rec['risk_reward_ratio']:.2f}:1")
        print(f"Score:                {rec['score']:.1f}/100")
        
        print(f"\nTrading Signals:")
        print(f"  Bullish Signals:     {rec['signal_count']['bullish']}")
        print(f"  Bearish Signals:     {rec['signal_count']['bearish']}")
        print(f"  Net Sentiment:       {'BULLISH' if rec['signal_count']['bullish'] > rec['signal_count']['bearish'] else 'BEARISH'}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print()


def example_4_btst_strategy():
    """Example 4: BTST - Buy Today Sell Tomorrow"""
    print("\n" + "="*80)
    print("EXAMPLE 4: BTST Strategy - Buy Today, Sell Tomorrow")
    print("="*80)
    
    print("\nBTST characteristics:")
    print("  • Duration: Overnight (4-16 hours)")
    print("  • Target: 1.2% profit")
    print("  • Stop: 0.8% loss")
    print("  • Risk:Reward: 1.5:1")
    print("  • Entry: Near market close")
    print("  • Exit: Next open or early\n")
    
    symbols = ["TCS-EQ", "HDFC-EQ"]
    print(f"BTST opportunities for: {', '.join(symbols)}\n")
    
    for symbol in symbols:
        try:
            engine = StockRecommendationEngine(symbol, strategy="btst")
            results = engine.run_full_analysis()
            rec = results['recommendation']
            
            print(f"{symbol:12s} | {rec['action']:4s} | "
                  f"Entry: ₹{rec['current_price']:.2f} | "
                  f"Target: ₹{rec['take_profit']:.2f} | "
                  f"Gain: +{rec['profit_target_percent']:.2f}%")
        except Exception as e:
            print(f"{symbol:12s} | Error: {str(e)[:30]}")
    
    print()


def example_5_swing_strategy():
    """Example 5: Swing Trading - 2-5 day holds"""
    print("\n" + "="*80)
    print("EXAMPLE 5: SWING Trading - 2-5 Day Positions")
    print("="*80)
    
    print("\nSwing trading characteristics:")
    print("  • Duration: 2-5 days")
    print("  • Target: 3.0% profit")
    print("  • Stop: 1.5% loss")
    print("  • Risk:Reward: 2.0:1")
    print("  • Uses: Daily candles\n")
    
    symbol = "RELIANCE-EQ"
    print(f"Swing analysis for {symbol}:\n")
    
    try:
        engine = StockRecommendationEngine(symbol, strategy="swing")
        results = engine.run_full_analysis()
        rec = results['recommendation']
        analysis = results['analysis']
        
        print(f"Entry Price:          ₹{rec['current_price']:.2f}")
        print(f"Action:               {rec['action']}")
        print(f"Target (3%):          ₹{rec['take_profit']:.2f}")
        print(f"Stop Loss (1.5%):     ₹{rec['stop_loss']:.2f}")
        print(f"Max Gain:             {rec['profit_target_percent']:.2f}%")
        print(f"Max Loss:             {rec['risk_percent']:.2f}%")
        print(f"Holding Period:       {rec['holding_period']}")
        
        sr = analysis['support_resistance']
        print(f"\nKey Levels:")
        print(f"  Support:            {[f'₹{s:.2f}' for s in sr.get('support', [])[:3]]}")
        print(f"  Resistance:         {[f'₹{r:.2f}' for r in sr.get('resistance', [])[:3]]}")
        
        tech = analysis['technical']
        print(f"\nTechnical Setup:")
        print(f"  RSI:                {tech.get('RSI', 'N/A'):.1f}")
        print(f"  MACD:               {('Bullish' if tech.get('MACD', 0) > tech.get('MACD_SIGNAL', 0) else 'Bearish')}")
        print(f"  ADX:                {tech.get('ADX', 'N/A'):.1f}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print()


def example_6_momentum_strategy():
    """Example 6: Momentum Trading - Long-term trend following"""
    print("\n" + "="*80)
    print("EXAMPLE 6: MOMENTUM Trading - 5+ Day Trend Following")
    print("="*80)
    
    print("\nMomentum trading characteristics:")
    print("  • Duration: 5+ days (1-4 weeks)")
    print("  • Target: 5.0% profit")
    print("  • Stop: 2.0% loss")
    print("  • Risk:Reward: 2.5:1")
    print("  • Uses: Daily candles + 1-year history\n")
    
    symbols = ["BHARTIARTL-EQ", "SBIN-EQ"]
    print(f"Momentum opportunities in: {', '.join(symbols)}\n")
    
    for symbol in symbols:
        try:
            engine = StockRecommendationEngine(symbol, strategy="momentum")
            results = engine.run_full_analysis()
            rec = results['recommendation']
            
            print(f"\n{symbol}:")
            print(f"  Action:              {rec['action']}")
            print(f"  Confidence:          {rec['confidence']:.1f}%")
            print(f"  Entry:               ₹{rec['current_price']:.2f}")
            print(f"  Target (5%):         ₹{rec['take_profit']:.2f}")
            print(f"  Stop (2%):           ₹{rec['stop_loss']:.2f}")
            print(f"  Holding:             {rec['holding_period']}")
            
            if rec['action'] == 'BUY':
                print(f"  ✓ Setup APPROVED for momentum trade")
            else:
                print(f"  ✗ Trend not strong enough")
        
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    print()


def example_7_strategy_details():
    """Example 7: Display detailed strategy information"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Strategy Details & Configuration")
    print("="*80)
    
    strategies = STRATEGIES
    
    for name, config in list(strategies.items())[:2]:  # Show first 2 for brevity
        print(f"\n{name.upper()}")
        print(f"{'─'*70}")
        print(f"Description:         {config['description']}")
        print(f"Timeframe:           {config['timeframe']}")
        print(f"Holding Period:      {config['holding_period']}")
        print(f"Data Period:         {config['data_period']}")
        print(f"Data Interval:       {config['data_interval']}")
        print(f"\nProfit/Loss Targets:")
        print(f"  Profit Target:     {config['profit_target_percent']}%")
        print(f"  Stop Loss:         {config['stop_loss_percent']}%")
        print(f"  Risk:Reward:       {config['risk_reward_ratio']}:1")
        print(f"\nIndicator Settings:")
        for key, value in config['technical_indicators'].items():
            print(f"  {key:.<40} {value}")
    
    print()


def example_8_batch_analysis():
    """Example 8: Analyze portfolio across all strategies"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Portfolio Analysis - All Strategies")
    print("="*80)
    
    portfolio = ["SBIN-EQ", "INFY-EQ", "TCS-EQ"]
    print(f"\nAnalyzing portfolio: {', '.join(portfolio)}")
    print(f"Using all strategies: Scalping, Intraday, BTST, Swing, Momentum\n")
    
    for symbol in portfolio:
        print(f"\n{symbol:12s} PORTFOLIO ANALYSIS:")
        print("─" * 70)
        
        best_strategy = None
        best_confidence = 0
        
        for strategy in list(STRATEGIES.keys()):
            try:
                engine = StockRecommendationEngine(symbol, strategy=strategy)
                results = engine.run_full_analysis()
                rec = results['recommendation']
                
                if rec['confidence'] > best_confidence and rec['action'] in ['BUY', 'SELL']:
                    best_confidence = rec['confidence']
                    best_strategy = (strategy, rec)
                
                print(f"  {strategy:12s} | {rec['action']:<4s} | "
                      f"Conf: {rec['confidence']:5.1f}% | Target: {rec['profit_target_percent']:5.2f}%")
            
            except Exception as e:
                print(f"  {strategy:12s} | Error")
        
        if best_strategy:
            print(f"\n  ✓ BEST STRATEGY: {best_strategy[0].upper()} "
                  f"({best_strategy[1]['confidence']:.0f}% confidence)")
    
    print()


if __name__ == "__main__":
    print("\n" + "█"*80)
    print("█  MULTI-STRATEGY STOCK RECOMMENDATION EXAMPLES")
    print("█  Scalping | Intraday | BTST | Swing | Momentum")
    print("█"*80)
    
    try:
        example_1_all_strategies_comparison()
        example_2_scalping_strategy()
        example_3_intraday_strategy()
        example_4_btst_strategy()
        example_5_swing_strategy()
        example_6_momentum_strategy()
        example_7_strategy_details()
        example_8_batch_analysis()
        
        print("\n" + "█"*80)
        print("█  All examples completed successfully!")
        print("█  Next: Choose a strategy and run: python cli.py -s SYMBOL --strategy STRATEGY")
        print("█"*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
