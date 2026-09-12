from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class EvidenceSource(BaseModel):
    id: int
    title: str
    publisher: str
    publication_date: date
    reporting_period: str
    document_type: str
    url: str


class EvidenceProject(BaseModel):
    id: int
    project_description: str
    administrative_description: str
    budget_year: int

    original_budget: Decimal | None = None
    q1_performance: Decimal | None = None
    ytd_performance: Decimal | None = None
    performance_percentage: Decimal | None = None
    balance: Decimal | None = None

    source_page: int


class EvidenceResponse(BaseModel):
    project: EvidenceProject
    source: EvidenceSource