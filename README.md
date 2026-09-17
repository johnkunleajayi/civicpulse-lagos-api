# CivicPulse Lagos

**Know. Verify. Act.**

CivicPulse Lagos is an AI-powered civic information platform that helps Lagos residents understand public spending and government projects using structured data extracted from official government publications.

> **Public information shouldn't require a government insider to understand.**

---

## 🚀 Try CivicPulse

### Live Demo

**[Open CivicPulse Lagos](https://civicpulse-lagos.vercel.app/)**

The live frontend is already connected to the deployed backend. **No local setup is required to test the application.**

### ⚠️ About the Backend

The CivicPulse API is currently hosted on **Render's free tier**.

When the backend has been inactive for a while, Render may put it to sleep. The **first request can therefore take a little longer while the service wakes up**.

If the application appears to be loading slowly, please allow a few seconds and try again.

**Backend API:**  
https://civicpulse-lagos-api.onrender.com/

**API Documentation:**  
https://civicpulse-lagos-api.onrender.com/docs

### Backup

If the live application is temporarily unavailable, the project can also be reviewed through the repository and API documentation:

**GitHub Repository:**  
https://github.com/johnkunleajayi/civicpulse-lagos-api

---

## The Problem

Government budgets and performance reports contain valuable information, but they can be difficult for ordinary citizens to navigate and understand.

A citizen may want to ask:

- How much was budgeted for a project?
- How much has been spent?
- Which projects received the largest allocations?
- How much was spent on rail, health, or infrastructure?
- Where can I verify the information?

CivicPulse turns these questions into understandable answers while keeping the underlying evidence visible.

---

## How It Works

**Ask → Retrieve → Answer → Verify → Act**

1. **Ask** — A citizen asks a question in natural language.
2. **Retrieve** — CivicPulse identifies relevant records from structured government data.
3. **Answer** — The system presents the information in an understandable format.
4. **Verify** — Supporting source and reporting-period information is provided.
5. **Act** — The citizen can open the original government document and verify the information independently.

### Evidence First

CivicPulse follows a simple principle:

> **The AI explains the evidence; it does not invent the evidence.**

The underlying figures come from official Lagos State government publications. The AI interaction sits on top of the evidence rather than replacing it.

---

## Current Data

The current MVP focuses on the **Lagos State 2026 Budget and Q2 2026 Budget Performance Report**.

The dataset currently contains project-level information across areas including:

- Rail
- Transportation
- Health
- Infrastructure
- Agriculture
- Fire and Rescue

### Primary Source

**Lagos State Government — Q2 2026 Budget Performance Report**

https://lagosmepb.org/wp-content/uploads/Y2026-LASG-Q2-BIR.pdf

---

## Example

A citizen can ask:

> **How much did Lagos spend on rail projects in Q2 2026?**

CivicPulse retrieves the relevant project records and presents the available expenditure information together with supporting source references.

The citizen can then follow the evidence back to the official government report.

**Information → Understanding → Verification**

---

## Key Features

- Natural-language civic questions
- Project-level budget and expenditure data
- Category-based queries
- Project comparison and ranking
- Evidence attached to answers
- Official source links
- Reporting-period references
- Source-page references
- Evidence-first retrieval

---

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend

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

CivicPulse focuses on Transparency & Accountability by making public financial information easier to understand while preserving a clear path back to the original evidence.

Project Status

MVP / Hackathon Proof of Concept

The current version demonstrates the core citizen journey:

Ask → Understand → Verify

The MVP currently uses Lagos State 2026 budget and Q2 2026 budget performance data.

Future iterations can expand coverage to additional reporting periods, government datasets, sectors, and civic use cases.

License

This project is currently provided as a hackathon proof of concept.
