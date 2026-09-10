from decimal import Decimal

from app.database.connection import SessionLocal
from app.database.models import ProjectDB


SOURCE_ID = 1


projects = [
    {
        "administrative_code": "011101000100",
        "administrative_description": "Lagos State Public Procurement Agency",
        "project_description": "Integration and set-up of E-Procurement system in 10 MDAs",
        "budget_year": 2026,
        "original_budget": Decimal("680410575"),
        "q1_performance": Decimal("0"),
        "ytd_performance": Decimal("0"),
        "performance_percentage": Decimal("0"),
        "balance": Decimal("680410575"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    }
]


db = SessionLocal()

try:
    for project in projects:
        db.add(ProjectDB(**project))

    db.commit()

    print(f"Successfully seeded {len(projects)} projects.")

finally:
    db.close()