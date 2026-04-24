#!/usr/bin/env python3
"""
TradeGate Phase 1: Electrician Job Scraper
Built by Mandy Richardson & Claude (Anthropic)

Scrapes job boards, verifies contractors with WA L&I, checks Glassdoor ratings,
and scores jobs to protect students from wage theft and unsafe work.
"""

import time
import csv
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


@dataclass
class Job:
    """Represents a vetted job posting"""
    title: str
    company: str
    location: str
    pay: str
    url: str
    source: str  # indeed, linkedin, craigslist
    posted_date: str
    description: str
    
    # L&I Verification
    lni_registered: bool = False
    lni_status: str = "Unknown"
    lni_licensed_electrical: bool = False
    lni_violations: int = 0
    lni_workers_comp: str = "Unknown"
    
    # Glassdoor
    glassdoor_rating: float = 0.0
    glassdoor_review_count: int = 0
    glassdoor_summary: str = ""
    
    # Scoring
    score: int = 0
    score_breakdown: str = ""
    hours_count_toward_trainee: bool = False
    recommendation: str = ""


class JobScraper:
    """Scrapes job boards for construction jobs"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.jobs: List[Job] = []
    
    def scrape_indeed(self, query: str, location: str, max_results: int = 20) -> List[Job]:
        """Scrape Indeed for jobs"""
        print(f"\n🔍 Scraping Indeed for '{query}' in {location}...")
        
        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            # Build Indeed URL
            search_query = query.replace(" ", "+")
            search_location = location.replace(" ", "+")
            url = f"https://www.indeed.com/jobs?q={search_query}&l={search_location}"
            
            try:
                page.goto(url, timeout=30000)
                page.wait_for_timeout(3000)  # Let page load
                
                # Find job cards
                job_cards = page.query_selector_all('div.job_seen_beacon')
                
                for card in job_cards[:max_results]:
                    try:
                        # Extract job details
                        title_elem = card.query_selector('h2.jobTitle span')
                        title = title_elem.inner_text() if title_elem else "Unknown Title"
                        
                        company_elem = card.query_selector('span[data-testid="company-name"]')
                        company = company_elem.inner_text() if company_elem else "Unknown Company"
                        
                        location_elem = card.query_selector('div[data-testid="text-location"]')
                        job_location = location_elem.inner_text() if location_elem else location
                        
                        # Get job link
                        link_elem = card.query_selector('h2.jobTitle a')
                        job_url = "https://www.indeed.com" + link_elem.get_attribute('href') if link_elem else ""
                        
                        # Try to get pay
                        pay_elem = card.query_selector('div.metadata.salary-snippet-container')
                        pay = pay_elem.inner_text() if pay_elem else "Not listed"
                        
                        # Try to get description snippet
                        desc_elem = card.query_selector('div.job-snippet')
                        description = desc_elem.inner_text() if desc_elem else ""
                        
                        job = Job(
                            title=title.strip(),
                            company=self._clean_company_name(company.strip()),
                            location=job_location.strip(),
                            pay=pay.strip(),
                            url=job_url,
                            source="Indeed",
                            posted_date=datetime.now().strftime("%Y-%m-%d"),
                            description=description.strip()
                        )
                        
                        jobs.append(job)
                        print(f"  ✓ Found: {job.company} - {job.title}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing job card: {str(e)}")
                        continue
                
            except PlaywrightTimeout:
                print("  ⚠ Indeed page timed out")
            except Exception as e:
                print(f"  ⚠ Error scraping Indeed: {str(e)}")
            finally:
                browser.close()
        
        print(f"  → Found {len(jobs)} jobs on Indeed")
        return jobs
    
    def scrape_linkedin(self, query: str, location: str, max_results: int = 20) -> List[Job]:
        """Scrape LinkedIn for jobs (simplified - LinkedIn blocks scrapers heavily)"""
        print(f"\n🔍 Scraping LinkedIn for '{query}' in {location}...")
        print("  ⚠ Note: LinkedIn heavily blocks scrapers. Results may be limited.")
        
        jobs = []
        # LinkedIn scraping would go here
        # For Phase 1, we'll focus on Indeed and add LinkedIn later
        print("  → LinkedIn scraping coming in Phase 2")
        return jobs
    
    def scrape_craigslist(self, query: str, location: str = "seattle", max_results: int = 20) -> List[Job]:
        """Scrape Craigslist for jobs"""
        print(f"\n🔍 Scraping Craigslist for '{query}' in {location}...")
        
        jobs = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            # Craigslist search URL
            search_query = query.replace(" ", "+")
            url = f"https://{location}.craigslist.org/search/jjj?query={search_query}"
            
            try:
                page.goto(url, timeout=30000)
                page.wait_for_timeout(2000)
                
                # Find job listings
                listings = page.query_selector_all('li.cl-static-search-result')
                
                for listing in listings[:max_results]:
                    try:
                        title_elem = listing.query_selector('div.title')
                        title = title_elem.inner_text() if title_elem else "Unknown Title"
                        
                        link_elem = listing.query_selector('a')
                        job_url = link_elem.get_attribute('href') if link_elem else ""
                        
                        # Craigslist doesn't show company in listing - need to visit page
                        # For now, mark as "See Posting"
                        company = "See Posting"
                        
                        meta_elem = listing.query_selector('div.meta')
                        meta = meta_elem.inner_text() if meta_elem else ""
                        
                        job = Job(
                            title=title.strip(),
                            company=company,
                            location=location.title(),
                            pay="See posting",
                            url=job_url,
                            source="Craigslist",
                            posted_date=datetime.now().strftime("%Y-%m-%d"),
                            description=meta
                        )
                        
                        jobs.append(job)
                        print(f"  ✓ Found: {job.title}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing listing: {str(e)}")
                        continue
                
            except Exception as e:
                print(f"  ⚠ Error scraping Craigslist: {str(e)}")
            finally:
                browser.close()
        
        print(f"  → Found {len(jobs)} jobs on Craigslist")
        return jobs
    
    def _clean_company_name(self, name: str) -> str:
        """Clean company name for L&I lookup"""
        # Remove common suffixes that might cause lookup issues
        suffixes = [" Inc.", " LLC", " Inc", " LLC.", " Corporation", " Corp", " Corp.", " Ltd", " Ltd."]
        clean_name = name
        for suffix in suffixes:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)]
        return clean_name.strip()


class LNIVerifier:
    """Verifies contractors with WA State L&I"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
    
    def verify_contractor(self, company_name: str) -> Dict:
        """Look up contractor on WA L&I verification page"""
        print(f"\n🔍 Checking L&I for: {company_name}")
        
        result = {
            "registered": False,
            "status": "Not Found",
            "licensed_electrical": False,
            "violations": 0,
            "workers_comp": "Unknown"
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                # WA L&I Contractor Search
                url = "https://secure.lni.wa.gov/verify/"
                page.goto(url, timeout=30000)
                page.wait_for_timeout(2000)
                
                # Enter company name
                search_input = page.query_selector('input[name="Name"]')
                if search_input:
                    search_input.fill(company_name)
                    
                    # Click search
                    search_button = page.query_selector('input[type="submit"]')
                    if search_button:
                        search_button.click()
                        page.wait_for_timeout(3000)
                        
                        # Check for results
                        # This is simplified - actual L&I page parsing would be more complex
                        page_text = page.content().lower()
                        
                        if "no records found" in page_text:
                            result["status"] = "Not Registered"
                            print(f"  ✗ Not registered with L&I")
                        else:
                            result["registered"] = True
                            result["status"] = "Registered"
                            
                            # Check for electrical license
                            if "electrical" in page_text or "electrician" in page_text:
                                result["licensed_electrical"] = True
                                print(f"  ✓ Licensed Electrical Contractor (HOURS COUNT!)")
                            else:
                                print(f"  ✓ Registered (not electrical)")
                            
                            # Check workers comp status
                            if "current" in page_text and "workers" in page_text:
                                result["workers_comp"] = "Current"
                            
                            # Check for violations (simplified)
                            if "violation" in page_text:
                                result["violations"] = 1  # Would need to parse actual count
                
            except Exception as e:
                print(f"  ⚠ Error verifying L&I: {str(e)}")
                result["status"] = "Error checking"
            finally:
                browser.close()
        
        return result


class GlassdoorScraper:
    """Scrapes Glassdoor for company ratings"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
    
    def get_rating(self, company_name: str) -> Dict:
        """Get Glassdoor rating for company"""
        print(f"\n🔍 Checking Glassdoor for: {company_name}")
        
        result = {
            "rating": 0.0,
            "review_count": 0,
            "summary": "No reviews found"
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                # Search Glassdoor
                search_query = company_name.replace(" ", "-")
                url = f"https://www.glassdoor.com/Search/results.htm?keyword={search_query}"
                page.goto(url, timeout=30000)
                page.wait_for_timeout(3000)
                
                # Try to find rating
                # Note: Glassdoor heavily protects against scraping
                # This is simplified and may need to be adjusted
                
                rating_elem = page.query_selector('[data-test="rating"]')
                if rating_elem:
                    rating_text = rating_elem.inner_text()
                    try:
                        result["rating"] = float(rating_text)
                    except:
                        pass
                
                review_elem = page.query_selector('[data-test="cell-Reviews-count"]')
                if review_elem:
                    review_text = review_elem.inner_text()
                    try:
                        result["review_count"] = int(re.sub(r'[^\d]', '', review_text))
                    except:
                        pass
                
                if result["rating"] > 0:
                    print(f"  ✓ Found: {result['rating']} stars ({result['review_count']} reviews)")
                    
                    # Generate simple summary based on rating
                    if result["rating"] >= 4.0:
                        result["summary"] = "Highly rated by employees"
                    elif result["rating"] >= 3.5:
                        result["summary"] = "Generally positive reviews"
                    elif result["rating"] >= 3.0:
                        result["summary"] = "Mixed reviews"
                    else:
                        result["summary"] = "Below average rating"
                else:
                    print(f"  ⚠ No rating found")
                
            except Exception as e:
                print(f"  ⚠ Error checking Glassdoor: {str(e)}")
            finally:
                browser.close()
        
        return result


class JobScorer:
    """Scores jobs based on L&I status and Glassdoor ratings"""
    
    def score_job(self, job: Job) -> Job:
        """Score job 0-100 based on safety and quality indicators"""
        score = 0
        breakdown = []
        
        # L&I Status (40 points max)
        if job.lni_registered:
            score += 20
            breakdown.append("L&I Registered (+20)")
            
            if job.lni_workers_comp == "Current":
                score += 10
                breakdown.append("Workers Comp Current (+10)")
            
            if job.lni_violations == 0:
                score += 10
                breakdown.append("No Violations (+10)")
        else:
            breakdown.append("NOT L&I Registered (0)")
        
        # Electrical License (30 points max)
        if job.lni_licensed_electrical:
            score += 30
            breakdown.append("Licensed Electrical Contractor (+30)")
            job.hours_count_toward_trainee = True
        else:
            breakdown.append("Not Electrical Contractor (0)")
        
        # Glassdoor Rating (30 points max)
        if job.glassdoor_rating >= 4.0:
            score += 30
            breakdown.append(f"Glassdoor {job.glassdoor_rating}★ (+30)")
        elif job.glassdoor_rating >= 3.5:
            score += 20
            breakdown.append(f"Glassdoor {job.glassdoor_rating}★ (+20)")
        elif job.glassdoor_rating >= 3.0:
            score += 10
            breakdown.append(f"Glassdoor {job.glassdoor_rating}★ (+10)")
        else:
            if job.glassdoor_rating > 0:
                breakdown.append(f"Glassdoor {job.glassdoor_rating}★ (0)")
            else:
                breakdown.append("No Glassdoor rating (0)")
        
        job.score = score
        job.score_breakdown = " | ".join(breakdown)
        
        # Generate recommendation
        if score >= 80:
            job.recommendation = "✅ EXCELLENT - Safe, legit contractor"
        elif score >= 60:
            job.recommendation = "🟢 GOOD - Acceptable holdover work"
        elif score >= 40:
            job.recommendation = "🟡 CAUTION - Verify before applying"
        else:
            job.recommendation = "🔴 AVOID - Red flags present"
        
        return job


def main():
    """Run the complete TradeGate job scraper"""
    print("=" * 80)
    print("TradeGate Phase 1: Electrician Job Scraper")
    print("Built by Mandy Richardson & Claude (Anthropic)")
    print("=" * 80)
    
    # Initialize components
    scraper = JobScraper(headless=True)
    lni_verifier = LNIVerifier(headless=True)
    glassdoor_scraper = GlassdoorScraper(headless=True)
    scorer = JobScorer()
    
    # Scrape jobs
    all_jobs = []
    
    # Indeed
    indeed_jobs = scraper.scrape_indeed("electrician helper", "Seattle, WA", max_results=10)
    all_jobs.extend(indeed_jobs)
    
    # Craigslist
    craigslist_jobs = scraper.scrape_craigslist("electrician helper", "seattle", max_results=10)
    all_jobs.extend(craigslist_jobs)
    
    print(f"\n{'='*80}")
    print(f"Total jobs found: {len(all_jobs)}")
    print(f"{'='*80}")
    
    # Verify each job with L&I and Glassdoor
    for i, job in enumerate(all_jobs, 1):
        print(f"\n[{i}/{len(all_jobs)}] Processing: {job.company}")
        
        # L&I Verification
        lni_result = lni_verifier.verify_contractor(job.company)
        job.lni_registered = lni_result["registered"]
        job.lni_status = lni_result["status"]
        job.lni_licensed_electrical = lni_result["licensed_electrical"]
        job.lni_violations = lni_result["violations"]
        job.lni_workers_comp = lni_result["workers_comp"]
        
        # Glassdoor Rating
        glassdoor_result = glassdoor_scraper.get_rating(job.company)
        job.glassdoor_rating = glassdoor_result["rating"]
        job.glassdoor_review_count = glassdoor_result["review_count"]
        job.glassdoor_summary = glassdoor_result["summary"]
        
        # Score the job
        job = scorer.score_job(job)
        
        # Rate limiting
        time.sleep(2)
    
    # Sort by score (highest first)
    all_jobs.sort(key=lambda x: x.score, reverse=True)
    
    # Save results to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"tradegate_results_{timestamp}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'score', 'recommendation', 'company', 'title', 'location', 'pay',
            'hours_count_toward_trainee', 'lni_status', 'lni_licensed_electrical',
            'glassdoor_rating', 'glassdoor_summary', 'source', 'url', 'score_breakdown'
        ])
        writer.writeheader()
        
        for job in all_jobs:
            writer.writerow({
                'score': job.score,
                'recommendation': job.recommendation,
                'company': job.company,
                'title': job.title,
                'location': job.location,
                'pay': job.pay,
                'hours_count_toward_trainee': 'YES' if job.hours_count_toward_trainee else 'NO',
                'lni_status': job.lni_status,
                'lni_licensed_electrical': 'YES' if job.lni_licensed_electrical else 'NO',
                'glassdoor_rating': job.glassdoor_rating if job.glassdoor_rating > 0 else 'N/A',
                'glassdoor_summary': job.glassdoor_summary,
                'source': job.source,
                'url': job.url,
                'score_breakdown': job.score_breakdown
            })
    
    print(f"\n{'='*80}")
    print(f"✅ Results saved to: {csv_filename}")
    print(f"{'='*80}")
    
    # Display top 10
    print("\n🏆 TOP 10 VETTED JOBS:\n")
    for i, job in enumerate(all_jobs[:10], 1):
        print(f"{i}. SCORE: {job.score}/100 - {job.recommendation}")
        print(f"   {job.company} - {job.title}")
        print(f"   📍 {job.location} | 💰 {job.pay}")
        if job.hours_count_toward_trainee:
            print(f"   ⚡ HOURS COUNT TOWARD TRAINEE CARD!")
        print(f"   L&I: {job.lni_status} | Glassdoor: {job.glassdoor_rating}★")
        print(f"   {job.url}")
        print()


if __name__ == "__main__":
    main()
