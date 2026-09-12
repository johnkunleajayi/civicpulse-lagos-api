import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.models import Base
from app.routes.evidence import router as evidence_router
from app.routes.projects import router as projects_router
from app.routes.questions import router as questions_router
from app.routes.sources import router as sources_router


app = FastAPI(
    title="CivicPulse Lagos API",
    description="Trusted civic information for Lagos residents.",
    version="0.1.0",
)


frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


app.include_router(projects_router)
app.include_router(sources_router)
app.include_router(evidence_router)
app.include_router(questions_router)


@app.get("/")
def root():
    return {
        "name": "CivicPulse Lagos",
        "tagline": "Know. Verify. Act.",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }