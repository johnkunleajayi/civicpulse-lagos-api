from decimal import Decimal

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int

    administrative_code: str
    administrative_description: str
    project_description: str

    budget_year: int

    original_budget: Decimal | None = None
    q1_performance: Decimal | None = None
    ytd_performance: Decimal | None = None
    performance_percentage: Decimal | None = None
    balance: Decimal | None = None

    source_id: int
    source_page: int