# Standing Product Decisions — Resume Build-Outs / TradeG8

These decisions were made across the build conversations. Do not re-litigate
them in future sessions; if one changes, update this file.

## Vision & users (from the TradeG8 proposal, Apr 2026)

- TradeG8 = protective, 100%-free employment-access platform for pre-apprentices
  facing barriers (supervised internet, benefit compliance, records, no laptop).
- Three user tiers: students; career navigators/case managers; limited read-only
  compliance stakeholders (DOC/BFET/unemployment).
- 5 phases: job engine → resume generator → student accounts → case management →
  partnership dashboard. Phase 1 done; Phase 2 (resume) underway as of Jun 2026.
- Free forever for students and programs. Never: charge students, sell data,
  premium tiers, ads, gated features.

## The optimization plan tiers (Apr 28, 2026)

- Tier 1 (before launch): application tracking, smart one-click apply,
  follow-up automation, trade-specific interview prep.
- Tier 2: employer response tracking, salary negotiation, criminal-record
  guidance (ban-the-box intelligence), compliance report auto-generation.
- Tier 3: peer referral network, worker-safety-focused employer ratings,
  SMS-first access.
- NOTE — realism check (Jun 2026 review): the plan's success metrics (50%
  interview rate, 50% placement) are aspirational targets, not commitments, and
  earlier docs (`BUILD_COMPLETE.md`, README "Production Ready") overstate what
  exists. Treat claims in those files as marketing drafts, not status.

## The app's non-negotiables (from the Stand-Out Playbook, verbatim list)

1. Keep the "Stand Out" section in the Instructor Pathway Packet after workshop
   reflections and before full-text attachments.
2. Preserve neutral language — no union/non-union labels in objectives.
3. Offer checklists by target trade (Electrical, Pipe/HVAC-R, Outside Line/Tree).
4. Resume bullets reflect measured work and safety practices — no vague adjectives.
5. If links are output, include official source URLs.

## Mandy's working rules for AI sessions (extracted from her corrections)

1. **Never fabricate.** "Provide only correct information. do not make stuff up."
   Mark gaps "not identified" instead of inventing. Anti-fabrication is the
   prime directive for any generated resume content.
2. **Additive iterations only.** "Do not take anything away. we are only adding."
   Never silently drop approved content; audit revisions for drops.
3. **Rewrite, don't explain.** Construction relevance lives inside the rewritten
   bullet — never append "this translates to..." commentary.
4. **Person-locked resumes.** Never blend one person's history into another's
   resume without explicit confirmation.
5. **Plain language for students; answer keys for instructors.** Dual-audience
   output, written for someone who may be working from a phone.
6. **One locked template per artifact type**, reused identically (per trade,
   per packet) — usability in the live classroom drives structure.
7. **Union-neutral, pathway-complete.** Cover union, non-union, CITC/open-shop,
   city/utility, and L&I trainee routes. No ideology; eyes-open warnings.
8. **Receipts over rhetoric.** "Activity with receipts, not dreams with garnish."
   Strong = named pathway + current requirements + recent action + proof docs.

## Technical decisions in force (Jun 2026)

- Resume engine is **rule-based** (no AI API dependency) — ported from
  resume-workshop-app into `backend/ai/resume_translation.py`. Content data in
  `backend/data/`. Hugging Face/LLM enhancement is optional future work, not a
  dependency.
- One-page caps enforced in code: 450-char summary, 12 skills, 8 certs, 3 jobs,
  4 bullets/job, 24 words/bullet. Union-language scrubbing on by default.
- Supabase is the database (project `Tradeg8`, id dskwuolufovhhrsappwx). Schema
  applied; RLS enabled but policies not yet written (required before client
  access). The Supabase project is shared with other ANEW tables (`anew_*`,
  `profiles`) — decide deliberately before separating.
- Export plan: DOCX/PDF following the Drive `resume-maker` skill pattern
  (single data source, one-page auto-fit) or docxtpl template from
  resume-workshop-app. Phone-first delivery: editable format + PDF for
  formal applications.
- Scraper strategy (acknowledged in the proposal itself): Craigslist-first /
  official APIs over fragile Indeed scraping.

## Known gaps (work to do, not yet decided away)

- Incarceration-era work translation crosswalk does not exist in any source —
  must be authored with Mandy using the same Pass 1→3 method.
- No RLS policies; no real auth; job search API not wired to scraper; frontend
  is a placeholder.
- Interview prep (grilling packets) exists as curriculum but not in the app.
