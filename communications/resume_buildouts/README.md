# Resume Build-Outs — Canonical Knowledge Archive

**Purpose:** This folder is the single source of truth for everything related to
Mandy Richardson's resume build-outs (apps, curriculum, conversations, content).
It exists so that no future session — Claude, ChatGPT, or human — has to
re-discover this history again.

**Rule for future sessions:** Read this folder FIRST before doing any resume
work. Add what you learn here. Never let knowledge live only in a chat.

## Contents

| File | What it holds |
|------|---------------|
| `00_SOURCE_INVENTORY.md` | Every known resume build-out source: repos, Drive files (with file IDs), archives — and which one is canonical |
| `01_BUILD_HISTORY.md` | Timeline of every build and conversation, in order |
| `02_PRODUCT_DECISIONS.md` | The standing decisions: vision, users, content rules, roadmap, and corrections (what was rejected as unrealistic) |
| `03_TEACHING_FRAMEWORK.md` | How Mandy teaches resume writing — the pedagogy the app must encode |
| `04_CURRICULUM_NOTES.md` | Distilled content from the instructor curriculum documents |
| `05_INTERVIEW_PREP.md` | The grilling method: five-part rubric, per-trade packet layout, proof checklists |

## The one-paragraph context

Mandy Richardson is an ANEW pre-apprenticeship instructor and journeyman
carpenter. Her students wait 6–12 months for apprenticeship placement and need
safe "hold-over" jobs, resumes that translate non-construction experience into
trade language, and compliance documentation (BFET / unemployment / DOC). She
has built several resume tools with AI help; the current production target is
**TradeG8** (job search + vetting + resume + compliance). The resume engine in
TradeG8 (`backend/ai/resume_translation.py`) was ported from the
**resume-workshop-app** build-out, which is the canonical content source.
