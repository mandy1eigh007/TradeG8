# TradeG8 API Documentation

## Base URL

```text
http://localhost:8000/api
```

## Authentication

Authenticated endpoints will require a JWT token in the Authorization header:

```text
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### POST /auth/signup

Create a new user account.

Request:

```json
{
  "email": "student@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

Response:

```json
{
  "user_id": "123",
  "email": "student@example.com",
  "token": "jwt_token_here"
}
```

#### POST /auth/login

Login existing user.

Request:

```json
{
  "email": "student@example.com",
  "password": "secure_password"
}
```

Response:

```json
{
  "token": "jwt_token_here",
  "user": {
    "id": "123",
    "email": "student@example.com",
    "name": "John Doe"
  }
}
```

### Jobs

#### GET /jobs/search

Search for construction jobs.

Query parameters:

- `query` required: job search query, such as `electrician helper`
- `location` optional: job location, default `Seattle, WA`
- `limit` optional: number of results, default `20`, max `100`

Response:

```json
{
  "jobs": [
    {
      "id": "job_123",
      "title": "Electrician Helper",
      "company": "ABC Electric",
      "location": "Seattle, WA",
      "pay": "$22-25/hour",
      "score": 85,
      "lni_verified": true,
      "glassdoor_rating": 4.2,
      "hours_count": true,
      "url": "https://indeed.com/job/123"
    }
  ]
}
```

### Resumes

The resume endpoints are live and run on the rule-based translation engine
ported from the resume-workshop-app build-out (instructor-vetted content,
no AI API key required).

#### GET /resumes/trades

List the 26 trades that have instructor-vetted objective starters.

#### GET /resumes/skills

Return the vetted skills canon grouped by category (transferable,
job-specific, self-management).

#### GET /resumes/objectives

Query parameters:

- `trade` required: target trade, such as `Carpenter (General)`
- `mode` optional: `apprenticeship` (default) or `job`

Returns instructor-vetted objective starters for the trade, with generic
fallbacks for unknown trades.

#### GET /resumes/roles

List the 20 prior-work roles that have vetted bullet banks.

#### GET /resumes/role-bullets

Query parameters:

- `role` required: prior role, such as `Line Cook`

Returns measured, evidence-ready duty bullets (≤24 words each) plus the
construction skills those bullets demonstrate. Returns 404 for unknown roles.

#### POST /resumes/parse

Parse raw resume text into structured suggestions.

Request:

```json
{ "text": "Jordan Smith\nSeattle, WA\njordan@example.com\n(206) 555-1234\n..." }
```

Response includes `header` (name/email/phone/city/state), `education`,
`certifications` (normalized labels, e.g. `OSHA Outreach 10-Hour
(Construction)`), `detected_roles`, `suggested_bullets` per role, and
`suggested_skills`.

#### POST /resumes/generate

Build a construction-ready resume context: union-neutral language, normalized
skills, ≤24-word bullets, one-page caps (12 skills, 3 jobs, 4 bullets/job).

Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "206-555-1234",
  "city": "Seattle",
  "state": "WA",
  "target_trade": "Electrician – Inside (01)",
  "objective": "",
  "skills": ["teamwork", "forklift"],
  "certifications": ["OSHA 10"],
  "job_history": [
    {
      "title": "Cashier",
      "company": "McDonald's",
      "city": "Seattle, WA",
      "dates": "2021 - 2023",
      "bullets": ["Handled cash register", "Maintained clean workspace"]
    }
  ],
  "education": [
    { "school": "Rainier Beach High School", "credential": "Diploma", "year": "2018" }
  ]
}
```

Response: `{ "status": "ok", "resume": { ...cleaned context... } }`. When no
`objective` is supplied and `target_trade` is set, the response also includes
`objective_suggestions` from the vetted starters bank. PDF/DOCX export is the
next planned step.
