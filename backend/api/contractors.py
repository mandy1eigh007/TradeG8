"""
Contractor API Endpoints

Pillar 2 of the platform: instead of students chasing contractors, contractors
pitch students. Contractors get a "learn about us" page, list their own jobs
(still L&I-vetted and scored — being on the platform never exempts anyone from
vetting), and browse opted-in applicants.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database.client import require_db

router = APIRouter()


class ContractorPageRequest(BaseModel):
    name: str
    owner_id: str
    about: str = ""
    trades: List[str] = []
    hiring: bool = False
    contact_email: str = ""
    contact_phone: str = ""
    # pay ranges, perks, whether hours count, crew size, photos…
    profile: Dict[str, Any] = {}


class DirectJobPosting(BaseModel):
    company_id: str
    posted_by: str
    title: str
    location: str = ""
    pay: str = ""
    description: str = ""
    url: str = ""


@router.get("/")
async def list_contractors(hiring_only: bool = False, db=Depends(require_db)):
    """Browse contractor pages (optionally only those actively hiring)."""
    q = db.table("companies").select("*")
    if hiring_only:
        q = q.eq("hiring", True)
    result = q.execute()
    return {"contractors": result.data or []}


@router.post("/")
async def upsert_contractor_page(request: ContractorPageRequest, db=Depends(require_db)):
    """Create or update a contractor's 'learn about us' page."""
    existing = (
        db.table("companies").select("id").eq("name", request.name).execute()
    )
    row = {
        "name": request.name,
        "owner_id": request.owner_id,
        "about": request.about,
        "trades": request.trades,
        "hiring": request.hiring,
        "contact_email": request.contact_email,
        "contact_phone": request.contact_phone,
        "profile": request.profile,
    }
    if existing.data:
        result = (
            db.table("companies").update(row).eq("id", existing.data[0]["id"]).execute()
        )
    else:
        result = db.table("companies").insert(row).execute()
    return {"status": "ok", "contractor": result.data[0] if result.data else row}


@router.get("/{company_id}")
async def get_contractor_page(company_id: str, db=Depends(require_db)):
    """A contractor's page plus their open direct postings."""
    company = db.table("companies").select("*").eq("id", company_id).execute()
    if not company.data:
        raise HTTPException(status_code=404, detail="contractor not found")
    jobs = (
        db.table("jobs").select("*").eq("company_id", company_id).execute()
    )
    return {"contractor": company.data[0], "postings": jobs.data or []}


@router.post("/jobs")
async def post_direct_job(request: DirectJobPosting, db=Depends(require_db)):
    """
    A contractor lists a job directly. The posting enters the same vetting
    pipeline as scraped jobs: the scraper's L&I verifier and scorer run on the
    company, so direct postings carry a safety score like everything else.
    """
    company = (
        db.table("companies").select("*").eq("id", request.company_id).execute()
    )
    if not company.data:
        raise HTTPException(status_code=404, detail="contractor page not found")
    c = company.data[0]
    row = {
        "title": request.title,
        "company": c["name"],
        "company_id": request.company_id,
        "posted_by": request.posted_by,
        "is_direct_posting": True,
        "location": request.location,
        "pay": request.pay,
        "description": request.description,
        "url": request.url,
        "source": "Direct posting",
        # Carries the company's verification state until the vetting pipeline
        # re-scores it; unverified contractors start at 0, not at trusted.
        "lni_registered": bool(c.get("lni_verified")),
        "score": 0,
        "recommendation": "Pending verification",
    }
    result = db.table("jobs").insert(row).execute()
    return {"status": "ok", "posting": result.data[0] if result.data else row}
