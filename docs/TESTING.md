# How to Test TradeG8

## Quick Test

```bash
python3 -m py_compile main.py test.py scraper.py
```

This confirms the current Python entry points parse cleanly.

## Backend Import Test

```bash
python3 -c "import main; print(main.app.title)"
```

If dependencies are missing, install them first:

```bash
pip install -r requirements.txt
```

## Full Backend Test

```bash
cd backend
python main.py
```

Visit: http://localhost:8000/docs

You should see the FastAPI docs with all endpoints.

Note: this requires the full backend application tree, including `backend/main.py` and the API modules. The current archive added setup scaffolding, but the full backend package tree is not yet present.

## Test Job Scraper

```bash
python3 -c "from scraper import JobScraper; s = JobScraper(); jobs = s.scrape_indeed('electrician helper', 'Seattle, WA', 5); print(f'Found {len(jobs)} jobs')"
```

## Test Full Stack

1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm start`
3. Open: http://localhost:3000

You should see the TradeG8 homepage.

Note: this requires the full `backend/` and `frontend/` application trees.
