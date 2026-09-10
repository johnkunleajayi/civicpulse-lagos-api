from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class Project(BaseModel):
    administrative_code: str
    administrative_description: str
    project_description: str

    budget_year: int

    original_budget: Optional[Decimal] = None
    q1_performance: Optional[Decimal] = None
    ytd_performance: Optional[Decimal] = None
    performance_percentage: Optional[Decimal] = None
    balance: Optional[Decimal] = None

    source_id: str
    source_page: int