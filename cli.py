#!/usr/bin/env python3
"""
CLI Interface for Stock Recommendation AI Agent
Command-line tool for analyzing stocks and generating recommendations
Supports multiple trading strategies: Scalping, Intraday, BTST, Swing, Momentum
"""
import sys
import argparse
from recommendation_engine import StockRecommendationEngine
from chart_generator import ChartGenerator
from strategy_config import list_all_strategies
import json


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Stock Recommendation AI Agent - Analyze stocks with multiple trading strategies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Analyze single stock (default: swing strategy)
  python cli.py -s SBIN-EQ
  
  # Use specific strategy
  python cli.py -s INFY-EQ --strategy intraday
  
  # Scalping analysis (fast trades)
  python cli.py -s TCS-EQ --strategy scalping --chart
  
  # Momentum trading (long-term trend)
  python cli.py -s RELIANCE-EQ --strategy momentum
  
  # BTST (Buy Today Sell Tomorrow)
  python cli.py -s HDFC-EQ --strategy btst
  
  # Compare multiple stocks with same strategy
  python cli.py -s SBIN-EQ INFY-EQ TCS-EQ --strategy swing
  
  # Output as JSON
  python cli.py -s SBIN-EQ --strategy intraday --json

STRATEGIES:
  scalping   - Ultra-short term (5-15 min), tight stops, 0.75% target
  intraday   - Same day (1-4 hours), moderate risk, 1.5% target  
  btst       - Overnight (4-16 hours), momentum-based, 1.2% target
  swing      - Medium term (2-5 days), strong trends, 3% target
  momentum   - Long-term (5+ days), trend following, 5% target
        """
    )
    
    parser.add_argument('-s', '--symbol', type=str, nargs='+', required=True,
                       help='Stock symbol(s) to analyze (e.g., SBIN-EQ, INFY-EQ)')
    parser.add_argument('--strategy', type=str, default='swing',
                       choices=['scalping', 'intraday', 'btst', 'swing', 'momentum'],
                       help='Trading strategy (default: swing)')
    parser.add_argument('-p', '--period', type=str, default=None,
                       choices=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'],
                       help='Time period for analysis (overrides strategy default)')
    parser.add_argument('-i', '--interval', type=str, default=None,
                       choices=['5m', '15m', '30m', '1h', '4h', '1d', '1wk'],
                       help='Data interval (overrides strategy default)')
    parser.add_argument('--chart', action='store_true',
                       help='Generate technical analysis chart')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--strategies', action='store_true',
                       help='List all available strategies')
    
    args = parser.parse_args()
    
    # Show available strategies
    if args.strategies:
        show_strategies()
        sys.exit(0)
    
    # Handle multiple symbols
    symbols = args.symbol if isinstance(args.symbol, list) else [args.symbol]
    
    if len(symbols) > 1:
        analyze_multiple(symbols, args)
    else:
        analyze_single(symbols[0], args)


def show_strategies():
    """Display all available trading strategies"""
    strategies = list_all_strategies()
    print(f"\n{'='*70}")
    print("AVAILABLE TRADING STRATEGIES")
    print(f"{'='*70}\n")
    
    for name, description in strategies.items():
        print(f"{name.upper():12s} - {description}")
    
    print(f"\nUse: python cli.py -s SYMBOL --strategy <strategy_name>")
    print(f"{'='*70}\n")


def analyze_single(symbol: str, args):
    """Analyze a single stock with specified strategy"""
    period = args.period  # Use provided period or let strategy default
    interval = args.interval  # Use provided interval or let strategy default
    
    try:
        # Create engine with strategy
        engine = StockRecommendationEngine(
            symbol, 
            period=period or "1y", 
            interval=interval or "1d",
            strategy=args.strategy
        )
        results = engine.run_full_analysis()
        
        if args.json:
            # Output JSON format
            print(json.dumps(results, indent=2, default=str))
        else:
            # Print formatted report
            rec = results['recommendation']
            
            print(f"\n{'='*70}")
            print(f"RECOMMENDATION: {rec['action']}")
            print(f"{'='*70}")
            print(f"Strategy:             {rec['strategy_name']} ({rec['timeframe']})")
            print(f"Holding Period:       {rec['holding_period']}")
            print(f"Current Price:        ₹{rec['current_price']:.2f}")
            print(f"Take Profit:          ₹{rec['take_profit']:.2f} (+{rec['profit_target_percent']:.2f}%)")
            print(f"Stop Loss:            ₹{rec['stop_loss']:.2f} (-{rec['risk_percent']:.2f}%)")
            print(f"Risk/Reward Ratio:    {rec['risk_reward_ratio']:.2f}:1")
            print(f"\nConfidence:           {rec['confidence']:.1f}%")
            print(f"Analysis Score:       {rec['score']:.1f}/100")
            print(f"Bullish Signals:      {rec['signal_count']['bullish']}")
            print(f"Bearish Signals:      {rec['signal_count']['bearish']}")
            
            print(f"\n{'─'*70}")
            print("DETAILED SIGNALS:")
            print(f"{'─'*70}")
            
            for category, signals in rec['signals'].items():
                if signals:
                    print(f"\n{category.upper()}:")
                    for signal in signals:
                        print(f"  • {signal}")
            
            print(f"\n{'='*70}\n")
            
            # Print analysis summary
            print("TECHNICAL INDICATORS:")
            print("─" * 70)
            for key, value in results['analysis']['technical'].items():
                if isinstance(value, float):
                    print(f"  {key:.<50} {value:.2f}")
                else:
                    print(f"  {key:.<50} {value}")
            
            print("\nSUPPORT & RESISTANCE:")
            print("─" * 70)
            sr = results['analysis']['support_resistance']
            print(f"  Support Levels:     {[f'₹{s:.2f}' for s in sr.get('support', [])]}")
            print(f"  Resistance Levels:  {[f'₹{r:.2f}' for r in sr.get('resistance', [])]}")
            
            print("\nORDER BLOCKS:")
            print("─" * 70)
            ob = results['analysis']['order_blocks']
            print(f"  Bullish Blocks:     {ob['bullish_count']}")
            print(f"  Bearish Blocks:     {ob['bearish_count']}")
            
            print("\nLIQUIDITY ANALYSIS:")
            print("─" * 70)
            liq = results['analysis']['liquidity']
            print(f"  Grade:              {liq['liquidity_grade']}")
            print(f"  Score:              {liq['liquidity_score']}/100")
            print(f"  Volume Trend:       {liq['volume_trend']}")
            print(f"  Volume vs Average:  {liq['volume_vs_average']:.2f}x")
        
        # Generate chart if requested
        if args.chart:
            print("\nGenerating chart...")
            generator = ChartGenerator(symbol, engine.df)
            chart_path = generator.generate_main_chart(
                engine.technical_analyzer.indicators,
                results['analysis']['support_resistance'],
                results['current_price'],
                results['recommendation']
            )
            
            ob_path = generator.generate_order_blocks_chart(
                results['analysis']['order_blocks']
            )
            print(f"✓ Charts generated successfully")
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


def analyze_multiple(symbols: list, args):
    """Compare multiple stocks with same strategy"""
    print(f"\n{'='*70}")
    print(f"Comparing {len(symbols)} stocks")
    print(f"Strategy: {args.strategy.upper()}")
    print(f"{'='*70}\n")
    
    comparisons = []
    
    for symbol in symbols:
        try:
            print(f"Analyzing {symbol}...", end=' ')
            period = args.period or "1y"
            interval = args.interval or "1d"
            engine = StockRecommendationEngine(
                symbol, 
                period=period, 
                interval=interval,
                strategy=args.strategy
            )
            results = engine.run_full_analysis()
            rec = results['recommendation']
            comparisons.append({
                'symbol': symbol,
                'status': 'success',
                'price': rec['current_price'],
                'recommendation': rec['action'],
                'confidence': rec['confidence'],
                'score': rec['score'],
                'tp': rec['take_profit'],
                'sl': rec['stop_loss'],
                'rr': rec['risk_reward_ratio']
            })
            print("✓")
        except Exception as e:
            print(f"✗ ({str(e)})")
            comparisons.append({
                'symbol': symbol,
                'status': 'error',
                'error': str(e)
            })
    
    # Display comparison table
    print(f"\n{'='*100}")
    print(f"{'Symbol':<12} {'Price':<12} {'Action':<8} {'Conf%':<8} {'Score':<8} {'TP':<12} {'SL':<12} {'R:R':<8}")
    print(f"{'='*100}")
    
    for comp in comparisons:
        if comp['status'] == 'success':
            symbol = comp['symbol']
            price = f"₹{comp['price']:.2f}"
            action = comp['recommendation']
            conf = f"{comp['confidence']:.1f}%"
            score = f"{comp['score']:.1f}"
            tp = f"₹{comp['tp']:.2f}"
            sl = f"₹{comp['sl']:.2f}"
            rr = f"{comp['rr']:.2f}:1"
            print(f"{symbol:<12} {price:<12} {action:<8} {conf:<8} {score:<8} {tp:<12} {sl:<12} {rr:<8}")
        else:
            print(f"{comp['symbol']:<12} {'ERROR':<12} {comp['error']:<60}")
    
    print(f"{'='*100}\n")


if __name__ == '__main__':
    main()
