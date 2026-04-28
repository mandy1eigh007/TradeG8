"""
Resume Generation API Endpoints
"""

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class JobHistory(BaseModel):
    title: str
    company: str
    duration: str
    responsibilities: List[str]


class ResumeRequest(BaseModel):
    name: str
    email: str
    phone: str
    target_trade: str
    job_history: List[JobHistory]


@router.post("/generate")
async def generate_resume(request: ResumeRequest):
    """
    Generate construction-language resume.

    Eventually this will translate job history into trade-specific construction
    language and export PDF/DOCX files.
    """
    return {
        "message": "Resume generation coming soon",
        "target_trade": request.target_trade,
        "status": "pending",
    }


@router.get("/")
async def list_resumes(user_id: str):
    """List all resumes for a user"""
    return {
        "user_id": user_id,
        "resumes": [],
        "message": "Resume listing endpoint",
    }
