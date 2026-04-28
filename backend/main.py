#!/usr/bin/env python3
"""
TradeG8 Backend API
Built by Mandy Richardson & Claude (Anthropic)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth, jobs, resumes

app = FastAPI(
    title="TradeG8 API",
    description="AI-powered job search for construction trades",
    version="1.0.0",
)

# Configure CORS. Keep this permissive for the scaffold; tighten it when auth
# and deployment settings are wired into the full backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "TradeG8 API - AI for the people",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
