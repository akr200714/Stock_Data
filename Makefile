.PHONY: help install test run-cli run-api run-quickstart run-examples clean

help:
	@echo "Stock Recommendation AI Agent - Makefile Commands"
	@echo "=================================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install all dependencies"
	@echo "  make quickstart       - Run quick start setup and tests"
	@echo ""
	@echo "CLI Usage:"
	@echo "  make run-aapl         - Analyze AAPL (example)"
	@echo "  make run-cli          - Interactive CLI tool"
	@echo "  make run-compare      - Compare multiple stocks"
	@echo ""
	@echo "Server:"
	@echo "  make run-api          - Start Flask API server"
	@echo "  make run-api-debug    - Start API with debug mode"
	@echo ""
	@echo "Utilities:"
	@echo "  make run-examples     - Run all usage examples"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Clean generated files"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

quickstart:
	@echo "Running quick start setup..."
	python quickstart.py

run-cli:
	python cli.py -s AAPL

run-aapl:
	python cli.py -s AAPL --chart

run-msft:
	python cli.py -s MSFT --chart

run-tsla:
	python cli.py -s TSLA --chart

run-compare:
	python cli.py -s AAPL MSFT GOOGL AMZN NVDA

run-api:
	python api_server.py

run-api-debug:
	DEBUG_MODE=True python api_server.py

run-examples:
	python examples.py

test:
	@echo "Running tests..."
	python quickstart.py

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__ *.pyc .pytest_cache
	rm -rf charts/*.png
	rm -f *.json
	@echo "✓ Cleanup complete"

.DEFAULT_GOAL := help
