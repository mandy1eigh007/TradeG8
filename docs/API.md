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

#### POST /resumes/generate

Generate a construction-language resume.

Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "206-555-1234",
  "target_trade": "electrician",
  "job_history": [
    {
      "title": "Cashier",
      "company": "McDonald's",
      "duration": "2 years",
      "responsibilities": [
        "Handled cash register",
        "Maintained clean workspace",
        "Followed safety procedures"
      ]
    }
  ]
}
```

Response:

```json
{
  "resume_id": "resume_123",
  "pdf_url": "https://storage.url/resume.pdf",
  "docx_url": "https://storage.url/resume.docx"
}
```
