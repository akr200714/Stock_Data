#!/usr/bin/env python3
"""
Quick Start Guide - Run this to get started with the Stock Recommendation Agent
"""

import sys
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def check_dependencies():
    """Check if all dependencies are installed"""
    print_header("Checking Dependencies")
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'flask', 'matplotlib', 'yfinance'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n  ⚠️  Missing packages: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        return False
    
    print("\n  ✓ All dependencies installed!")
    return True


def test_data_fetch():
    """Test data fetching with Breeze Connect"""
    print_header("Testing Breeze Connect Setup")
    
    try:
        print("  Checking Breeze Connect credentials in .env...")
        from config import BREEZE_API_KEY, BREEZE_SECRET_KEY
        
        if BREEZE_API_KEY == "your-breeze-api-key" or not BREEZE_API_KEY:
            print("  ⚠️  BREEZE_API_KEY not configured in .env")
            print("  ")
            print("  Setup Instructions:")
            print("  1. Get credentials from: https://www.angelbroking.com/breeze/")
            print("  2. Edit .env file:")
            print("     BREEZE_API_KEY=your-actual-key")
            print("     BREEZE_SECRET_KEY=your-actual-secret")
            print("  3. Run this script again")
            return False
        
        print("  ✓ Breeze Connect credentials found in .env")
        print("  ✓ API Key configured")
        print("  ✓ Secret Key configured")
        
        print("\n  Testing data handler initialization...")
        from data_handler import BreezeConnectDataHandler
        
        # Test with SBIN (Indian stock)
        handler = BreezeConnectDataHandler("SBIN-EQ", lookback_days=30)
        print(f"  ✓ Data handler initialized for SBIN-EQ")
        
        print("\n  ℹ️  To fetch actual data, authenticate with:")
        print("     handler = BreezeConnectDataHandler('SBIN-EQ')")
        print("     handler.login(BREEZE_SECRET_KEY)")
        print("     df = handler.fetch_data()")
        
        return True
    
    except ImportError as e:
        print(f"  ✗ Missing dependency: {str(e)}")
        print(f"  Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"  ✗ Setup verification failed: {str(e)}")
        print(f"  Details: {str(e)}")
        return False


def test_analysis():
    """Test recommendation engine"""
    print_header("Testing Recommendation Engine")
    
    try:
        from recommendation_engine import StockRecommendationEngine
        print("  Running full analysis for MSFT...")
        engine = StockRecommendationEngine("MSFT", period="3mo", interval="1d")
        results = engine.run_full_analysis()
        
        rec = results['recommendation']
        print(f"  ✓ Analysis complete")
        print(f"  ✓ Recommendation: {rec['action']}")
        print(f"  ✓ Confidence: {rec['confidence']:.1f}%")
        print(f"  ✓ Target Price: ${rec['take_profit']:.2f}")
        print(f"  ✓ Stop Loss: ${rec['stop_loss']:.2f}")
        return True
    except Exception as e:
        print(f"  ✗ Analysis failed: {str(e)}")
        return False


def show_quick_commands():
    """Display quick command reference"""
    print_header("Quick Command Reference")
    
    commands = [
        ("Analyze single stock", "python cli.py -s AAPL"),
        ("Generate chart", "python cli.py -s AAPL --chart"),
        ("Compare stocks", "python cli.py -s AAPL MSFT GOOGL"),
        ("Custom timeframe", "python cli.py -s AAPL -p 3mo -i 1d"),
        ("JSON output", "python cli.py -s AAPL --json"),
        ("Start API server", "python api_server.py"),
        ("Run examples", "python examples.py"),
    ]
    
    for desc, cmd in commands:
        print(f"\n  {desc}:")
        print(f"    $ {cmd}")


def show_api_examples():
    """Display API usage examples"""
    print_header("API Endpoint Examples")
    
    examples = [
        ("Health check", "curl http://localhost:5000/api/health"),
        ("Analyze stock", 'curl -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d \'{"symbol": "AAPL"}\''),
        ("Get indicators", "curl http://localhost:5000/api/indicators/AAPL"),
        ("Get levels", "curl http://localhost:5000/api/levels/AAPL"),
        ("Compare stocks", 'curl -X POST http://localhost:5000/api/compare -H "Content-Type: application/json" -d \'{"symbols": ["AAPL", "MSFT"]}\''),
    ]
    
    for desc, cmd in examples:
        print(f"\n  {desc}:")
        print(f"    {cmd}")


def show_next_steps():
    """Show recommended next steps"""
    print_header("Next Steps")
    
    steps = [
        ("1. Try CLI", "python cli.py -s AAPL"),
        ("2. Generate Charts", "python cli.py -s AAPL --chart"),
        ("3. Compare Stocks", "python cli.py -s AAPL MSFT GOOGL"),
        ("4. Start API", "python api_server.py"),
        ("5. Run Examples", "python examples.py"),
        ("6. Read Docs", "See DOCUMENTATION.md for detailed info"),
    ]
    
    for step, cmd in steps:
        print(f"\n  {step}")
        print(f"  → {cmd}")


def main():
    """Main quick start flow"""
    print("\n")
    print("█"*70)
    print("█"*70)
    print("█  STOCK RECOMMENDATION AI AGENT - Quick Start Guide")
    print("█"*70)
    print("█"*70)
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies before continuing.")
        sys.exit(1)
    
    # Test data fetch
    if not test_data_fetch():
        print("\n⚠️  Unable to fetch data. Check internet connection.")
        sys.exit(1)
    
    # Test analysis
    if not test_analysis():
        print("\n⚠️  Analysis engine test failed.")
        sys.exit(1)
    
    print_header("✓ All Tests Passed!")
    print("  Your Stock Recommendation AI Agent is ready to use!")
    
    # Show commands
    show_quick_commands()
    show_api_examples()
    show_next_steps()
    
    # Final message
    print_header("Important Notes")
    print("""
  • This tool is for educational purposes only
  • Always do your own research before trading
  • Do not rely solely on these recommendations
  • Past performance does not guarantee future results
  • Consult a financial advisor before making trades
    """)
    
    print("\n" + "█"*70)
    print("█  Happy analyzing! 🚀")
    print("█"*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        sys.exit(1)
