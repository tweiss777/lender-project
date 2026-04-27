# Lender Matching Platform

A loan underwriting and lender matching system that evaluates business loan applications against multiple lenders' credit policies. Upload a lender guidelines PDF, and the system extracts and normalizes the policy criteria automatically. Submit a loan application and get back a ranked list of eligible lenders with detailed pass/fail reasoning per criterion.

---

## Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- An [Anthropic API key](https://console.anthropic.com/) (used for PDF parsing)

---

## Quick Start

**1. Clone the repository**

```bash
git clone <repo-url>
cd <repo>
```

**2. Set up environment variables**

If running without Docker Compose:

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

> If running with Docker Compose, set environment variables directly in `docker-compose.yml` instead.

**3. Build and start all services**

```bash
docker compose up --build
```

This will:
- Start a PostgreSQL database
- Seed it with 5 real lenders and 12 programs from the provided PDFs
- Start the FastAPI server on port 3000 (internal)
- Build and serve the React client at **http://localhost:80**

**4. Open the app**

```
http://localhost:80
```

To stop everything:

```bash
docker compose down
```

To stop and wipe the database volume:

```bash
docker compose down -v
```

---

## Project Structure

```
.
├── docker-compose.yml
├── .env.example
├── server/                  # FastAPI backend
│   ├── Dockerfile
│   ├── main.py
│   ├── pyproject.toml
│   └── app/
│       ├── models/          # SQLAlchemy models
│       ├── routes/          # FastAPI routers
│       ├── services/        # Matching engine + PDF parser
│       │   └── checks/      # One file per eligibility criterion
│       ├── abstractions/    # EvaluationCheck base class
│       ├── Schemas/         # Pydantic request/response schemas
│       ├── database.py
│       └── seed.py
└── client/                  # React + TypeScript frontend
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── pages/
        │   └── apply/       # Multi-step application flow
        ├── components/      # StepLayout, CriteriaResultCard
        ├── store/           # Redux store + applicationSlice
        └── types/           # Shared TypeScript types
```

---

## Architecture

### Backend

The server is built with **FastAPI** and **SQLAlchemy** backed by **PostgreSQL**.

**Lender Policy Schema** — policies are normalized across several tables rather than stored as a blob. Each `LenderPolicy` row holds scalar criteria (min FICO, min PayNet, loan amount range, etc.) and links to join tables for list-based criteria:

- `lender_allowed_industries` / `lender_excluded_industries`
- `lender_allowed_states` / `lender_excluded_states`
- `lender_equipment_restrictions`

This separation makes whitelist vs blacklist logic explicit and keeps each table purpose-specific.

**Matching Engine** — the core of the system. When underwriting is triggered, `MatchingEngine.run()` loads the borrower, guarantor, business credit, and loan request into an `ApplicationContext`, then evaluates every `LenderPolicy` in the database using a list of `EvaluationCheck` instances. Each check returns a `CriterionResult(name, passed, reason)` or `None` if the criterion doesn't apply to that policy. The fit score is `passed / total * 100`. Results are persisted to `match_results` with the full per-criterion JSON for the UI to display.

**Adding a new check** — create a file in `app/services/checks/`, subclass `EvaluationCheck`, implement `evaluate(app_ctx, policy_ctx)`, and add an instance to the list in `MatchingEngine.__init__`. No other changes required.

**PDF Parser** — lender guidelines PDFs are base64-encoded and sent to the Claude API with a structured extraction prompt. Claude returns a JSON object matching the `LenderPreview` schema. The user reviews the preview before it is committed to the database. Re-uploading the same lender upserts by `(lender_id, program_name)` — no duplicates.

### Frontend

Built with **React + TypeScript + Vite**, styled with **Tailwind CSS** and **shadcn/ui**. Application state across the multi-step form is managed with **Redux Toolkit**.

In Docker, nginx serves the built assets and proxies `/api/` requests to the server container over the internal `kaaj_network` — the browser never talks to the server directly.

---

## API Reference

### Borrowers

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/borrowers` | Create a borrower |
| `GET` | `/api/v1/borrowers/:id` | Get a borrower |
| `PATCH` | `/api/v1/borrowers/:id` | Update a borrower |
| `DELETE` | `/api/v1/borrowers/:id` | Delete a borrower |
| `POST` | `/api/v1/borrowers/:id/underwrite` | Run underwriting for a loan request |
| `GET` | `/api/v1/borrowers/:id/underwrite` | Get existing underwriting results |

**POST `/api/v1/borrowers`**
```json
{
  "company_name": "Acme Equipment LLC",
  "industry": "Construction",
  "state": "TX",
  "years_in_business": 7,
  "revenue": 2500000
}
```

**POST `/api/v1/borrowers/:id/underwrite`**
```json
{
  "loan_request_id": 1
}
```

Returns a ranked list of all lender programs with eligibility status and per-criterion pass/fail detail.

---

### Loan Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/loan_requests` | Create a loan request |
| `GET` | `/api/v1/loan_requests/:id` | Get a loan request |
| `PATCH` | `/api/v1/loan_requests/:id` | Update a loan request |
| `DELETE` | `/api/v1/loan_requests/:id` | Delete a loan request |

**POST `/api/v1/loan_requests`**
```json
{
  "borrower_id": 1,
  "amount": 150000,
  "term_months": 60,
  "equipment_type": "Excavator",
  "equipment_year": 2023,
  "equipment_cost": 160000,
  "equipment_description": "2023 CAT 320 Hydraulic Excavator",
  "status": "pending"
}
```

---

### Lenders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/lenders` | List all lenders and their programs |
| `POST` | `/api/v1/lenders/parse` | Upload a PDF and get a structured policy preview |
| `POST` | `/api/v1/lenders/confirm` | Confirm and save a parsed lender preview |

**POST `/api/v1/lenders/parse`**

`multipart/form-data` with a `file` field containing the PDF.

Returns a `LenderPreview` object for review — nothing is written to the database.

**POST `/api/v1/lenders/confirm`**

Body: the `LenderPreview` JSON returned from `/parse` (optionally edited).

Upserts the lender and all programs. Response:
```json
{
  "lender_name": "Apex Commercial Capital",
  "programs_created": ["A Rate", "B Rate"],
  "programs_updated": []
}
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Used by the PDF parser to extract lender policies |
| `CONNECTION_STRING` | Yes | PostgreSQL connection string |
| `PORT` | No | Server port (default: `3000`) |
| `CORS_ORIGINS` | No | Comma-separated allowed origins (default: `http://localhost:5173,http://localhost:80`) |
