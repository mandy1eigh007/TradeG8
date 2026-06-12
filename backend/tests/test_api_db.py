"""Tests for profile, job board, and application-tracking endpoints.

Uses a minimal in-memory fake of the Supabase client so the full
profile -> search -> apply -> activity-log flow is verified without
live credentials.
"""

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


class FakeResult:
    def __init__(self, data):
        self.data = data


class FakeQuery:
    def __init__(self, store, name):
        self.store, self.name = store, name
        self.filters, self.desc_order, self.limit_n = [], None, None
        self._pending = None

    # write ops
    def insert(self, rows):
        rows = rows if isinstance(rows, list) else [rows]
        for r in rows:
            r.setdefault("id", str(uuid.uuid4()))
            self.store[self.name].append(dict(r))
        self._pending = rows
        return self

    def upsert(self, row, on_conflict=None):
        keys = (on_conflict or "id").split(",")
        rows = self.store[self.name]
        for existing in rows:
            if all(existing.get(k) == row.get(k) for k in keys):
                existing.update(row)
                self._pending = [existing]
                return self
        row = dict(row)
        row.setdefault("id", str(uuid.uuid4()))
        rows.append(row)
        self._pending = [row]
        return self

    def update(self, patch):
        self._patch = patch
        self._pending = "update"
        return self

    # read ops / filters
    def select(self, *_args):
        return self

    def eq(self, col, val):
        self.filters.append(lambda r: r.get(col) == val)
        return self

    def gte(self, col, val):
        self.filters.append(lambda r: (r.get(col) or 0) >= val)
        return self

    def ilike(self, col, pattern):
        needle = pattern.strip("%").lower()
        self.filters.append(lambda r: needle in str(r.get(col, "")).lower())
        return self

    def or_(self, expr):
        clauses = []
        for part in expr.split(","):
            col, _op, pat = part.split(".", 2)
            needle = pat.strip("%").lower()
            clauses.append((col, needle))
        self.filters.append(
            lambda r: any(n in str(r.get(c, "")).lower() for c, n in clauses)
        )
        return self

    def order(self, col, desc=False):
        self.desc_order = (col, desc)
        return self

    def limit(self, n):
        self.limit_n = n
        return self

    def execute(self):
        if self._pending == "update":
            hits = [r for r in self.store[self.name]
                    if all(f(r) for f in self.filters)]
            for r in hits:
                r.update(self._patch)
            return FakeResult([dict(r) for r in hits])
        if self._pending is not None:
            return FakeResult([dict(r) for r in self._pending])
        rows = [r for r in self.store[self.name] if all(f(r) for f in self.filters)]
        if self.desc_order:
            col, desc = self.desc_order
            rows.sort(key=lambda r: str(r.get(col) or ""), reverse=desc)
        if self.limit_n:
            rows = rows[: self.limit_n]
        return FakeResult([dict(r) for r in rows])


class FakeDB:
    def __init__(self):
        self.store = {"users": [], "jobs": [], "saved_jobs": [], "activity_logs": []}

    def table(self, name):
        return FakeQuery(self.store, name)


@pytest.fixture
def client():
    fake = FakeDB()
    app.dependency_overrides[require_db] = lambda: fake
    import api.jobs as jobs_module
    original = jobs_module.get_supabase
    jobs_module.get_supabase = lambda: fake
    yield TestClient(app), fake
    app.dependency_overrides.clear()
    jobs_module.get_supabase = original


def test_db_unconfigured_returns_503():
    c = TestClient(app)
    assert c.post("/api/applications/", json={"user_id": "u", "job_id": "j"}).status_code == 503
    assert c.get("/api/profiles/abc").status_code == 503


def test_full_student_flow(client):
    c, fake = client
    uid = str(uuid.uuid4())

    # 1. Create the apply-once profile
    r = c.post("/api/profiles/", json={
        "user_id": uid, "email": "student@example.com",
        "first_name": "Jordan", "last_name": "Smith", "phone": "2065551234",
        "profile": {"target_trade": "Electrician – Inside (01)",
                    "certifications": ["OSHA Outreach 10-Hour (Construction)"]},
    })
    assert r.status_code == 200
    assert c.get(f"/api/profiles/{uid}").json()["first_name"] == "Jordan"

    # 2. Import vetted scraper results into the job board
    r = c.post("/api/jobs/import", json=[
        {"title": "Electrician Helper", "company": "ABC Electric",
         "location": "Seattle, WA", "score": 90, "lni_registered": True,
         "hours_count_toward_trainee": True, "recommendation": "EXCELLENT"},
        {"title": "Laborer", "company": "Sketchy Co", "location": "Seattle, WA",
         "score": 20, "recommendation": "AVOID"},
    ])
    assert r.json()["imported"] == 2

    # 3. Search filters out the low-scoring posting
    r = c.get("/api/jobs/search", params={"query": "electrician", "min_score": 60})
    jobs = r.json()["jobs"]
    assert len(jobs) == 1 and jobs[0]["company"] == "ABC Electric"
    job_id = jobs[0]["id"]

    # 4. One-tap apply
    r = c.post("/api/applications/", json={"user_id": uid, "job_id": job_id})
    assert r.json()["application"]["status"] == "applied"

    # 5. Tracker shows it; activity log captured it automatically
    apps = c.get("/api/applications/", params={"user_id": uid}).json()["applications"]
    assert len(apps) == 1
    activity = c.get("/api/applications/activity", params={"user_id": uid}).json()["activity"]
    assert activity and activity[0]["activity_type"] == "job_application"

    # 6. Status update after an interview
    r = c.patch(f"/api/applications/{job_id}",
                json={"user_id": uid, "status": "interview"})
    assert r.json()["application"]["status"] == "interview"


def test_invalid_status_rejected(client):
    c, _ = client
    r = c.post("/api/applications/", json={"user_id": "u", "job_id": "j", "status": "ghosted"})
    assert r.status_code == 422


def test_job_detail_404(client):
    c, _ = client
    assert c.get("/api/jobs/nonexistent").status_code == 404
