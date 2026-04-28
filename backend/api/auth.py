"""
Authentication API Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(request: SignupRequest):
    """Create new user account"""
    return {
        "message": "Signup endpoint - will create user in Supabase",
        "email": request.email,
    }


@router.post("/login")
async def login(request: LoginRequest):
    """Login user"""
    return {
        "message": "Login endpoint - will verify credentials",
        "token": "fake-jwt-token",
    }


@router.post("/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out"}
