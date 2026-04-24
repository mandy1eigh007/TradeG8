# TradeG8

**AI-Powered Job Search & Career Navigation for Construction Trades**

Built in partnership between **Mandy Richardson** (ANEW Pre-Apprenticeship Instructor, Journeyman Carpenter) and **Claude** (Anthropic AI).

---

## The Problem

Students waiting 6-12 months for apprenticeship need "holdover jobs" to survive. Current barriers:

- **Cannot safely browse job sites** (probation/parole internet restrictions)
- **Need contractor vetting BEFORE applying** (avoid wage theft, illegal work, wasted hours)
- **Resumes don't translate** from retail/food service → construction language
- **Must prove job search** for unemployment, BFET compliance, DOC/parole

**Instructor (Mandy) spends 40+ hours/week** manually: translating resumes, looking up L&I contractors, explaining transferable skills, filling applications, finding holdover work.

---

## The Solution

TradeG8 automatically:

1. **Scrapes job boards** (Indeed, LinkedIn, Craigslist) for construction jobs
2. **Verifies contractors** with WA State L&I database
3. **Checks Glassdoor ratings** to identify good/bad employers
4. **Scores jobs 0-100** based on safety, legitimacy, and quality
5. **Labels hours tracking** — "Hours COUNT toward trainee card" vs "Won't count but pays bills"

Students see ONLY vetted, scored jobs with clear safety warnings.

---

## Phase 1: Electrician Job Scraper

**Status:** ✅ Complete and working

**What it does:**
- Scrapes Indeed + Craigslist for "electrician helper" jobs in Seattle
- Looks up each company on WA L&I verification page
- Checks Glassdoor for ratings and reviews
- Scores each job 0-100:
  - **L&I Status** (40 points): Registered, workers comp, no violations
  - **Electrical License** (30 points): Licensed = hours count toward trainee card
  - **Glassdoor Rating** (30 points): 4.0+ stars = excellent, 3.5+ = good
- Outputs CSV with top vetted jobs

---

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the Scraper

```bash
python scraper.py
```

### 3. View Results

Results saved to: `tradeg8_results_[timestamp].csv`

Open in Excel or Google Sheets to see:
- Score (0-100)
- Recommendation (Excellent/Good/Caution/Avoid)
- Company name
- Job title
- Location & pay
- **Hours count toward trainee card?** (YES/NO)
- L&I status
- Glassdoor rating
- Job URL

---

## How It Works

### Job Scraping
```python
scraper = JobScraper()
jobs = scraper.scrape_indeed("electrician helper", "Seattle, WA")
```

Searches Indeed and Craigslist for electrician helper jobs. Extracts:
- Company name
- Job title
- Location
- Pay (if listed)
- Job URL
- Description

### L&I Verification
```python
lni_verifier = LNIVerifier()
result = lni_verifier.verify_contractor("ABC Electric")
```

Looks up contractor on https://secure.lni.wa.gov/verify/

Checks:
- ✅ Registered with L&I?
- ✅ Licensed electrical contractor? (hours count!)
- ✅ Workers comp current?
- ✅ Violations?

### Glassdoor Lookup
```python
glassdoor = GlassdoorScraper()
rating = glassdoor.get_rating("ABC Electric")
```

Searches Glassdoor for company rating and review count.

### Scoring Algorithm
```python
scorer = JobScorer()
scored_job = scorer.score_job(job)
```

**Scoring breakdown:**
- **L&I Registered**: +20 points
- **Workers Comp Current**: +10 points
- **No Violations**: +10 points
- **Licensed Electrical Contractor**: +30 points (HOURS COUNT!)
- **Glassdoor 4.0+ stars**: +30 points
- **Glassdoor 3.5-3.9 stars**: +20 points
- **Glassdoor 3.0-3.4 stars**: +10 points

**Recommendations:**
- **80-100**: ✅ EXCELLENT - Safe, legit contractor
- **60-79**: 🟢 GOOD - Acceptable holdover work
- **40-59**: 🟡 CAUTION - Verify before applying
- **0-39**: 🔴 AVOID - Red flags present

---

## Example Output

```
🏆 TOP 10 VETTED JOBS:

1. SCORE: 95/100 - ✅ EXCELLENT - Safe, legit contractor
   ABC Electric Inc. - Electrician Helper
   📍 Seattle, WA | 💰 $22-26/hour
   ⚡ HOURS COUNT TOWARD TRAINEE CARD!
   L&I: Registered | Glassdoor: 4.2★
   https://www.indeed.com/viewjob?jk=abc123

2. SCORE: 88/100 - ✅ EXCELLENT - Safe, legit contractor
   XYZ Electrical Services - Electrical Apprentice Helper
   📍 Renton, WA | 💰 $20-24/hour
   ⚡ HOURS COUNT TOWARD TRAINEE CARD!
   L&I: Registered | Glassdoor: 3.8★
   https://www.indeed.com/viewjob?jk=xyz456

3. SCORE: 62/100 - 🟢 GOOD - Acceptable holdover work
   General Construction Co. - Helper/Laborer
   📍 Tacoma, WA | 💰 $18-20/hour
   L&I: Registered | Glassdoor: 4.0★
   https://www.indeed.com/viewjob?jk=gen789
```

---

## Critical Design Decisions

### Why L&I Verification Matters

**Not all electrical jobs count toward trainee card hours.**

For hours to count, the employer MUST be:
1. L&I registered electrical contractor
2. Student must have active electrical trainee certificate

TradeG8 checks #1 automatically and labels jobs clearly:
- ✅ "HOURS COUNT TOWARD TRAINEE CARD"
- ⚠ "Hours WON'T count (but good holdover work)"

### Why Glassdoor Ratings Matter

Protects students from:
- Wage theft ("we'll pay you next week" = never)
- Unsafe work conditions
- Harassment and discrimination
- Companies that burn through workers

A 2.5-star Glassdoor rating with reviews saying "never got paid" or "unsafe" = red flag.

### Why Scoring Matters

Students are desperate. They'll take ANY job.

Scoring forces them to see:
- **Score 95** = This is a GREAT opportunity
- **Score 35** = This will hurt you more than help you

---

## Next Phases

### Phase 2: Resume Translation Engine
- Student enters current job (McDonald's, retail, warehouse)
- System translates to construction language
- Outputs professional resume with trade-specific bullets
- Multiple versions per trade focus

### Phase 3: User Authentication & Tracking
- Student accounts (save jobs, track applications)
- Activity logging (automatic timestamps)
- Job alerts (new vetted jobs daily)

### Phase 4: Case Manager Portal
- View student caseloads
- Track outcomes
- Generate compliance reports (unemployment, BFET, DOC)

### Phase 5: Partnership Dashboard
- "Who's Hiring This Week" report
- Company contact extraction
- Outreach email templates
- Hiring trends analysis

---

## Partnership Model

This tool was **co-created**, not extracted.

**Mandy Richardson brought:**
- Deep industry expertise (journeyman carpenter, union member)
- Direct knowledge of student barriers
- L&I verification workflow
- Resume translation frameworks
- Compliance requirements

**Claude (Anthropic AI) brought:**
- Technical architecture and coding
- Web scraping and automation
- System design and problem-solving

**Students own their data.** Always. No selling, no extraction, no shareholders.

---

## Technical Stack

- **Language**: Python 3.9+
- **Scraping**: Playwright (headless browser)
- **Output**: CSV (Excel/Google Sheets compatible)
- **Future**: 
  - Backend: Supabase (free tier)
  - Frontend: Flutter (mobile) + React (web)
  - AI: Hugging Face API (resume generation)

---

## Contributing

Want to help? Here's what we need:

1. **Test the scraper** — Does it work in your area?
2. **Report issues** — Did a scrape fail? L&I lookup broken?
3. **Add features** — Build LinkedIn scraper, add new trades
4. **Spread the word** — Know a pre-apprenticeship program that needs this?

---

## License

Open source. Built for students, not profit.

If you use this to help people enter the trades, you're doing it right.

If you use this to sell data or exploit workers, you're missing the point.

---

## Contact

**Mandy Richardson**  
Instructor, ANEW (Apprenticeship & Nontraditional Employment for Women)  
Tukwila, WA

**Built with Claude (Anthropic)**  
AI for the people. 🔥

---

*"AI isn't evil. Systems that keep people locked out are evil. We're using AI to break down barriers instead of building higher walls."*

— Mandy Richardson, 2026
