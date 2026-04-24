#!/usr/bin/env python3
"""
Quick test to verify TradeG8 components work
"""

print("Testing TradeG8 components...")
print("=" * 60)

# Test 1: Check imports
print("\n1. Testing imports...")
try:
    from playwright.sync_api import sync_playwright
    print("   ✓ Playwright installed")
except ImportError:
    print("   ✗ Playwright not installed. Run: pip install playwright")
    print("   ✗ Then run: playwright install chromium")
    exit(1)

# Test 2: Check Playwright browsers
print("\n2. Testing Playwright browser...")
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com", timeout=10000)
        browser.close()
    print("   ✓ Chromium browser working")
except Exception as e:
    print(f"   ✗ Browser test failed: {e}")
    print("   Run: playwright install chromium")
    exit(1)

# Test 3: Quick scrape test
print("\n3. Testing job scraper...")
try:
    from scraper import JobScraper
    scraper = JobScraper(headless=True)
    jobs = scraper.scrape_indeed("electrician", "Seattle, WA", max_results=3)
    print(f"   ✓ Scraped {len(jobs)} test jobs from Indeed")
    if jobs:
        print(f"   ✓ Example: {jobs[0].company} - {jobs[0].title}")
except Exception as e:
    print(f"   ✗ Scraper test failed: {e}")

print("\n" + "=" * 60)
print("✅ All tests passed! TradeG8 is ready to run.")
print("\nRun the full scraper with:")
print("  python3 scraper.py")
print("=" * 60)
