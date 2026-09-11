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
    },
    {
        "administrative_code": "011113600100",
        "administrative_description": "Fire Service",
        "project_description": "Rehabilitation of Fire Service Security and Control Centre",
        "budget_year": 2026,
        "original_budget": Decimal("1043767965"),
        "q1_performance": Decimal("200000000"),
        "ytd_performance": Decimal("200000000"),
        "performance_percentage": Decimal("19.2"),
        "balance": Decimal("843767965"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
    {
        "administrative_code": "011113600100",
        "administrative_description": "Fire Service",
        "project_description": "FIRE AND RESCUE SERVICE RESPONSE UNIT (HEAVY DUTY VEHICLE EQUIPMENT)",
        "budget_year": 2026,
        "original_budget": Decimal("2100000000"),
        "q1_performance": Decimal("610641815.77"),
        "ytd_performance": Decimal("610641815.77"),
        "performance_percentage": Decimal("29.1"),
        "balance": Decimal("1489358184.23"),
        "source_id": SOURCE_ID,
        "source_page": 56,
    },
]


db = SessionLocal()

try:
    added = 0
    skipped = 0

    for project in projects:
        existing = (
            db.query(ProjectDB)
            .filter(
                ProjectDB.administrative_code
                == project["administrative_code"],
                ProjectDB.project_description
                == project["project_description"],
                ProjectDB.budget_year
                == project["budget_year"],
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        db.add(ProjectDB(**project))
        added += 1

    db.commit()

    print(f"Successfully added {added} projects.")
    print(f"Skipped {skipped} existing projects.")

finally:
    db.close()