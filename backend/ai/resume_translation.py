"""
TradeG8 Resume Translation Engine

Rule-based construction resume engine ported from Mandy Richardson's
resume-workshop-app (github.com/mandy1eigh007/resume-workshop-app).
No AI API required: role detection, skill inference, cert normalization,
and resume assembly all run on instructor-vetted rules and content.

Content data lives in backend/data/:
- skills_canon.json          vetted skill labels by category
- objective_starters.json    per-trade objective starters (apprenticeship/job)
- role_bullets.json          measured duty bullets per prior role
- resume_context_schema.json JSON Schema for the assembled resume
"""

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Resume shape limits (one-page discipline, from the workshop content spec)
MAX_SUMMARY_CHARS = 450
MAX_SKILLS = 12
MAX_CERTS = 8
MAX_JOBS = 3
MAX_BULLETS_PER_JOB = 4
MAX_SCHOOLS = 2

# Union/non-union language is scrubbed so resumes stay neutral and students
# are never labeled by affiliation before they're even hired.
UNION_BANS = [
    r"\bunion\b", r"\bnon[-\s]?union\b", r"\bibew\b", r"\blocal\s*\d+\b",
    r"\binside\s*wire(man|men)?\b", r"\blow[-\s]?voltage\b",
    r"\bsound\s+and\s+communication(s)?\b", r"\bneca\b", r"\bopen[-\s]?shop\b",
]
BANNED_RE = re.compile("|".join(UNION_BANS), re.I)
FILLER_LEADS = re.compile(
    r"^\s*(responsible for|duties included|tasked with|in charge of)\s*:?\s*", re.I
)
MULTISPACE = re.compile(r"\s+")
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(\+?1[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}")
PHONE_DIGITS = re.compile(r"\D+")
CITY_STATE_RE = re.compile(r"\b([A-Za-z .'-]{2,}),\s*([A-Za-z]{2})\b")
DATE_RANGE_RE = re.compile(
    r"(?P<start>(?:\d{4}|\w{3,9}\s+\d{4}))\s*(?:–|-|to|until|through)\s*"
    r"(?P<end>(?:Present|Current|\d{4}|\w{3,9}\s+\d{4}))",
    re.I,
)
SECTION_HEADERS = re.compile(
    r"^(objective|summary|professional summary|skills|core competencies|experience|"
    r"work history|employment|education|certifications|certificates|references|"
    r"contact|profile|qualifications|career|background|achievements|accomplishments|"
    r"projects|volunteer|activities|interests|technical skills|languages|awards|"
    r"honors|publications|training|licenses|memberships)$",
    re.I,
)


def _load_json(name: str) -> Dict[str, Any]:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


SKILLS_CANON: Dict[str, List[str]] = _load_json("skills_canon.json")["skillsCanon"]
OBJECTIVE_STARTERS: Dict[str, Dict[str, List[str]]] = _load_json(
    "objective_starters.json"
)["objectiveStarters"]
ROLE_BULLETS: Dict[str, List[str]] = _load_json("role_bullets.json")["roleBullets"]
TRADES: List[str] = sorted(OBJECTIVE_STARTERS.keys())


# ─────────────────────────────────────────────────────────
# Basic cleaners
# ─────────────────────────────────────────────────────────
def strip_banned(text: str) -> str:
    return BANNED_RE.sub("", text or "").strip()


def norm_ws(s: str) -> str:
    return MULTISPACE.sub(" ", (s or "").strip())


def cap_first(s: str) -> str:
    s = norm_ws(s)
    return s[:1].upper() + s[1:] if s else s


def clean_phone(s: str) -> str:
    digits = PHONE_DIGITS.sub("", s or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return norm_ws(s or "")


def clean_email(s: str) -> str:
    return (s or "").strip().lower()


def clean_bullet(s: str) -> str:
    """Normalize a duty bullet: strip markers/filler, cap at 24 words."""
    s = norm_ws(s)
    s = re.sub(r"^[•\-•]+\s*", "", s)
    s = FILLER_LEADS.sub("", s)
    s = re.sub(r"\.+$", "", s)
    s = cap_first(s)
    words = s.split()
    return " ".join(words[:24]) if len(words) > 24 else s


def split_list(raw: str) -> List[str]:
    if not raw:
        return []
    parts = [p.strip(" •\t") for p in re.split(r"[,\n;•]+", raw)]
    return [p for p in parts if p]


def parse_dates(raw: str) -> Tuple[str, str]:
    raw = norm_ws(raw)
    m = DATE_RANGE_RE.search(raw)
    if m:
        return (m.group("start"), m.group("end"))
    if "–" in raw or "-" in raw:
        sep = "–" if "–" in raw else "-"
        bits = [b.strip() for b in raw.split(sep, 1)]
        if len(bits) == 2:
            return bits[0], bits[1]
    return (raw, "") if raw else ("", "")


# ─────────────────────────────────────────────────────────
# Skills: canon, synonyms, inference, categorization
# ─────────────────────────────────────────────────────────
SKILL_CANON = [
    "Problem-solving", "Critical thinking", "Attention to detail", "Time management",
    "Teamwork & collaboration", "Adaptability & willingness to learn",
    "Safety awareness", "Conflict resolution", "Customer service", "Leadership",
    "Reading blueprints & specs", "Hand & power tools",
    "Materials handling (wood/concrete/metal)", "Operating machinery",
    "Trades math & measurement", "Regulatory compliance",
    "Physical stamina & dexterity",
]
_SKILL_SYNONYMS = {
    "problem solving": "Problem-solving", "problem-solving": "Problem-solving",
    "critical-thinking": "Critical thinking",
    "attention to details": "Attention to detail",
    "time-management": "Time management", "teamwork": "Teamwork & collaboration",
    "collaboration": "Teamwork & collaboration",
    "adaptability": "Adaptability & willingness to learn",
    "willingness to learn": "Adaptability & willingness to learn",
    "safety": "Safety awareness", "customer service skills": "Customer service",
    "leadership skills": "Leadership", "blueprints": "Reading blueprints & specs",
    "tools": "Hand & power tools", "machinery": "Operating machinery",
    "math": "Trades math & measurement", "measurements": "Trades math & measurement",
    "compliance": "Regulatory compliance", "stamina": "Physical stamina & dexterity",
    "forklift": "Operating machinery",
}
TRANSFERABLE_KEYWORDS = {
    "problem": "Problem-solving", "solve": "Problem-solving",
    "troubleshoot": "Problem-solving", "analyz": "Critical thinking",
    "priorit": "Time management", "deadline": "Time management",
    "detail": "Attention to detail", "team": "Teamwork & collaboration",
    "collabor": "Teamwork & collaboration",
    "adapt": "Adaptability & willingness to learn",
    "learn": "Adaptability & willingness to learn", "safety": "Safety awareness",
    "osha": "Safety awareness", "customer": "Customer service", "lead": "Leadership",
    "blueprint": "Reading blueprints & specs", "spec": "Reading blueprints & specs",
    "tool": "Hand & power tools", "drill": "Hand & power tools",
    "saw": "Hand & power tools", "forklift": "Operating machinery",
    "material": "Materials handling (wood/concrete/metal)",
    "machin": "Operating machinery", "math": "Trades math & measurement",
    "measure": "Trades math & measurement", "code": "Regulatory compliance",
    "permit": "Regulatory compliance", "compliance": "Regulatory compliance",
    "stamina": "Physical stamina & dexterity", "lift": "Physical stamina & dexterity",
}
_JOB_SPECIFIC = {
    "Reading blueprints & specs", "Hand & power tools", "Operating machinery",
    "Materials handling (wood/concrete/metal)", "Trades math & measurement",
    "Regulatory compliance", "Safety awareness",
}
_SELF_MANAGEMENT = {
    "Leadership", "Adaptability & willingness to learn",
    "Physical stamina & dexterity",
}


def normalize_skill_label(s: str) -> str:
    base = (s or "").strip()
    key = re.sub(r"\s+", " ", base.lower())
    mapped = _SKILL_SYNONYMS.get(key)
    if mapped:
        return mapped
    return re.sub(r"\s+", " ", base).strip().title()


def suggest_transferable_skills_from_text(text: str) -> List[str]:
    hits: Dict[str, int] = {}
    low = (text or "").lower()
    for kw, skill in TRANSFERABLE_KEYWORDS.items():
        if kw in low:
            hits[skill] = hits.get(skill, 0) + 1
    ordered = [s for s, _ in sorted(hits.items(), key=lambda kv: -kv[1])]
    return [s for s in SKILL_CANON if s in ordered][:8]


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {
        "Transferable": [], "Job-Specific": [], "Self-Management": []
    }
    seen = set()
    for s in skills:
        lab = normalize_skill_label(s)
        if not lab or lab.lower() in seen:
            continue
        seen.add(lab.lower())
        if lab in _JOB_SPECIFIC:
            out["Job-Specific"].append(lab)
        elif lab in _SELF_MANAGEMENT:
            out["Self-Management"].append(lab)
        else:
            out["Transferable"].append(lab)
    return out


# ─────────────────────────────────────────────────────────
# Certifications
# ─────────────────────────────────────────────────────────
CERT_MAP = {
    "osha": "OSHA Outreach 10-Hour (Construction)",
    "osha-10": "OSHA Outreach 10-Hour (Construction)",
    "osha 10": "OSHA Outreach 10-Hour (Construction)",
    "osha10": "OSHA Outreach 10-Hour (Construction)",
    "osha 30": "OSHA Outreach 30-Hour (Construction)",
    "osha-30": "OSHA Outreach 30-Hour (Construction)",
    "osha30": "OSHA Outreach 30-Hour (Construction)",
    "flagger": "WA Flagger (expires 3 years from issuance)",
    "wa flagger": "WA Flagger (expires 3 years from issuance)",
    "forklift": "Forklift — employer evaluation on hire",
    "fork lift": "Forklift — employer evaluation on hire",
    "cpr": "CPR",
    "first aid": "First Aid",
    "firstaid": "First Aid",
    "aerial lift": "Aerial Lift",
    "confined space": "Confined Space",
    "traffic control": "Traffic Control",
}


def parse_certs(text: str) -> List[str]:
    low = (text or "").lower()
    out = set()
    for k, v in CERT_MAP.items():
        if re.search(rf"\b{re.escape(k)}\b", low):
            out.add(v)
    return sorted(out)


# ─────────────────────────────────────────────────────────
# Role detection + bullet suggestions
# ─────────────────────────────────────────────────────────
ROLE_ALIASES = {
    "Line Cook": ["line cook", "cook", "kitchen"],
    "Prep Cook": ["prep cook", "prep"],
    "Server": ["server", "waiter", "waitress", "front of house", "foh"],
    "Dishwasher": ["dishwasher", "dishes"],
    "Barista": ["barista", "coffee"],
    "Cashier": ["cashier", "till", "pos"],
    "Retail Associate": ["retail associate", "retail", "sales associate"],
    "Stocker": ["stocker", "stocking", "stock clerk"],
    "Warehouse Associate": ["warehouse associate", "warehouse", "whse"],
    "Order Selector": ["order selector", "selector", "order picker", "picker"],
    "Shipping & Receiving": ["shipping", "receiving", "ship", "receive"],
    "Material Handler": ["material handler", "materials", "handler"],
    "Forklift Operator (trainee/experience)": ["forklift", "lift truck", "fork truck"],
    "Delivery Driver (Non-CDL)": ["delivery driver", "driver", "courier"],
    "Mover": ["mover", "moving"],
    "Janitor": ["janitor", "custodian"],
    "Custodian": ["custodian", "janitor"],
    "Housekeeper": ["housekeeper", "housekeeping", "room attendant"],
    "Security Guard": ["security", "guard"],
    "Landscaper/Groundskeeper": ["landscaper", "grounds", "groundskeeper", "mowing"],
    "Construction Laborer (general)": ["construction laborer", "laborer", "construction"],
    "Demolition Laborer": ["demolition", "demo"],
    "Traffic Control/Flagger": ["flagger", "traffic control"],
    "Tool Room Attendant": ["tool room", "tool attendant", "toolroom"],
    "Parts Counter": ["parts counter", "parts"],
    "Facilities Porter": ["porter", "facilities porter"],
    "Event Setup Crew/Stagehand": ["stagehand", "event setup", "av crew"],
    "Maintenance Helper": ["maintenance helper", "maintenance"],
    "Painter Helper": ["painter helper", "paint prep", "painter"],
    "Drywall/Lather Helper": ["drywall", "lather", "sheetrock"],
    "Flooring Helper": ["flooring helper", "flooring"],
    "Concrete Laborer": ["concrete laborer", "concrete"],
    "Mason Tender": ["mason tender", "masonry helper", "masonry"],
    "Carpenter Helper": ["carpenter helper", "carpenter", "framing"],
    "Roofer Helper": ["roofer", "roofing"],
    "HVAC Helper": ["hvac helper", "hvac"],
    "Electrical Helper": ["electrical helper", "electrician helper", "electrical"],
    "Plumbing Helper": ["plumbing helper", "plumbing", "plumber helper"],
    "Sheet Metal Helper": ["sheet metal helper", "sheet metal"],
    "Ironworker Helper": ["ironworker helper", "ironworker"],
    "Glazier Helper": ["glazier", "glazier helper", "glass"],
    "Welder/Fabrication Helper": ["welder", "fabrication", "fab"],
    "Grounds/Right-of-Way Helper": ["right of way", "row", "grounds"],
    "Warehouse Clerk": ["warehouse clerk", "inventory clerk"],
    "Assembler (Light Manufacturing)": ["assembler", "assembly", "light manufacturing"],
    "Kitchen Helper": ["kitchen helper", "kitchen staff"],
    "Busser": ["busser", "bus boy", "busboy", "bussing"],
    "Host": ["host", "hostess"],
    "Recycling Sorter": ["recycling", "sorter", "recycler"],
    "Delivery Helper": ["delivery helper", "delivery assistant"],
    "General Laborer": ["general laborer", "general labor", "day labor", "day laborer"],
}


def detect_roles_from_text(text: str, all_roles: Optional[List[str]] = None) -> List[str]:
    roles = all_roles if all_roles is not None else list(ROLE_ALIASES.keys())
    low = (text or "").lower()
    found = set()
    for r in roles:
        terms = ROLE_ALIASES.get(r, [r.lower()])
        for t in terms:
            if re.search(rf"\b{re.escape(t)}\b", low):
                found.add(r)
                break
    return [r for r in roles if r in found][:12]


def bullets_for_role(role: str) -> List[str]:
    """Vetted, measured bullets for a prior role (exact, then fuzzy match)."""
    if role in ROLE_BULLETS:
        return ROLE_BULLETS[role]
    low = norm_ws(role).lower()
    for name, bullets in ROLE_BULLETS.items():
        if low and (low in name.lower() or name.lower() in low):
            return bullets
    return []


BULLET_SKILL_HINTS = [
    (re.compile(r"\b(clean|organize|stage|restock|housekeep|walkway|sweep|debris)\b", re.I),
     "Attention to detail"),
    (re.compile(r"\b(pallet|forklift|lift|jack|rig|hoist|carry|load|unload|stack)\b", re.I),
     "Materials handling (wood/concrete/metal)"),
    (re.compile(r"\b(conduit|measure|layout|prints?|drawings?)\b", re.I),
     "Reading blueprints & specs"),
    (re.compile(r"\b(grinder|drill|saw|snips|hand tools|power tools|torch)\b", re.I),
     "Hand & power tools"),
    (re.compile(r"\b(ppe|osha|lockout|tagout|loto|hazard|spill|permit)\b", re.I),
     "Regulatory compliance"),
    (re.compile(r"\b(count|verify|inspect|qc|torque|measure)\b", re.I),
     "Critical thinking"),
    (re.compile(r"\b(rush|deadline|targets?|production|pace)\b", re.I),
     "Time management"),
    (re.compile(r"\b(team|crew|assist|support|communicat)\b", re.I),
     "Teamwork & collaboration"),
    (re.compile(r"\b(climb|lift|carry|physical|stamina)\b", re.I),
     "Physical stamina & dexterity"),
]


def skills_from_bullets(bullets: List[str]) -> List[str]:
    hits = set()
    for b in bullets:
        for rx, skill in BULLET_SKILL_HINTS:
            if rx.search(b):
                hits.add(skill)
    return [s for s in SKILL_CANON if s in hits]


# ─────────────────────────────────────────────────────────
# Header / education parsing (raw resume text)
# ─────────────────────────────────────────────────────────
def _likely_name(lines: List[str]) -> str:
    best = ""
    best_score = -1.0
    for i, l in enumerate(lines[:20]):
        s = l.strip()
        if not s:
            continue
        if EMAIL_RE.search(s) or PHONE_RE.search(s):
            continue
        if SECTION_HEADERS.match(s):
            continue
        if re.search(r"(objective|summary|skills|experience|education|cert|resume|cv|curriculum)", s, re.I):
            continue
        words = [w for w in re.split(r"\s+", s) if w]
        if not (2 <= len(words) <= 4):
            continue
        if any(re.search(r"\d", w) for w in words):
            continue
        skip = {"address", "phone", "email", "street", "avenue", "road", "city", "state", "zip"}
        if any(w.lower() in skip for w in words):
            continue
        caps = sum(1 for w in words if w[:1].isalpha() and w[:1].isupper())
        score = caps / len(words) + (20 - i) * 0.01
        if score > best_score:
            best_score = score
            best = s
    return best


def parse_header(text: str) -> Dict[str, str]:
    m = EMAIL_RE.search(text or "")
    email = m.group(0) if m else ""
    m = PHONE_RE.search(text or "")
    phone = m.group(0) if m else ""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    city = state = ""
    m2 = CITY_STATE_RE.search("\n".join(lines[:30]))
    if m2:
        city, state = m2.group(1), m2.group(2).upper()
    return {
        "name": cap_first(_likely_name(lines)),
        "email": clean_email(email),
        "phone": clean_phone(phone),
        "city": cap_first(city),
        "state": (state or "").strip(),
    }


def parse_education(text: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    edu_keywords = r"(high school|ged|college|university|program|certificate|diploma|academy|institute|school of)"
    i = 0
    while i < len(lines) and len(out) < MAX_SCHOOLS:
        l = lines[i]
        if re.search(edu_keywords, l, re.I):
            school = cap_first(l)
            cred = year = details = ""
            for la in lines[i + 1:i + 7]:
                if not year and re.search(r"\b(20\d{2}|19\d{2})\b", la):
                    year = la.strip()
                mcs = CITY_STATE_RE.search(la)
                if mcs and not details:
                    details = f"{mcs.group(1)}, {mcs.group(2).upper()}"
                if not cred and any(
                    x in la.lower()
                    for x in ["diploma", "degree", "certificate", "ged", "program",
                              "apprentice", "associate", "bachelor", "master"]
                ):
                    cred = cap_first(la.strip())
            out.append({"school": school, "credential": cred, "year": year, "details": details})
        i += 1
    return out[:MAX_SCHOOLS]


# ─────────────────────────────────────────────────────────
# Objectives
# ─────────────────────────────────────────────────────────
def objective_starters(trade: str, mode: str = "apprenticeship") -> List[str]:
    """Instructor-vetted starters for a trade; generic fallbacks otherwise."""
    mode = "job" if (mode or "").lower().startswith("j") else "apprenticeship"
    bank = OBJECTIVE_STARTERS.get(trade)
    if bank is None:
        low = norm_ws(trade).lower()
        for name, modes in OBJECTIVE_STARTERS.items():
            if low and (low in name.lower() or name.lower() in low):
                bank = modes
                break
    if bank and bank.get(mode):
        return bank[mode]
    if mode == "apprenticeship":
        return [
            f"Seeking entry into a {trade} apprenticeship; ready to show up safe, learn fast, and support the crew.",
            f"Aiming for {trade} apprenticeship placement—reliable, safety-forward, and coachable with strong work pace.",
            f"Applying to {trade} apprenticeship; committed to tool proficiency, print reading basics, and productive teamwork.",
        ]
    return [
        f"Seeking hands-on work in {trade}; dependable, safety-aware, and ready to contribute on Day 1.",
        f"Looking for entry-level {trade} work—strong pace, clean work areas, and consistent follow-through.",
        f"Pursuing {trade} work; show up, work safe, take direction, and help the crew hit targets.",
    ]


# ─────────────────────────────────────────────────────────
# Resume assembly
# ─────────────────────────────────────────────────────────
@dataclass
class JobEntry:
    company: str = ""
    role: str = ""
    city: str = ""
    start: str = ""
    end: str = ""
    bullets: List[str] = field(default_factory=list)


def build_resume_context(
    name: str,
    email: str,
    phone: str,
    city: str = "",
    state: str = "",
    objective: str = "",
    skills: Optional[List[str]] = None,
    certifications: Optional[List[str]] = None,
    jobs: Optional[List[Dict[str, Any]]] = None,
    schools: Optional[List[Dict[str, str]]] = None,
    trade: str = "",
) -> Dict[str, Any]:
    """Assemble a cleaned, capped, union-neutral resume context dict.

    Bullets are normalized to ≤24 words, skills are normalized against the
    canon and deduped, and everything respects the one-page limits.
    """
    summary = strip_banned(norm_ws(objective))[:MAX_SUMMARY_CHARS]

    seen = set()
    out_skills: List[str] = []
    for s in (skills or []):
        lab = normalize_skill_label(norm_ws(s))
        if lab and lab.lower() not in seen:
            seen.add(lab.lower())
            out_skills.append(lab)
    out_skills = out_skills[:MAX_SKILLS]

    certs = [norm_ws(c) for c in (certifications or []) if norm_ws(c)][:MAX_CERTS]

    out_jobs: List[Dict[str, Any]] = []
    for j in (jobs or [])[:MAX_JOBS]:
        start, end = parse_dates(j.get("dates", "")) if j.get("dates") else (
            norm_ws(j.get("start", "")), norm_ws(j.get("end", "")))
        bullets = [clean_bullet(b) for b in (j.get("bullets") or []) if str(b).strip()]
        entry = JobEntry(
            company=cap_first(j.get("company", "")),
            role=cap_first(j.get("title", "") or j.get("role", "")),
            city=cap_first(j.get("city", "")),
            start=start,
            end=end,
            bullets=bullets[:MAX_BULLETS_PER_JOB],
        )
        if any([entry.company, entry.role, entry.bullets]):
            out_jobs.append(asdict(entry))

    out_schools = []
    for s in (schools or [])[:MAX_SCHOOLS]:
        school = {
            "school": cap_first(s.get("school", "")),
            "credential": cap_first(s.get("credential", "")),
            "year": norm_ws(s.get("year", "")),
            "details": cap_first(s.get("details", "")),
        }
        if any(school.values()):
            out_schools.append(school)

    return {
        "Name": cap_first(name),
        "City": cap_first(city),
        "State": (state or "").strip().upper(),
        "phone": clean_phone(phone),
        "email": clean_email(email),
        "summary": summary,
        "skills": out_skills,
        "skills_by_category": categorize_skills(out_skills),
        "certs": certs,
        "jobs": out_jobs,
        "schools": out_schools,
        "trade_label": norm_ws(trade),
    }


def analyze_resume_text(text: str) -> Dict[str, Any]:
    """One-shot intake: parse raw resume text into structured suggestions."""
    detected_roles = detect_roles_from_text(text)
    suggested_bullets = {r: bullets_for_role(r) for r in detected_roles}
    suggested_bullets = {r: b for r, b in suggested_bullets.items() if b}
    return {
        "header": parse_header(text),
        "education": parse_education(text),
        "certifications": parse_certs(text),
        "detected_roles": detected_roles,
        "suggested_bullets": suggested_bullets,
        "suggested_skills": suggest_transferable_skills_from_text(text),
    }
