"""Tests for the contractor pages and trade-community endpoints."""

import sys
import uuid
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from fastapi.testclient import TestClient

from database.client import require_db
from main import app
from tests.test_api_db import FakeDB


@pytest.fixture
def client():
    fake = FakeDB()
    for t in ("companies", "communities", "community_channels",
              "community_members", "posts", "comments"):
        fake.store.setdefault(t, [])
    app.dependency_overrides[require_db] = lambda: fake
    yield TestClient(app), fake
    app.dependency_overrides.clear()


def test_contractor_page_and_direct_posting(client):
    c, fake = client
    owner = str(uuid.uuid4())

    # Contractor creates a "learn about us" page
    r = c.post("/api/contractors/", json={
        "name": "ABC Electric", "owner_id": owner,
        "about": "Family shop, 12 electricians, we train our helpers.",
        "trades": ["Electrician – Inside (01)"], "hiring": True,
        "profile": {"pay_range": "$22-28/hr", "hours_count": True},
    })
    assert r.status_code == 200
    company_id = r.json()["contractor"]["id"]

    # Page is browsable; hiring filter works
    assert len(c.get("/api/contractors/", params={"hiring_only": True}).json()["contractors"]) == 1

    # Direct job posting starts UNVERIFIED — no pay-to-skip-vetting
    r = c.post("/api/contractors/jobs", json={
        "company_id": company_id, "posted_by": owner,
        "title": "Electrician Helper", "pay": "$24/hr", "location": "Seattle, WA",
    })
    posting = r.json()["posting"]
    assert posting["is_direct_posting"] is True
    assert posting["score"] == 0
    assert posting["recommendation"] == "Pending verification"

    # Posting shows on the contractor's page
    page = c.get(f"/api/contractors/{company_id}").json()
    assert len(page["postings"]) == 1

    # Updating the page upserts rather than duplicating
    c.post("/api/contractors/", json={"name": "ABC Electric", "owner_id": owner, "hiring": False})
    assert len(c.get("/api/contractors/").json()["contractors"]) == 1


def test_community_flow(client):
    c, fake = client
    # Seed one trade community + channel (mirrors the Supabase seed migration)
    community_id, channel_id = str(uuid.uuid4()), str(uuid.uuid4())
    fake.store["communities"].append(
        {"id": community_id, "trade": "Electrician – Inside (01)",
         "name": "Electrician – Inside (01)"})
    fake.store["community_channels"].append(
        {"id": channel_id, "community_id": community_id, "name": "Mentorship"})

    student, mentor = str(uuid.uuid4()), str(uuid.uuid4())

    assert len(c.get("/api/community/").json()["communities"]) == 1
    assert len(c.get(f"/api/community/{community_id}/channels").json()["channels"]) == 1

    # Join as member and as mentor
    c.post(f"/api/community/{community_id}/join", json={"user_id": student})
    c.post(f"/api/community/{community_id}/join",
           json={"user_id": mentor, "member_role": "mentor"})
    mentors = c.get(f"/api/community/{community_id}/mentors").json()["mentors"]
    assert len(mentors) == 1 and mentors[0]["user_id"] == mentor

    # Student asks; mentor answers — in the open
    r = c.post("/api/community/posts", json={
        "channel_id": channel_id, "author_id": student,
        "title": "PSEJATC says 8000 OJT hours — does my warehouse job count?",
        "body": "I have a year at UPS. Anything I can do with that?"})
    post_id = r.json()["post"]["id"]
    c.post(f"/api/community/posts/{post_id}/comments", json={
        "author_id": mentor,
        "body": "Warehouse hours don't count toward OJT, but forklift + materials handling go straight on your resume. Get your trainee card first."})

    posts = c.get(f"/api/community/channels/{channel_id}/posts").json()["posts"]
    assert len(posts) == 1
    comments = c.get(f"/api/community/posts/{post_id}/comments").json()["comments"]
    assert len(comments) == 1

    # Guardrails
    assert c.post(f"/api/community/{community_id}/join",
                  json={"user_id": student, "member_role": "boss"}).status_code == 422
    assert c.post("/api/community/posts", json={
        "channel_id": channel_id, "author_id": student, "title": "  "}).status_code == 422
