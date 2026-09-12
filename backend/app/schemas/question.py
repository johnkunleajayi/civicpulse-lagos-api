from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.evidence import EvidenceResponse


class QuestionRequest(BaseModel):
    question: str


class SummaryEvidenceSource(BaseModel):
    id: int
    title: str
    publisher: str
    publication_date: date
    reporting_period: str
    document_type: str
    url: str


class SummaryEvidence(BaseModel):
    id: int
    metric: str
    budget_year: int
    reporting_period: str

    original_budget: Decimal | None = None
    q1_performance: Decimal | None = None
    performance_percentage: Decimal | None = None

    source_page: int
    source: SummaryEvidenceSource


class QuestionResponse(BaseModel):
    question: str
    answer: str
    evidence: list[EvidenceResponse | SummaryEvidence]