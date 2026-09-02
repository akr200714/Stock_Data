"""
Flask API Server - REST API for stock recommendations
"""
from flask import Flask, request, jsonify
from recommendation_engine import StockRecommendationEngine
from chart_generator import ChartGenerator
import json
import traceback
from functools import wraps
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Store recent analyses for quick retrieval
analysis_cache = {}


def log_request(f):
    """Decorator to log API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[API] {request.method} {request.path}")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/health', methods=['GET'])
@log_request
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Stock Recommendation AI Agent'
    })


@app.route('/api/analyze', methods=['POST'])
@log_request
def analyze_stock():
    """
    Analyze a stock and generate recommendation
    
    Request body:
    {
        "symbol": "AAPL",
        "period": "1y",
        "interval": "1d"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'symbol' not in data:
            return jsonify({'error': 'Missing symbol parameter'}), 400
        
        symbol = data['symbol'].upper()
        period = data.get('period', '1y')
        interval = data.get('interval', '1d')
        generate_chart = data.get('generate_chart', True)
        
        print(f"Analyzing {symbol}...")
        
        # Run analysis
        engine = StockRecommendationEngine(symbol, period, interval)
        results = engine.run_full_analysis()
        
        # Generate chart if requested
        chart_path = None
        if generate_chart:
            try:
                generator = ChartGenerator(symbol, engine.df)
                chart_path = generator.generate_main_chart(
                    engine.technical_analyzer.indicators,
                    results['analysis']['support_resistance'],
                    results['current_price'],
                    results['recommendation']
                )
            except Exception as e:
                print(f"Warning: Could not generate chart: {str(e)}")
        
        # Cache the result
        analysis_cache[symbol] = results
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'data': results,
            'chart': chart_path
        })
    
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/compare', methods=['POST'])
@log_request
def compare_stocks():
    """
    Compare multiple stocks
    
    Request body:
    {
        "symbols": ["AAPL", "MSFT", "GOOGL"],
        "period": "1y",
        "interval": "1d"
    }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({'error': 'Missing symbols parameter'}), 400
        
        results = []
        for symbol in symbols:
            try:
                engine = StockRecommendationEngine(symbol, data.get('period', '1y'), 
                                                  data.get('interval', '1d'))
                analysis = engine.run_full_analysis()
                results.append({
                    'symbol': symbol,
                    'status': 'success',
                    'recommendation': analysis['recommendation'],
                    'current_price': analysis['current_price']
                })
            except Exception as e:
                results.append({
                    'symbol': symbol,
                    'status': 'error',
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'comparisons': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommendation/<symbol>', methods=['GET'])
@log_request
def get_recommendation(symbol):
    """Get recommendation for a specific stock"""
    try:
        symbol = symbol.upper()
        
        # Check cache first
        if symbol in analysis_cache:
            return jsonify({
                'success': True,
                'symbol': symbol,
                'data': analysis_cache[symbol]
            })
        
        # Run analysis if not cached
        engine = StockRecommendationEngine(symbol)
        results = engine.run_full_analysis()
        analysis_cache[symbol] = results
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'data': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/indicators/<symbol>', methods=['GET'])
@log_request
def get_indicators(symbol):
    """Get technical indicators for a stock"""
    try:
        symbol = symbol.upper()
        period = request.args.get('period', '1y')
        interval = request.args.get('interval', '1d')
        
        engine = StockRecommendationEngine(symbol, period, interval)
        engine.df = engine.data_handler.fetch_data()
        engine.technical_analyzer = __import__('technical_analysis').TechnicalAnalyzer(engine.df)
        indicators = engine.technical_analyzer.calculate_all_indicators()
        latest = engine.technical_analyzer.get_latest_indicators()
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'indicators': latest
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/levels/<symbol>', methods=['GET'])
@log_request
def get_levels(symbol):
    """Get support and resistance levels"""
    try:
        symbol = symbol.upper()
        period = request.args.get('period', '1y')
        interval = request.args.get('interval', '1d')
        
        engine = StockRecommendationEngine(symbol, period, interval)
        engine.df = engine.data_handler.fetch_data()
        engine.sr_analyzer = __import__('support_resistance').SupportResistanceAnalyzer(engine.df)
        levels = engine.sr_analyzer.find_levels()
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'levels': levels
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/orderblocks/<symbol>', methods=['GET'])
@log_request
def get_order_blocks(symbol):
    """Get order blocks for a stock"""
    try:
        symbol = symbol.upper()
        period = request.args.get('period', '1y')
        interval = request.args.get('interval', '1d')
        
        engine = StockRecommendationEngine(symbol, period, interval)
        engine.df = engine.data_handler.fetch_data()
        engine.ob_analyzer = __import__('order_blocks').OrderBlockAnalyzer(engine.df)
        blocks = engine.ob_analyzer.find_order_blocks()
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'blocks': blocks
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/liquidity/<symbol>', methods=['GET'])
@log_request
def get_liquidity(symbol):
    """Get liquidity analysis for a stock"""
    try:
        symbol = symbol.upper()
        period = request.args.get('period', '1y')
        interval = request.args.get('interval', '1d')
        
        engine = StockRecommendationEngine(symbol, period, interval)
        engine.df = engine.data_handler.fetch_data()
        engine.liquidity_analyzer = __import__('liquidity_analysis').LiquidityAnalyzer(engine.df)
        liquidity = engine.liquidity_analyzer.analyze_liquidity()
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'liquidity': liquidity
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cache', methods=['GET'])
@log_request
def get_cache_info():
    """Get cached analysis information"""
    return jsonify({
        'cached_symbols': list(analysis_cache.keys()),
        'cache_size': len(analysis_cache)
    })


@app.route('/api/cache/<symbol>', methods=['DELETE'])
@log_request
def clear_cache(symbol):
    """Clear cache for a specific symbol"""
    symbol = symbol.upper()
    if symbol in analysis_cache:
        del analysis_cache[symbol]
        return jsonify({'success': True, 'message': f'Cache cleared for {symbol}'})
    return jsonify({'error': 'Symbol not in cache'}), 404


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"Stock Recommendation AI Agent - Flask Server")
    print(f"{'='*60}")
    print(f"Starting server on http://0.0.0.0:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
