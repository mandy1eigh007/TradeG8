"""
Authentication API Endpoints

Backed by Supabase Auth. Profiles can also be created by a navigator on a
student's behalf (shared devices, no personal email access is common) —
see api/profiles.py.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from database.client import require_db

router = APIRouter()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(request: SignupRequest, db=Depends(require_db)):
    """Create a new user account via Supabase Auth."""
    try:
        result = db.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                "options": {"data": {"full_name": request.full_name}},
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"signup failed: {e}")
    user = getattr(result, "user", None)
    return {
        "status": "ok",
        "user_id": getattr(user, "id", None),
        "email": request.email,
        "message": "Account created. Complete your profile at /api/profiles.",
    }


@router.post("/login")
async def login(request: LoginRequest, db=Depends(require_db)):
    """Login and receive a session token."""
    try:
        result = db.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"login failed: {e}")
    session = getattr(result, "session", None)
    user = getattr(result, "user", None)
    return {
        "status": "ok",
        "user_id": getattr(user, "id", None),
        "access_token": getattr(session, "access_token", None),
        "refresh_token": getattr(session, "refresh_token", None),
    }


@router.post("/logout")
async def logout(db=Depends(require_db)):
    """Logout the current session."""
    try:
        db.auth.sign_out()
    except Exception:
        pass
    return {"status": "ok", "message": "Logged out"}
