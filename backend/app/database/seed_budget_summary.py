from decimal import Decimal

from app.database.connection import SessionLocal
from app.database.models import BudgetSummaryDB, SourceDB


SOURCE_URL = (
    "https://lagosmepb.org/wp-content/uploads/"
    "Y2026-LASG-Q2-BIR.pdf"
)

Q2_REPORTING_PERIOD = "Q2 2026"
BUDGET_YEAR = 2026

CAPITAL_BUDGET = Decimal("2337805210325.31")
Q2_CAPITAL_EXPENDITURE = Decimal("772640867614.64")
Q2_PERFORMANCE_PERCENTAGE = Decimal("33.0")

SOURCE_PAGE = 5


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
                "Q2 2026 Budget Implementation Report "
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
                == Q2_REPORTING_PERIOD,
            )
            .first()
        )

        if summary:
            summary.original_budget = CAPITAL_BUDGET
            summary.q1_performance = Q2_CAPITAL_EXPENDITURE
            summary.performance_percentage = (
                Q2_PERFORMANCE_PERCENTAGE
            )
            summary.source_id = source.id
            summary.source_page = SOURCE_PAGE

            print(
                "Q2 capital expenditure summary updated."
            )

        else:
            summary = BudgetSummaryDB(
                metric="Total Capital Expenditure",
                budget_year=BUDGET_YEAR,
                reporting_period=Q2_REPORTING_PERIOD,
                original_budget=CAPITAL_BUDGET,
                q1_performance=Q2_CAPITAL_EXPENDITURE,
                performance_percentage=(
                    Q2_PERFORMANCE_PERCENTAGE
                ),
                source_id=source.id,
                source_page=SOURCE_PAGE,
            )

            db.add(summary)

            print(
                "Q2 capital expenditure summary added."
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_budget_summary()