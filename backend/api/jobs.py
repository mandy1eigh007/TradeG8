"""
Job Search API Endpoints
"""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/search")
async def search_jobs(
    query: str = Query(..., description="Job search query"),
    location: str = Query("Seattle, WA", description="Job location"),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Search for construction jobs.

    This endpoint will eventually scrape job boards, verify contractors with
    L&I, check reputation signals, and score jobs for student safety.
    """
    return {
        "query": query,
        "location": location,
        "limit": limit,
        "jobs": [],
        "message": "Job scraping coming soon - use scraper.py for now",
    }


@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get details for a specific job"""
    return {
        "job_id": job_id,
        "message": "Job details endpoint",
    }
