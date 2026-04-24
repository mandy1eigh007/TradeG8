#!/usr/bin/env python3
"""
TradeG8 - Run on Replit
Click the green RUN button to start scraping!
"""

import os
import sys

# Ensure we're using the right Python
print("🔧 Checking Python version...")
print(f"Python {sys.version}")
print()

# Run the scraper
print("=" * 80)
print("TradeG8 Phase 1: Electrician Job Scraper")
print("Built by Mandy Richardson & Claude (Anthropic)")
print("=" * 80)
print()
print("Starting job search...")
print("This will take 5-10 minutes. Go grab coffee! ☕")
print()

# Import and run
from scraper import main
main()

print()
print("=" * 80)
print("✅ DONE! Check the files panel on the left for your CSV file.")
print("=" * 80)
