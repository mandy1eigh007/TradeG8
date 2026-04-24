#!/bin/bash

echo "========================================="
echo "TradeGate Setup"
echo "Built by Mandy Richardson & Claude"
echo "========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install requirements
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

echo ""
echo "========================================="
echo "✅ Setup complete!"
echo "========================================="
echo ""
echo "To run the scraper:"
echo "  python3 scraper.py"
echo ""
echo "Results will be saved to:"
echo "  tradegate_results_[timestamp].csv"
echo ""
