from app.database.connection import SessionLocal
from app.database.models import BudgetSummaryDB, SourceDB


def get_budget_summary_evidence(summary_id: int):
    db = SessionLocal()

    try:
        summary = (
            db.query(BudgetSummaryDB)
            .filter(BudgetSummaryDB.id == summary_id)
            .first()
        )

        if not summary:
            return None

        source = (
            db.query(SourceDB)
            .filter(SourceDB.id == summary.source_id)
            .first()
        )

        return {
            "id": summary.id,
            "metric": summary.metric,
            "budget_year": summary.budget_year,
            "reporting_period": summary.reporting_period,
            "original_budget": summary.original_budget,
            "q1_performance": summary.q1_performance,
            "performance_percentage": summary.performance_percentage,
            "source_page": summary.source_page,
            "source": source,
        }

    finally:
        db.close()