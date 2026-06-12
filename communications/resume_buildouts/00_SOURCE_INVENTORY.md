# Source Inventory — Every Known Resume Build-Out Location

Last verified: 2026-06-12

## GitHub repos (account: mandy1eigh007)

| Repo | Status | What it is |
|------|--------|------------|
| **resume-workshop-app** (Dart label, mostly Python) | **CANONICAL content source** | Streamlit app (`app.py`, ~1,900 lines) + the vetted content library: `CONTENT_MASTER.md` (25 trades), `Skills_Canon.json`, `Objective_Starters_Bank.json` (26 trades × apprenticeship/job × 5 starters), `Role_Bullets_Master.md` (20 roles), `Resume_Context_Schema.json`, `Certification_Normalization.csv`, Stand-Out Playbook, Pathway Packet structure, Flutter `mobile_app/` |
| **resume_workshop** (Python) | Superseded / unused | Older single-file Streamlit build, "Resume Guide for Construction Only". Simpler `skills.json` + `role_aliases.json`. All improvements landed in resume-workshop-app. **Candidate home for this knowledge archive.** |
| **TradeG8** (Python) | **Active production target** | Job search + L&I vetting + resume + compliance platform. Resume engine ported from resume-workshop-app lives at `backend/ai/resume_translation.py` with data in `backend/data/` (integrated 2026-06-12, branch `claude/build-conversations-review-3422sa`) |

## Archives inside the TradeG8 repo (`contents/`)

`Resume -20260424T184228Z-3-001.zip` — the instructor curriculum + source apps:
- `Resume_Lesson_Plan.docx` — 150-minute lesson plan
- `Resume_Workshop_Student_Facing.docx` — student workbook (9 numbered modules)
- `Resume_Hand_Outs.docx` — 20 transferable skills, job-specific skills, vocabulary, online tools
- `W2 - Trades Resume - student handout.docx` — combination-format guidance
- `Pace 59 Transferable Skills to Construction (For People With No Experience).docx` — **the signature translation doc: 25 prior jobs, each with skill decoding + regular bullets + construction-focused rewrite**
- `Copy of Applying for "Hold-Over" Jobs While You Wait for Apprenticeship.docx` — hold-over strategy, L&I verification workflow, trainee cards, red flags
- `Instructor_Packet_Standout_Playbook.docx` — evidence > adjectives; credential truth-telling; trade-specific quick wins; **contains the verbatim "What the App Must Do" list**
- `Professional Resume - App content report.docx` — ChatGPT inventory of Mandy's personal evidence vault (design pattern: master evidence archive → tailored resumes)
- Mock interview instructor guides V1/V2; instructor pathway packets; 10 Resume Tips PDF
- `resume-workshop-app-main.zip` (two copies) and `reactive-resume-main.zip` (generic TS resume builder — reference only)

## Google Drive (account: mandy1eighrichardson@gmail.com)

ChatGPT conversation exports ("Resume Project GPT" folder, id `16jeJO0zf-bEZTyHnpRYxZqgXur7ACkko`):
- `ChatGPT - Resume APP - Resume workshop app code.md` — fileId `1naKX403oyRv6MEBQwE87obNi_-RCsDm6` (2.3MB, code history; code already captured in repos)
- `ChatGPT - Resume APP - Transferable Skills Construction Resume.md` — fileId `1SGfkXuQ2VjwzaPhWlSH7lQXcPr6FWlr9`
- `ChatGPT - Resume APP - Guide Book Guide.md` — fileId `1-jmU0PwZs4DgSoJ4nvKXfS_zYfTUTru0`
- `ChatGPT - Resume APP - Hold-over job applications.md` — fileId `1VMsMvpqsAgBROGcqfZ_ffAEVhlKXYwBQ`
- `ChatGPT - Resume APP - Grilling Interview Questions.md` — fileId `1vlO_KPiyewu44mEhg9SHff8-EWhDCpnF`
- `ChatGPT-Resume_Refinement_Assistance.md` — fileId `1IIhwLWtJxuXLEdjNsSS5kuGPOc6bt4Gy` (duplicates exist in other folders)

TradeG8 planning docs:
- `TRADEG8_OPTIMIZATION_PLAN.md.docx` — fileId `1tBgJJKPNY3QXFAaTFOf38hDMd8Y4PUvj` (the Tier 1/2/3 feature roadmap, April 28 2026)
- `App_TradeG8.md` — fileId `1QoWgrBVqQHOig1_QppHK98RiuhXXh23g` (one-page app card; 3 copies exist)
- `TradeG8-COMPLETE-Missing-Files.zip` — fileId `1Hjcv8TfSX_hJL8ZmxzaG0yqZ8_MVvoBd` — **verified identical to the April 28 package already applied to the repo; repo versions are newer. Do not re-apply.**
- `resume-maker/SKILL.md` — fileId `1ponkI69Yn3DhGlifG9kIw5bNVZt_--9_` — Claude skill spec for pixel-perfect one-page PDF/DOCX generation (jsPDF + docx npm, auto-fit algorithm). Blueprint for TradeG8 export feature.

Real student resumes (test inputs for the engine; folder id `1JXdiOENlLsULq87wB08QRyNvu2TVK2So`):
- Abdul Aman, Karl Kamara, Aaron DeSelms (June 8 2026 .docx generations + originals), Saulyman Corr (PDFs)

## Conversations inside the TradeG8 repo (`communications/`)

- `Claude-Project_proposal.md` — the TradeG8 origin conversation (vision, 5-phase roadmap, Phase 1 scraper build)
- `ACTIVITY_LOG.md` — running build log (sessions: 2026-04-24, 04-28, 06-12)
- An earlier file `Claude-Construction_industry_practice_platform_optimization` was the WRONG source (different app) and was removed — do not go looking for it.

## What does NOT exist (so you don't search for it)

- No GitHub PRs or issues on TradeG8 (history lives in the files above)
- No tool in Claude Code sessions to search claude.ai chat history across projects — exported files are the only bridge
