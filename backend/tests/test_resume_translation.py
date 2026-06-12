"""Tests for the rule-based resume translation engine and resume API."""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from ai import resume_translation as rt  # noqa: E402

SAMPLE_RESUME = """
Jordan Smith
Seattle, WA
jordan.smith@example.com
(206) 555-1234

OBJECTIVE
Hard worker looking for a new opportunity.

EXPERIENCE
Line Cook - Dick's Drive-In
2021 - 2023
Responsible for: prepping food and cleaning the kitchen under deadline pressure

Warehouse Associate - NW Distribution
2019 to 2021
Loaded pallets with a forklift and verified inventory counts

EDUCATION
Rainier Beach High School
Diploma 2018
Seattle, WA

CERTIFICATIONS
OSHA 10, Forklift certified, First Aid
"""


def test_data_loaded():
    assert len(rt.TRADES) >= 25
    assert "transferable" in rt.SKILLS_CANON
    assert len(rt.ROLE_BULLETS) >= 20


def test_clean_bullet_strips_filler_and_caps_words():
    long = "responsible for: " + "word " * 30
    out = rt.clean_bullet(long)
    assert not out.lower().startswith("responsible")
    assert len(out.split()) <= 24


def test_strip_banned_removes_union_language():
    assert "ibew" not in rt.strip_banned("IBEW Local 46 member").lower()
    assert "local" not in rt.strip_banned("Local 242 applicant").lower()


def test_clean_phone_formats_us_numbers():
    assert rt.clean_phone("12065551234") == "(206) 555-1234"
    assert rt.clean_phone("206.555.1234") == "(206) 555-1234"


def test_parse_header():
    h = rt.parse_header(SAMPLE_RESUME)
    assert h["name"] == "Jordan Smith"
    assert h["email"] == "jordan.smith@example.com"
    assert h["phone"] == "(206) 555-1234"
    assert h["state"] == "WA"


def test_parse_certs_normalizes():
    certs = rt.parse_certs(SAMPLE_RESUME)
    assert "OSHA Outreach 10-Hour (Construction)" in certs
    assert "Forklift — employer evaluation on hire" in certs
    assert "First Aid" in certs


def test_detect_roles_and_bullets():
    roles = rt.detect_roles_from_text(SAMPLE_RESUME)
    assert "Line Cook" in roles
    assert "Warehouse Associate" in roles
    assert rt.bullets_for_role("Line Cook")


def test_objective_starters_vetted_and_fallback():
    vetted = rt.objective_starters("Boilermaker", "apprenticeship")
    assert len(vetted) >= 3
    fallback = rt.objective_starters("Underwater Basket Weaver", "job")
    assert any("Underwater Basket Weaver" in s for s in fallback)


def test_skills_inference_and_categorization():
    skills = rt.skills_from_bullets(["Loaded pallets with forklift", "Worked with crew under deadlines"])
    assert "Materials handling (wood/concrete/metal)" in skills
    cats = rt.categorize_skills(["teamwork", "forklift", "stamina", "teamwork"])
    assert "Teamwork & collaboration" in cats["Transferable"]
    assert "Operating machinery" in cats["Job-Specific"]
    assert "Physical stamina & dexterity" in cats["Self-Management"]


def test_build_resume_context_caps_and_cleans():
    ctx = rt.build_resume_context(
        name="jordan smith",
        email="Jordan.Smith@Example.com",
        phone="2065551234",
        city="seattle",
        state="wa",
        objective="Seeking IBEW Local 46 apprenticeship " + "x" * 500,
        skills=["teamwork", "Teamwork", "forklift"] + [f"skill{i}" for i in range(15)],
        certifications=["OSHA 10"] * 10,
        jobs=[{"title": "line cook", "company": "dick's drive-in",
               "dates": "2021 - 2023", "bullets": ["responsible for: cleaning"] * 6}] * 5,
        schools=[{"school": "rainier beach high school", "credential": "diploma", "year": "2018"}] * 4,
        trade="Electrician – Inside (01)",
    )
    assert ctx["Name"] == "Jordan smith"
    assert ctx["email"] == "jordan.smith@example.com"
    assert ctx["phone"] == "(206) 555-1234"
    assert ctx["State"] == "WA"
    assert "ibew" not in ctx["summary"].lower()
    assert len(ctx["summary"]) <= rt.MAX_SUMMARY_CHARS
    assert len(ctx["skills"]) <= rt.MAX_SKILLS
    assert len(ctx["certs"]) <= rt.MAX_CERTS
    assert len(ctx["jobs"]) <= rt.MAX_JOBS
    assert all(len(j["bullets"]) <= rt.MAX_BULLETS_PER_JOB for j in ctx["jobs"])
    assert len(ctx["schools"]) <= rt.MAX_SCHOOLS


def test_analyze_resume_text_end_to_end():
    result = rt.analyze_resume_text(SAMPLE_RESUME)
    assert result["header"]["name"] == "Jordan Smith"
    assert result["detected_roles"]
    assert result["suggested_bullets"]
    assert result["certifications"]
    assert result["suggested_skills"]
