"""
Supabase client for the TradeG8 backend.

Configured via environment variables (see backend/.env.example):
  SUPABASE_URL          https://<project>.supabase.co
  SUPABASE_SERVICE_KEY  service-role key (backend only — never ship to clients)

Endpoints that need the database use the `require_db` dependency, which
returns a clear 503 when the backend isn't configured yet, so the API
stays usable (and testable) without credentials.
"""

import os

from fastapi import HTTPException

try:
    from supabase import create_client
except ImportError:  # supabase-py not installed in this environment
    create_client = None

_client = None


def get_supabase():
    """Return a cached Supabase client, or None when unconfigured."""
    global _client
    if _client is not None:
        return _client
    url = os.getenv("SUPABASE_URL", "").strip()
    key = (os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY") or "").strip()
    if not url or not key or create_client is None:
        return None
    _client = create_client(url, key)
    return _client


def require_db():
    """FastAPI dependency: the Supabase client or a 503 explaining why not."""
    db = get_supabase()
    if db is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Database not configured. Set SUPABASE_URL and "
                "SUPABASE_SERVICE_KEY (see backend/.env.example)."
            ),
        )
    return db
