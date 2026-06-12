"""
Student Profile API Endpoints

The apply-once profile: students (or a navigator helping them) enter their
information one time — contact, target trade, certs, skills, work history,
availability, transportation. Every application and resume reuses it, because
nobody has time to retype their life story for every posting, and many
students share devices or have no device at all.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from database.client import require_db

router = APIRouter()


class ProfileRequest(BaseModel):
    user_id: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    role: str = "student"
    case_manager_id: Optional[str] = None
    # Apply-once data: target_trade, certifications, skills, work_history,
    # availability, transportation, education — free-form by design.
    profile: Dict[str, Any] = {}


@router.post("/")
async def upsert_profile(request: ProfileRequest, db=Depends(require_db)):
    """Create or update a student/navigator profile."""
    if request.role not in ("student", "case_manager", "admin"):
        raise HTTPException(status_code=422, detail="invalid role")
    row = {
        "id": request.user_id,
        "email": request.email,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "phone": request.phone,
        "role": request.role,
        "case_manager_id": request.case_manager_id,
        "profile": request.profile,
    }
    result = db.table("users").upsert(row).execute()
    return {"status": "ok", "profile": result.data[0] if result.data else row}


@router.get("/{user_id}")
async def get_profile(user_id: str, db=Depends(require_db)):
    """Fetch a profile by id."""
    result = db.table("users").select("*").eq("id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="profile not found")
    return result.data[0]


@router.get("/{user_id}/students")
async def list_students(user_id: str, db=Depends(require_db)):
    """List students assigned to a case manager/navigator."""
    result = (
        db.table("users").select("*").eq("case_manager_id", user_id).execute()
    )
    return {"case_manager_id": user_id, "students": result.data or []}
