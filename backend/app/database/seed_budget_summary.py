from decimal import Decimal

from app.database.connection import SessionLocal
from app.database.models import BudgetSummaryDB, SourceDB


SOURCE_URL = (
    "https://lagosmepb.org/wp-content/uploads/"
    "Lagos%20Q1%272026%20BPR%20Publication.pdf"
)

Q1_REPORTING_PERIOD = "Q1 2026"
BUDGET_YEAR = 2026

CAPITAL_BUDGET = Decimal("2337805210325.31")
Q1_CAPITAL_EXPENDITURE = Decimal("340762383816.67")
Q1_PERFORMANCE_PERCENTAGE = Decimal("14.6")

SOURCE_PAGE = 56


def seed_budget_summary():
    db = SessionLocal()

    try:
        source = (
            db.query(SourceDB)
            .filter(SourceDB.url == SOURCE_URL)
            .first()
        )

        if not source:
            raise RuntimeError(
                "Q1 2026 Budget Performance Report "
                "source was not found."
            )

        summary = (
            db.query(BudgetSummaryDB)
            .filter(
                BudgetSummaryDB.metric
                == "Total Capital Expenditure",
                BudgetSummaryDB.budget_year
                == BUDGET_YEAR,
                BudgetSummaryDB.reporting_period
                == Q1_REPORTING_PERIOD,
            )
            .first()
        )

        if summary:
            summary.original_budget = CAPITAL_BUDGET
            summary.q1_performance = (
                Q1_CAPITAL_EXPENDITURE
            )
            summary.performance_percentage = (
                Q1_PERFORMANCE_PERCENTAGE
            )
            summary.source_id = source.id
            summary.source_page = SOURCE_PAGE

            print(
                "Capital expenditure summary updated."
            )

        else:
            summary = BudgetSummaryDB(
                metric="Total Capital Expenditure",
                budget_year=BUDGET_YEAR,
                reporting_period=Q1_REPORTING_PERIOD,
                original_budget=CAPITAL_BUDGET,
                q1_performance=Q1_CAPITAL_EXPENDITURE,
                performance_percentage=(
                    Q1_PERFORMANCE_PERCENTAGE
                ),
                source_id=source.id,
                source_page=SOURCE_PAGE,
            )

            db.add(summary)

            print(
                "Capital expenditure summary added."
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_budget_summary()