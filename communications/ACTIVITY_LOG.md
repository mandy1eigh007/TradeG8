# Activity Log

## 2026-04-24

### Setup
- Created the `communications/` folder to store project-history and reference documents.
- Added `communications/README.md` to define the folder purpose.
- Started this `communications/ACTIVITY_LOG.md` file as the running log for future work.
- Created the `contents/` folder for source materials and added `contents/README.md` to define its purpose.

### Current State
- Project review completed to understand the repo structure, runtime flow, and external dependencies.
- Confirmed the current scraper can return zero jobs because multiple live integrations are brittle or blocked.

### Communications Review
- Reviewed `communications/Claude-Construction_industry_practice_platform_optimization (1).md` to understand the app-creation history and prior planning context.
- Confirmed the uploaded communications file is a large mixed export containing chat history, project reviews, file listings, design references, and unrelated personal memory artifacts; future use should focus only on the app-relevant sections.
- Key product origin captured from the file: the app was originally framed as a construction practice/training platform for people entering the trades, not as a job scraper.
- Key historical assessment captured from the file: the technical foundation was considered solid, but the instructional content, real assets, and pedagogical sequencing were not complete.
- Key previously agreed priority order captured from the file: real tool images first, then vocabulary content, then math/context improvements, then week-module rewrites, then safety-module improvement.
- Important design context captured from the file: the intended audience was pre-apprentices and new entrants to construction, so content should be grounded in beginner needs rather than foreman- or journeyman-level expectations.

### Communications Correction
- User confirmed the earlier communications file was the wrong source for this repo and removed it.
- Reviewed the correct project-history file: `communications/Claude-Project_proposal.md`.
- Confirmed the correct origin story for this repo: TradeGate evolved from a broader construction-focused support concept into a job-search, contractor-vetting, resume-generation, and compliance-tracking platform.
- Confirmed the core intended user groups from the project proposal: students/job seekers, career navigators/case managers, and limited-access compliance officers.
- Confirmed the long-term feature vision from the project proposal: job scraping, L&I vetting, Glassdoor reputation scoring, resume translation, saved student profiles, case notes, compliance reporting, and partnership dashboards.
- Confirmed the current repo specifically descends from the “TradeGate Phase 1” prototype in the proposal: a Python/Playwright electrician job scraper with L&I lookup, Glassdoor lookup, scoring, CSV output, and supporting files like `README.md`, `setup.sh`, `test.py`, and `main.py`.
- Confirmed the proposal itself anticipated scraper fragility on Indeed and suggested alternatives such as Craigslist-first validation, API-based sourcing, or hybrid approaches.

### Contents Intake
- Confirmed a resume-source archive was uploaded to `contents/` as `Resume -20260424T184228Z-3-001.zip`.
- Confirmed the archive contains multiple resume workshop and instructor documents plus additional source app archives, including `resume-workshop-app-main.zip`, `resume-workshop-app-main(1).zip`, and `reactive-resume-main.zip`.

### Mission Understanding
- Confirmed the core mission of TradeGate is not “job scraping” by itself; it is a protective employment-access platform for people entering the trades who face systemic barriers to safe job search, application support, and compliance documentation.
- Confirmed the primary intended users are students seeking entry into construction trades, especially those navigating internet restrictions, supervision requirements, benefit compliance, or unstable access to opportunity.
- Confirmed the secondary intended users are career navigators and case managers who need better tools to support students without spending their time on repetitive manual job search, resume rewriting, and paperwork.
- Confirmed the tertiary intended users are limited-access compliance stakeholders such as parole officers, DOC staff, unemployment systems, and BFET-related reviewers who may need verified evidence of job-search activity.
- Confirmed the app’s intended ethical stance is student-first, anti-extractive, and grounded in co-creation: students should own their data, unsafe or exploitative employers should be filtered out, and the software should reflect lived workforce-development expertise rather than generic tech assumptions.

### Archive Application
- User asked to inspect the activity log after prior chat context was lost; reconstructed the project state from `communications/ACTIVITY_LOG.md` and `communications/Claude-Project_proposal.md`.
- User asked to unzip and apply the app build-out without hand-editing code.
- Inspected `contents/g8final.zip`; confirmed it contained the same nine root-level files already present in the repo and applied it with `unzip -o`, producing no tracked diff.
- User clarified that `g8final.zip` was the wrong file, removed it, uploaded `contents/trade8-complete-system.zip.zip`, and asked that future work be added to this activity log.
- Inspected `contents/trade8-complete-system.zip.zip`; confirmed it contains root-level project files: `README.md`, `UPLOAD_TO_GITHUB.md`, `BUILD_COMPLETE.md`, `main.py`, `requirements.txt`, `package.json`, `setup.sh`, `docker-compose.yml`, `LICENSE`, and `.gitignore`.
- Applied `contents/trade8-complete-system.zip.zip` to the repo root with `unzip -o`, replacing/updating root project files and adding new project-support files from the archive.
- User confirmed the corrected zip could be deleted after application; removed `contents/trade8-complete-system.zip.zip` and left the resume/source-materials archive in place.
- Ran smoke checks after archive application: `python3 -m py_compile main.py test.py scraper.py` passed, confirming the Python files parse cleanly.
- Ran import/startup smoke check with `python3 -c 'import main; print(main.app.title)'`; it failed because `fastapi` is not installed in the current environment.
- Noted an additional likely startup blocker from archive inspection: the applied `main.py` imports `api`, `database`, and `utils` packages, but those directories are not present in the current workspace.

### Critical Scaffold Additions
- User shared a recommended additions list for the completed TradeG8 system, emphasizing `backend/.env.example`, `backend/database/schema.sql`, `QUICKSTART.md`, resume translation frameworks, testing instructions, README improvements, and a richer health check.
- Added `backend/.env.example` documenting required Supabase, Hugging Face, JWT secret, environment, and CORS settings.
- Added `backend/database/schema.sql` with initial Supabase tables for users, jobs, saved jobs, compliance activity logs, and case notes.
- Added `backend/ai/resume_frameworks.py` with starter construction-language translation mappings and trade objectives to be expanded from the source materials in `contents/`.
- Added `QUICKSTART.md` with Replit/local setup instructions and a note that the full `backend/` and `frontend/` application trees are still required for full-stack startup.
- Added `docs/TESTING.md` with syntax, import, scraper, backend, and full-stack smoke-test instructions, including current-layout caveats.
- Updated the main `README.md` with "Who This Is For" and "Why TradeG8 is Different" sections, plus links to the new quickstart and testing docs.
- Updated root `main.py` health check to return detailed status including version and feature readiness flags for job scraping, resume AI, and database configuration.
- Updated `setup.sh` to handle the current root-file archive layout more gracefully by falling back to root `requirements.txt` and root `package.json` when `backend/` or `frontend/` are not yet present.
- Verification: `python3 -m py_compile main.py test.py scraper.py backend/ai/resume_frameworks.py` passed, and `bash -n setup.sh` passed.
- Import/startup smoke check still fails at `ModuleNotFoundError: No module named 'fastapi'`; after dependencies are installed, the missing full application packages may still need to be supplied or reconstructed.

### Database Schema Upgrade
- User asked whether Supabase access could be used to run the full TradeG8 database setup and provided an expanded schema.
- Replaced `backend/database/schema.sql` with the complete supplied schema, including tables for users, jobs, saved jobs, resumes, activity logs, case notes, compliance reports, and companies.
- The schema now includes role/status check constraints, L&I and Glassdoor fields, scoring fields, indexes, `updated_at` trigger function/triggers, optional seed data comments, and example RLS policy comments.
- User ran the schema in Supabase SQL Editor and reported the result as "ran no lines returned," which is expected for successful schema DDL when no SELECT query is included.
- User reran the schema and received `ERROR: 42P07: relation "users" already exists`, indicating at least the `users` table was already created in Supabase.
- User confirmed the Supabase schema verification is good; database setup is considered complete for the current schema.

### Uploaded Archive Verification
- User uploaded original archives and asked to verify `files` and `files2`.
- Found `backend/files.zip` and `backend/database/files2.zip`.
- Inspected both archives without applying them. Each contains only nine root-level Phase 1 prototype files (`GITHUB_SETUP.md`, `README.md`, `scraper.py`, `requirements.txt`, `LICENSE`, `.gitignore`, `setup.sh`, `test.py`, and `main.py`).
- Confirmed neither archive contains the missing full-stack application tree such as `backend/api/`, `backend/utils/`, `backend/scrapers/`, `frontend/src/`, or `frontend/public/`.
- Left both archives unextracted to avoid overwriting the newer scaffold and database/schema work.

### Commit Preparation
- User asked to commit everything and delete the last two uploaded zip files before zipping/exporting repo contents.
- Deleted `backend/files.zip` and `backend/database/files2.zip` after confirming they were old Phase 1 prototype bundles and not needed for the current scaffold.
- Created repository snapshot commit with the current TradeG8 scaffold, Supabase schema, docs, communications log, and source-materials archive.

## 2026-04-28

### Missing App Tree Package
- User provided the complete missing-files package intended to fill in the absent backend API and frontend scaffold.
- Added `backend/main.py`, backend package markers, and starter API routers for auth, jobs, and resumes.
- Added `backend/requirements.txt` and included `email-validator` because the auth router uses Pydantic `EmailStr`.
- Added the React frontend scaffold under `frontend/`, including `package.json`, `public/index.html`, `src/App.js`, and `src/index.js`.
- Added `docs/API.md` with starter endpoint documentation.
- Merged package config updates into existing `.gitignore`, `docker-compose.yml`, and root `requirements.txt` without replacing the stronger existing versions.
- Replaced stale root `main.py` with a compatibility launcher that imports the active backend app from `backend/main.py`.
- Updated quickstart/testing docs and README status language so they reflect the new scaffold instead of saying the backend/frontend trees are absent or fully complete.
- Ran scaffold verification checks: Python compile check passed for root/backend API/scraper/resume framework files, JSON parse check passed for root and frontend `package.json`, and `bash -n setup.sh` passed.
- Backend import smoke check still fails until dependencies are installed: `ModuleNotFoundError: No module named 'fastapi'`.
- Attempted Python dependency install from root `requirements.txt`; network access was approved after the sandboxed attempt failed on DNS.
- The first network-enabled install found a dependency conflict: `supabase==2.3.0` requires `httpx<0.25.0`, while root `requirements.txt` pinned `httpx==0.26.0`.
- Updated root `requirements.txt` to use `httpx==0.24.1`, which matches the Supabase client dependency range.
- Reran Python dependency install successfully after the `httpx` pin change. Pip warned that the shared JupyterLab environment prefers `httpx>=0.25.0`, but TradeG8's Supabase client requires the older compatible range.
- Installed frontend dependencies from `frontend/package.json` with approved npm network access; npm generated `frontend/package-lock.json`.
- npm install completed with audit warnings: 28 vulnerabilities reported in the React tooling dependency tree.
- Backend import smoke check now passes: `import main; print(main.app.title)` returns `TradeG8 API`.
- Direct backend scaffold checks passed for `health()` and `api.jobs.search_jobs(query="electrician")`.
- Frontend production build passed with `npm run build`; React generated the ignored `frontend/build/` output directory.
- Attempted the documented backend dependency path with `pip install -r backend/requirements.txt`; it failed because `torch==2.1.2` has no Python 3.12 build.
- Updated `backend/requirements.txt` to use `torch==2.2.0`, the first Torch version available for this environment, and aligned backend `transformers` to the root `4.37.0` pin.
- Reran `pip install -r backend/requirements.txt` successfully after the Torch pin update. This installed `torch==2.2.0+cu121`, `psycopg2-binary`, and the remaining backend-only dependencies.
- Final verification passed: root backend import returns `TradeG8 API`, backend `health()` returns `{"status": "healthy"}`, and `import torch; print(torch.__version__)` returns `2.2.0+cu121`.
