"""
TradeG8 Backend - Main FastAPI Application
Built by Mandy Richardson & Claude (Anthropic)
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn

from api import jobs, resumes, auth, users, case_manager, partnerships
from database.supabase_client import supabase_client
from utils.config import settings

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 TradeG8 Backend Starting...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔐 Auth enabled: {settings.SUPABASE_URL is not None}")
    yield
    # Shutdown
    print("👋 TradeG8 Backend Shutting Down...")

# Initialize FastAPI app
app = FastAPI(
    title="TradeG8 API",
    description="AI-Powered Job Search & Career Navigation for Construction Trades",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "name": "TradeG8 API",
        "version": "1.0.0",
        "status": "operational",
        "message": "AI for the people. 🔥"
    }

@app.get("/health")
async def health_check():
    """Health check with detailed deployment status"""
    return {
        "status": "healthy",
        "database": "connected" if supabase_client else "not_configured",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "features": {
            "job_scraping": True,
            "resume_ai": getattr(settings, "HUGGINGFACE_API_KEY", None) is not None,
            "database": getattr(settings, "SUPABASE_URL", None) is not None,
        },
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Job Search"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resume Generation"])
app.include_router(case_manager.router, prefix="/api/case-manager", tags=["Case Manager"])
app.include_router(partnerships.router, prefix="/api/partnerships", tags=["Partnerships"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
