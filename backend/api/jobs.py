"""
Job Search API Endpoints

The vetted job board. The scraper (scraper.py) finds jobs, verifies the
contractor with WA L&I, checks reputation, and scores 0-100; results are
imported here so students search ONE feed of pre-vetted, real jobs instead
of wading through fake and data-harvesting postings on the open internet.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from database.client import get_supabase, require_db

router = APIRouter()


class ScrapedJob(BaseModel):
    title: str
    company: str
    location: str = ""
    pay: str = ""
    url: str = ""
    source: str = ""
    description: str = ""
    lni_registered: bool = False
    lni_status: str = ""
    lni_licensed_electrical: bool = False
    lni_violations: int = 0
    lni_workers_comp: str = ""
    glassdoor_rating: Optional[float] = None
    glassdoor_review_count: Optional[int] = None
    glassdoor_summary: str = ""
    score: int = 0
    score_breakdown: str = ""
    hours_count_toward_trainee: bool = False
    recommendation: str = ""


@router.get("/search")
async def search_jobs(
    query: str = Query(..., description="Job search query"),
    location: str = Query("", description="Job location filter"),
    min_score: int = Query(0, ge=0, le=100, description="Minimum safety score"),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Search the vetted job board (highest safety score first).

    Falls back to a clear message when the database isn't configured.
    """
    db = get_supabase()
    if db is None:
        return {
            "query": query,
            "location": location,
            "jobs": [],
            "message": "Database not configured — run scraper.py directly for now",
        }
    q = (
        db.table("jobs")
        .select("*")
        .or_(f"title.ilike.%{query}%,company.ilike.%{query}%,description.ilike.%{query}%")
        .gte("score", min_score)
        .order("score", desc=True)
        .limit(limit)
    )
    if location:
        q = q.ilike("location", f"%{location}%")
    result = q.execute()
    return {
        "query": query,
        "location": location,
        "min_score": min_score,
        "count": len(result.data or []),
        "jobs": result.data or [],
    }


@router.post("/import")
async def import_jobs(jobs: List[ScrapedJob], db=Depends(require_db)):
    """Import scraped + vetted jobs into the board (used by scraper runs)."""
    rows = [j.model_dump() for j in jobs]
    if not rows:
        raise HTTPException(status_code=422, detail="no jobs provided")
    result = db.table("jobs").insert(rows).execute()
    return {"status": "ok", "imported": len(result.data or rows)}


@router.get("/{job_id}")
async def get_job(job_id: str, db=Depends(require_db)):
    """Get details for a specific vetted job."""
    result = db.table("jobs").select("*").eq("id", job_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="job not found")
    return result.data[0]
