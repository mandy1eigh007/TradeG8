# How We Teach Resumes — The Framework the App Must Encode

Synthesized from the ANEW curriculum documents and the ChatGPT build
conversations (sources inventoried in `00_SOURCE_INVENTORY.md`). This is the
pedagogy. App features should map to these stages.

## The one-line model

**Truth-locked translation**: real experience, rewritten in trade language,
never invented — delivered through locked additive templates, grounded in
Washington's verifiable systems (L&I, ARTS, trainee cards, ranking), pressure-
tested by grilling with receipts, written in plain language usable from a phone,
with the instructor always in the loop.

## The teaching sequence (workshop = 150 min, 5 phases; app mirrors it)

| Stage | What happens | Who does it | App support |
|-------|-------------|-------------|-------------|
| A. Inventory | Student lists what they actually did — jobs, volunteer, military, informal work. No blank page: scaffolded worksheets. | Student supplies truth | `/parse` endpoint: paste old resume → detected roles, certs, header |
| B. Translate | Each real job runs through the crosswalk: same facts, site language. Never claim construction experience that doesn't exist. | Instructor scaffolds, student picks what's true | Role bullet banks + `/role-bullets`; "use the ones that are true for you" |
| C. Standardize | Combination format, one page, ATS-safe. | Template enforces | `/generate` caps + cleaning |
| D. Tailor | Pull focus keywords from the actual job posting, map each to something true in the student's history. | Student + instructor | FUTURE: posting-keyword mapper |
| E. Deliver phone-first | Editable doc for fast sending; PDF for formal applications. Students may not own computers. | App | FUTURE: DOCX + PDF export |
| F. Cover letter | Short, plain, send-as-is. | App generates, student edits | Ported logic exists in resume-workshop-app, not yet in TradeG8 |
| G. Interview prep | Scripted true answers + memory joggers, then grilling mocks with instructor answer keys. | Instructor-led | FUTURE: grilling packets per trade (curriculum exists) |
| H. Hold-over track | Parallel: legal, L&I-verified interim work that protects countable hours. | Student executes checklist | TradeG8 job scoring + L&I verification IS this stage |

## Hard content rules (enforce in code, not in prose)

**Format:** one page; combination format; Calibri/Arial; name 20pt bold,
headers 12pt bold ALL CAPS, body 10.5–11pt; 1" margins (0.75" if spilling);
1.15 spacing; left-aligned; no images/graphics (ATS); PDF for submission.

**Section order:** Header → Objective/Summary → Skills → Work Experience →
Certifications → Education → Optional (volunteer/other).

**Objective:** 1–2 sentences; precise single job target (no "jack of all
trades"); union-neutral; for hold-over applications, state the apprenticeship
plan honestly ("Currently applying to registered apprenticeship programs for
[trade]. Seeking hold-over work…").

**Skills:** three buckets — Transferable, Job-Specific, Self-Management — at
least 5 each in the workshop, max 12 on the final page.

**Bullets:** action-verb led; ≥3 per job (≤4 on final page); ≤24 words;
quantify what's true ("cut assembly time by 20%", "cleaned 14+ rooms per
shift"); name the tool and the use ("Operated a table saw to cut framing
lumber"); the construction relevance lives INSIDE the rewritten bullet — never
append "this translates to…" explanations; no fluffy adjectives — measured
work and safety practices only.

**Certifications:** precise citations or nothing. "OSHA Outreach 10-Hour
(Construction)" — it's an outreach card, not a certification. Forklift =
employer evaluation on the specific truck, re-evaluated ≤3 years. WA Flagger
expires ≤3 years. EPA 608: state the type. Skills in training are allowed if
marked "in training". If no certs: "None yet" + plan.

**Honesty:** the #1 repeated rule across every source. Same employer, same
dates, same facts; only the language changes. Mark gaps rather than invent.

## The three-pass translation method (the signature move)

1. **Crosswalk** — "What You Did → What It Shows About You" (25 prior jobs
   covered in Pace 59: retail, food service, warehouse, janitorial, childcare,
   security, drivers, bank teller, bartender, stagehand, volunteer, etc.)
2. **Plain bullets** — the job as ordinary resume lines.
3. **Construction-focused rewrite** — same facts, site vocabulary: safety,
   clean work zones, checklists, physical capability, independence, team flow.

Example (warehouse): "Loaded and unloaded delivery trucks" → "Loaded and
unloaded freight safely and efficiently using pallet jacks and manual handling
techniques; maintained clean work zones and ensured clear access paths for
equipment movement."

**Gap:** an incarceration-era work crosswalk does not yet exist — author it
with Mandy using the same three passes.

## Interview prep (grilling) — the readiness audit

Per-trade packet, locked 8-section layout: general fit → pre-apprenticeship →
apprenticeship/local → non-union/hold-over/L&I → CITC/open-shop → city/utility
→ ranking/"while you wait" → instructor cheat sheet (answer key at bottom, so
co-instructors who don't know the trade can run mocks without page-flipping).

Standard push-harder trio for vague answers: (1) "Be specific — what exactly
did you do in the last 30–60 days?" (2) "What proof do you have right now?"
(3) "What exact local, training center, contractor, city program, or employer
are you talking about?"

Passing answers = **activity with receipts**: named pathway, current
requirements, accurate description of the work, recent action, documents in
hand. "I just want to work hard" fails.

## Hold-over jobs (the parallel lesson the rest of TradeG8 serves)

- Good hold-over job: legal, safe, near the tools, at/above minimum wage,
  ideally builds countable hours. "Not 'any job' — a legal, safe job that
  helps your long-term plan."
- L&I verification of every employer is **non-negotiable** (active status,
  bond/insurance, workers' comp, violations) plus training-agent status in
  ARTS if hours should count.
- Regulated trades: trainee card BEFORE the work; proper supervision ratios;
  chase affidavits of experience (electrical: employer has 20 days; plumbing:
  notarized within 30 days of renewal); keep a personal hours log + pay stubs.
  "Same body. Very different future."
- Red flags: 1099 misclassification, cash off books, no breaks, "apprentice"
  with no L&I paperwork, unreimbursed BYO-PPE, sub-minimum wage.
- Bridge programs to surface: King County Wastewater OIT, Seattle City Light
  BEAM and PAL, GovernmentJobs.com cohorts.

## What this means for TradeG8 features (mapping)

Already built (Jun 2026): role detection, vetted bullet banks, skills canon +
categorization, cert normalization, union scrubbing, one-page caps, objective
starters (26 trades × apprenticeship/job), text parsing, job scoring with L&I
lookup (scraper).

Build next, in pedagogy order:
1. DOCX/PDF export (Stage E — without a file in hand, nothing else lands)
2. Posting-keyword tailoring (Stage D)
3. Cover letter generation (Stage F — logic exists in resume-workshop-app)
4. Hours log + evidence vault (Stage H — also feeds compliance reporting)
5. Grilling packets / interview prep module (Stage G — curriculum exists)
6. Instructor review loop (every stage — case-manager accounts, Phase 4)
