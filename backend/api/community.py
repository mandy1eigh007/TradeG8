"""
Community API Endpoints

Pillar 3: Reddit-style communities, one per trade. Channels inside each
community (General, Mentorship, Applications & Ranking, Hold-Over Jobs).
Mentors are flagged members — mentorship happens in the open where every
answer helps the whole community, because nobody in construction has time
for one-on-one mentoring.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database.client import require_db

router = APIRouter()


class JoinRequest(BaseModel):
    user_id: str
    member_role: str = "member"


class PostRequest(BaseModel):
    channel_id: str
    author_id: str
    title: str
    body: str = ""


class CommentRequest(BaseModel):
    author_id: str
    body: str


@router.get("/")
async def list_communities(db=Depends(require_db)):
    """All trade communities."""
    result = db.table("communities").select("*").order("trade").execute()
    return {"communities": result.data or []}


@router.get("/{community_id}/channels")
async def list_channels(community_id: str, db=Depends(require_db)):
    """Channels in a trade community."""
    result = (
        db.table("community_channels")
        .select("*")
        .eq("community_id", community_id)
        .execute()
    )
    return {"community_id": community_id, "channels": result.data or []}


@router.post("/{community_id}/join")
async def join_community(community_id: str, request: JoinRequest, db=Depends(require_db)):
    """Join a trade community (as member, mentor, or moderator)."""
    if request.member_role not in ("member", "mentor", "moderator"):
        raise HTTPException(status_code=422, detail="invalid member_role")
    result = (
        db.table("community_members")
        .upsert(
            {
                "community_id": community_id,
                "user_id": request.user_id,
                "member_role": request.member_role,
            },
            on_conflict="community_id,user_id",
        )
        .execute()
    )
    return {"status": "ok", "membership": result.data[0] if result.data else None}


@router.get("/{community_id}/mentors")
async def list_mentors(community_id: str, db=Depends(require_db)):
    """The mentors of a trade community."""
    result = (
        db.table("community_members")
        .select("*, users(first_name, last_name, role)")
        .eq("community_id", community_id)
        .eq("member_role", "mentor")
        .execute()
    )
    return {"community_id": community_id, "mentors": result.data or []}


@router.get("/channels/{channel_id}/posts")
async def list_posts(channel_id: str, db=Depends(require_db)):
    """Posts in a channel, pinned first, newest first."""
    result = (
        db.table("posts")
        .select("*")
        .eq("channel_id", channel_id)
        .order("pinned", desc=True)
        .order("created_at", desc=True)
        .execute()
    )
    return {"channel_id": channel_id, "posts": result.data or []}


@router.post("/posts")
async def create_post(request: PostRequest, db=Depends(require_db)):
    """Start a thread in a channel."""
    if not request.title.strip():
        raise HTTPException(status_code=422, detail="title required")
    result = (
        db.table("posts")
        .insert(
            {
                "channel_id": request.channel_id,
                "author_id": request.author_id,
                "title": request.title.strip(),
                "body": request.body,
            }
        )
        .execute()
    )
    return {"status": "ok", "post": result.data[0] if result.data else None}


@router.get("/posts/{post_id}/comments")
async def list_comments(post_id: str, db=Depends(require_db)):
    """Comments on a post, oldest first."""
    result = (
        db.table("comments")
        .select("*")
        .eq("post_id", post_id)
        .order("created_at")
        .execute()
    )
    return {"post_id": post_id, "comments": result.data or []}


@router.post("/posts/{post_id}/comments")
async def add_comment(post_id: str, request: CommentRequest, db=Depends(require_db)):
    """Reply to a post."""
    if not request.body.strip():
        raise HTTPException(status_code=422, detail="comment body required")
    result = (
        db.table("comments")
        .insert(
            {
                "post_id": post_id,
                "author_id": request.author_id,
                "body": request.body.strip(),
            }
        )
        .execute()
    )
    return {"status": "ok", "comment": result.data[0] if result.data else None}
