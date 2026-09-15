from app.database.connection import SessionLocal
from app.database.models import ProjectDB, ProjectPerformanceDB


REPORTING_PERIOD = "Q1 2026"


db = SessionLocal()

try:
    projects = (
        db.query(ProjectDB)
        .filter(ProjectDB.budget_year == 2026)
        .all()
    )

    added = 0
    skipped = 0

    for project in projects:
        existing = (
            db.query(ProjectPerformanceDB)
            .filter(
                ProjectPerformanceDB.project_id == project.id,
                ProjectPerformanceDB.reporting_period
                == REPORTING_PERIOD,
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        performance = ProjectPerformanceDB(
            project_id=project.id,
            reporting_period=REPORTING_PERIOD,
            period_performance=project.q1_performance,
            ytd_performance=project.ytd_performance,
            performance_percentage=project.performance_percentage,
            balance=project.balance,
            source_id=project.source_id,
            source_page=project.source_page,
        )

        db.add(performance)
        added += 1

    db.commit()

    print(f"Successfully migrated {added} Q1 performance records.")
    print(f"Skipped {skipped} existing Q1 performance records.")

finally:
    db.close()