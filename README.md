# CivicPulse Lagos

**Know. Verify. Act.**

CivicPulse Lagos is an AI-powered civic information platform that helps Lagos residents understand public spending and government projects using verified information from official government sources.

> **Public information shouldn't require a government insider to understand.**

## The Problem

Government budgets and performance reports contain valuable information, but they are often difficult for ordinary citizens to navigate and understand.

A citizen may want to ask:

* How much was budgeted for a particular project?
* How much has been spent?
* Which projects received the largest allocations?
* How much was spent on rail or health projects?
* Where can I verify the information?

CivicPulse turns these questions into understandable answers while keeping the underlying evidence visible.

## How It Works

CivicPulse follows an evidence-first approach:

**Ask → Retrieve → Answer → Verify → Act**

1. **Ask** — A citizen asks a question in natural language.
2. **Retrieve** — CivicPulse identifies relevant structured records from verified government data.
3. **Answer** — The system generates a concise answer from the retrieved data.
4. **Verify** — The user sees the official source, reporting period, and document page supporting the answer.
5. **Act** — The user can open the official document and verify the information independently.

### AI Does Not Decide the Facts

CivicPulse is designed around a simple principle:

> **The AI explains the evidence; it does not invent the evidence.**

The underlying project and budget figures come from official government publications. The system retrieves relevant evidence before presenting an answer.

## Current Data Scope

The current proof of concept focuses on the **Lagos State 2026 Budget and Q1 2026 Budget Performance Report**.

The dataset currently includes verified capital-project records across areas including:

* Rail
* Transportation
* Health
* Infrastructure
* Agriculture
* Fire and Rescue

The primary source is the Lagos State Government's **Q1 2026 Budget Performance Report**.

Official source:

https://lagosmepb.org/wp-content/uploads/Lagos%20Q1%272026%20BPR%20Publication.pdf

## Example

A citizen can ask:

> How much did Lagos spend on rail projects in Q1 2026?

CivicPulse can return the verified expenditure across the available rail projects and provide the supporting government report and page number for each result.

This allows the citizen to move from **information → understanding → verification**.

## Key Features

* Natural-language civic questions
* Verified government budget data
* Project-level budget and expenditure information
* Category-based civic queries
* Project ranking and comparison
* Evidence attached to answers
* Official source links
* Reporting period and source-page references
* Simple, accessible interface
* Evidence-first architecture

## Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

### Architecture

```text
Citizen
   ↓
React + Vite Frontend
   ↓
FastAPI API
   ↓
Question Intent & Retrieval
   ↓
Verified Project / Budget Data
   ↓
Evidence Retrieval
   ↓
Answer + Official Source
```

## Repository Structure

```text
civicpulse-lagos/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── .gitignore
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/johnkunleajayi/civicpulse-lagos-api.git
cd civicpulse-lagos-api
```

### 2. Start the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## Trust & Verification

CivicPulse is built around four principles:

### Official Sources

The foundation of the system is published government information.

### Evidence Before Explanation

Relevant records are retrieved before an answer is presented.

### Traceability

Supported answers expose the source, reporting period, and document page.

### Citizen Verification

Users can open the original government document and independently check the evidence.

## Hackathon Context

CivicPulse Lagos was built for the **OSF × Andela Hackathon: Build for Africa, Take It to Kenya**.

The project aligns with the theme:

> **Information you can trust.**

It contributes to the hackathon tracks around:

* Transparency & Accountability
* Stability & Social Cohesion
* Safety, Reporting & Protection

The proof of concept demonstrates how technology can make public information easier to understand while preserving a clear path back to the original evidence.

## Project Status

**Proof of Concept / MVP**

The current version demonstrates the core citizen journey:

**Ask → Understand → Verify**

Future iterations can expand the data coverage, support additional government datasets, improve multilingual access, and provide more civic actions based on verified information.

## License

This project is currently provided as a hackathon proof of concept.
