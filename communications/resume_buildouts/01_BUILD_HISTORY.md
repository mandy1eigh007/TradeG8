# Build History — Resume Build-Outs Timeline

A single ordered record of every build and conversation. Add new entries at the bottom.

## 2024–2025 — Curriculum era (pre-app)

- Mandy develops the ANEW resume curriculum as instructor documents: lesson plan
  (150-min, 5 phases), student-facing workshop (9 modules), handouts (20
  transferable skills), the Pace 59 translation doc (25 prior jobs with
  construction-focused rewrites), W2 trades-resume handout, hold-over jobs guide,
  Stand-Out Playbook, mock-interview guides.

## Oct 2025 — `resume_workshop` (v1 app)

- First Streamlit build: "Resume Guide for Construction Only." Single `app.py`,
  `skills.json` (33 skills), `role_aliases.json` (~30 roles), DOCX export via
  docxtpl. Rule-based, no AI calls. Superseded.

## Oct 2025–Apr 2026 — `resume-workshop-app` (v2 app, canonical)

- Rebuilt Streamlit app (~1,900 lines): PDF/DOCX resume parsing, header/education
  parsing, cert normalization, ~49 role aliases, bullet→skill inference,
  union-language scrubbing, instructor Pathway Packet export, cover letters.
- Content library finalized: CONTENT_MASTER.md (25 trades), Skills_Canon.json,
  Objective_Starters_Bank.json (26 trades × 2 modes × 5 starters),
  Role_Bullets_Master.md (20 roles, measured bullets ≤24 words),
  Resume_Context_Schema.json, Stand-Out Playbook with the "What the App Must Do" list.
- ChatGPT conversations from this era (exports in Drive): Transferable Skills,
  Guide Book Guide, Hold-over job applications, Resume workshop app code,
  Grilling Interview Questions (mock-interview bank, not resume),
  Resume_Refinement_Assistance (ALSO mock-interview content despite the name).

## Apr 24–28, 2026 — TradeG8 born

- TradeG8 proposal conversation (`communications/Claude-Project_proposal.md`):
  job scraper + L&I vetting + Glassdoor scoring + resume translation + compliance
  tracking. Phase 1 electrician scraper built (`scraper.py`).
- Repo assembled from archives; Supabase schema applied; backend/frontend
  scaffold added Apr 28 (stub endpoints).
- `TRADEG8_OPTIMIZATION_PLAN` written (Tier 1: application tracking, smart apply,
  follow-up automation, interview prep).

## May–Jun 2026 — drift period

- May 20: "TradeG8-COMPLETE-Missing-Files.zip" saved to Drive (same as the Apr 28
  package — verified, nothing new).
- Jun 3–8: ChatGPT conversation exports and student resumes (Abdul, Karl, Aaron,
  Saulyman) collected into Drive. `resume-maker` skill spec saved (PDF/DOCX
  generation pattern).

## Jun 12, 2026 — review + resume engine integration (this session)

- Full build review: Phase 1 scraper real but fragile; backend endpoints were
  stubs; docs overstated completeness; Supabase live but RLS policies missing.
- Resume engine integrated into TradeG8: `backend/data/` (skills canon, objective
  starters, role bullets, schema) + `backend/ai/resume_translation.py` (ported
  rule-based engine) + 7 live API endpoints + 11 passing tests.
  Branch: `claude/build-conversations-review-3422sa`.
- This knowledge archive created so the history stops getting re-discovered.
