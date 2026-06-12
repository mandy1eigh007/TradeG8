"""
Application Tracking API Endpoints

One tap to apply/save a job; every action is logged automatically to
activity_logs. The same log doubles as compliance evidence (BFET /
unemployment / DOC) — students should never have to reconstruct their
job-search history by hand.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database.client import require_db

router = APIRouter()

VALID_STATUSES = ("saved", "applied", "interview", "offer", "rejected")


class ApplicationRequest(BaseModel):
    user_id: str
    job_id: str
    status: str = "applied"
    notes: str = ""


class StatusUpdate(BaseModel):
    user_id: str
    status: str
    notes: Optional[str] = None


def _log_activity(db, user_id: str, activity_type: str, details: dict):
    db.table("activity_logs").insert(
        {"user_id": user_id, "activity_type": activity_type, "details": details}
    ).execute()


@router.post("/")
async def track_application(request: ApplicationRequest, db=Depends(require_db)):
    """Save or apply to a job. Auto-logs the activity for compliance."""
    if request.status not in VALID_STATUSES:
        raise HTTPException(status_code=422, detail=f"status must be one of {VALID_STATUSES}")
    row = {
        "user_id": request.user_id,
        "job_id": request.job_id,
        "status": request.status,
        "notes": request.notes,
    }
    if request.status == "applied":
        row["applied_date"] = datetime.now(timezone.utc).isoformat()
    result = (
        db.table("saved_jobs")
        .upsert(row, on_conflict="user_id,job_id")
        .execute()
    )
    _log_activity(
        db,
        request.user_id,
        "job_application" if request.status == "applied" else "job_saved",
        {"job_id": request.job_id, "status": request.status},
    )
    return {"status": "ok", "application": result.data[0] if result.data else row}


@router.get("/")
async def list_applications(user_id: str, db=Depends(require_db)):
    """A student's application tracker: jobs with statuses, newest first."""
    result = (
        db.table("saved_jobs")
        .select("*, jobs(*)")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return {"user_id": user_id, "applications": result.data or []}


@router.patch("/{job_id}")
async def update_status(job_id: str, request: StatusUpdate, db=Depends(require_db)):
    """Update an application's status (interviewed, offer, rejected...)."""
    if request.status not in VALID_STATUSES:
        raise HTTPException(status_code=422, detail=f"status must be one of {VALID_STATUSES}")
    patch = {"status": request.status}
    if request.notes is not None:
        patch["notes"] = request.notes
    if request.status == "applied":
        patch["applied_date"] = datetime.now(timezone.utc).isoformat()
    result = (
        db.table("saved_jobs")
        .update(patch)
        .eq("user_id", request.user_id)
        .eq("job_id", job_id)
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="application not found")
    _log_activity(db, request.user_id, "application_status_change",
                  {"job_id": job_id, "status": request.status})
    return {"status": "ok", "application": result.data[0]}


@router.get("/activity")
async def activity_log(user_id: str, db=Depends(require_db)):
    """Raw activity log — the compliance evidence trail."""
    result = (
        db.table("activity_logs")
        .select("*")
        .eq("user_id", user_id)
        .order("timestamp", desc=True)
        .execute()
    )
    return {"user_id": user_id, "activity": result.data or []}
