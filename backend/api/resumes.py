"""
Resume Generation API Endpoints

Backed by the rule-based translation engine in ai/resume_translation.py,
ported from the resume-workshop-app build-out. No AI API key required.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ai import resume_translation as rt

router = APIRouter()


class JobHistory(BaseModel):
    title: str = ""
    company: str = ""
    city: str = ""
    dates: str = ""
    bullets: List[str] = []


class SchoolEntry(BaseModel):
    school: str = ""
    credential: str = ""
    year: str = ""
    details: str = ""


class ResumeRequest(BaseModel):
    name: str
    email: str
    phone: str
    city: str = ""
    state: str = ""
    target_trade: str = ""
    objective: str = ""
    skills: List[str] = []
    certifications: List[str] = []
    job_history: List[JobHistory] = []
    education: List[SchoolEntry] = []


class ResumeTextRequest(BaseModel):
    text: str


@router.get("/trades")
async def list_trades():
    """All trades with instructor-vetted objective starters."""
    return {"trades": rt.TRADES, "count": len(rt.TRADES)}


@router.get("/skills")
async def list_skills():
    """The vetted skills canon, grouped by category."""
    return {"skills_canon": rt.SKILLS_CANON}


@router.get("/objectives")
async def get_objectives(
    trade: str = Query(..., description="Target trade, e.g. 'Electrician – Inside (01)'"),
    mode: str = Query("apprenticeship", description="'apprenticeship' or 'job'"),
):
    """Instructor-vetted objective starters for a trade."""
    starters = rt.objective_starters(trade, mode)
    return {"trade": trade, "mode": mode, "starters": starters}


@router.get("/roles")
async def list_roles():
    """Prior-work roles that have vetted construction-ready bullet banks."""
    return {"roles": sorted(rt.ROLE_BULLETS.keys())}


@router.get("/role-bullets")
async def get_role_bullets(
    role: str = Query(..., description="Prior role, e.g. 'Line Cook'"),
):
    """Measured, evidence-ready duty bullets for a prior role."""
    bullets = rt.bullets_for_role(role)
    if not bullets:
        raise HTTPException(status_code=404, detail=f"No bullet bank for role '{role}'")
    return {
        "role": role,
        "bullets": bullets,
        "inferred_skills": rt.skills_from_bullets(bullets),
    }


@router.post("/parse")
async def parse_resume_text(request: ResumeTextRequest):
    """
    Parse raw resume text (pasted or extracted from PDF/DOCX) into structured
    suggestions: header, education, certifications, detected roles with
    bullet suggestions, and inferred transferable skills.
    """
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="text is empty")
    return rt.analyze_resume_text(request.text)


@router.post("/generate")
async def generate_resume(request: ResumeRequest):
    """
    Build a construction-ready resume context: union-neutral language,
    normalized skills, ≤24-word bullets, one-page caps. If no objective is
    supplied, vetted starters for the target trade are suggested.
    """
    context = rt.build_resume_context(
        name=request.name,
        email=request.email,
        phone=request.phone,
        city=request.city,
        state=request.state,
        objective=request.objective,
        skills=request.skills,
        certifications=request.certifications,
        jobs=[j.model_dump() for j in request.job_history],
        schools=[s.model_dump() for s in request.education],
        trade=request.target_trade,
    )
    response: Dict[str, Any] = {"status": "ok", "resume": context}
    if not request.objective and request.target_trade:
        response["objective_suggestions"] = rt.objective_starters(
            request.target_trade, "apprenticeship"
        )
    return response


@router.get("/")
async def list_resumes(user_id: str):
    """List all resumes for a user (Supabase wiring pending)"""
    return {
        "user_id": user_id,
        "resumes": [],
        "message": "Resume persistence coming with Supabase integration",
    }
