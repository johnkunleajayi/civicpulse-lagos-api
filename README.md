# CivicPulse Lagos

**Know. Verify. Act.**

CivicPulse Lagos is an AI-powered civic information platform that helps Lagos residents understand public spending and government projects using structured data extracted from official government publications.

> **Public information shouldn't require a government insider to understand.**

## The Problem

Government budgets and performance reports contain valuable information, but they can be difficult for ordinary citizens to navigate and understand.

A citizen may want to ask:

- How much was budgeted for a project?
- How much has been spent?
- Which projects received the largest allocations?
- How much was spent on rail, health, or infrastructure?
- Where can I verify the information?

CivicPulse turns these questions into understandable answers while keeping the underlying evidence visible.

## How It Works

**Ask → Retrieve → Answer → Verify → Act**

1. **Ask** — The citizen asks a question in natural language.
2. **Retrieve** — CivicPulse finds the relevant records from structured government data.
3. **Answer** — The system presents the information in a concise format.
4. **Verify** — The answer includes the supporting source and reporting period.
5. **Act** — The citizen can open the original government document and verify the information independently.

### Evidence First

CivicPulse is built on a simple principle:

> **The AI explains the evidence; it does not invent the evidence.**

The underlying figures come from official Lagos State government publications. The AI interaction sits on top of the evidence rather than replacing it.

## Current Data

The current MVP focuses on the **Lagos State 2026 Budget and Q2 2026 Budget Performance Report**.

The dataset currently covers project-level information across areas including:

- Rail
- Transportation
- Health
- Infrastructure
- Agriculture
- Fire and Rescue

**Primary source:**

[Lagos State Government — Q2 2026 Budget Performance Report](https://lagosmepb.org/wp-content/uploads/Y2026-LASG-Q2-BIR.pdf)

## Example

A citizen can ask:

> **How much did Lagos spend on rail projects in Q2 2026?**

CivicPulse retrieves the relevant project records and presents the available expenditure information together with supporting source references.

The user can then follow the evidence back to the official government report.

**Information → Understanding → Verification**

## Key Features

- Natural-language civic questions
- Project-level budget and expenditure data
- Category-based queries
- Project comparison and ranking
- Evidence attached to answers
- Official source links
- Reporting-period and page references
- Evidence-first retrieval

## Technology Stack

**Frontend**
- React
- Vite
- Tailwind CSS

**Backend**
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Architecture

```text
Citizen
   ↓
React + Vite
   ↓
FastAPI
   ↓
Question Intent & Retrieval
   ↓
Structured Government Data
   ↓
Evidence
   ↓
Answer + Official Source
Repository Structure
civicpulse-lagos-api/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── .gitignore
Running Locally
Backend
git clone https://github.com/johnkunleajayi/civicpulse-lagos-api.git
cd civicpulse-lagos-api/backend

python -m venv venv

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Start the API:

python -m uvicorn app.main:app --reload

API:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
Hackathon Context

CivicPulse Lagos was built for the OSF × Andela Hackathon: Build for Africa, Take It to Kenya.

The project responds to the theme:

Information you can trust.

It focuses on Transparency & Accountability by making public financial information easier to understand while preserving a clear path back to the original evidence.

Project Status

MVP / Hackathon Proof of Concept

The current version demonstrates the core citizen journey:

Ask → Understand → Verify

Future iterations can expand the dataset to additional reporting periods, government datasets, sectors, and civic use cases.

License

This project is currently provided as a hackathon proof of concept.
