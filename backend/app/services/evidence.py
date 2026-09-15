from app.database.connection import SessionLocal
from app.database.models import (
    ProjectDB,
    ProjectPerformanceDB,
    SourceDB,
)


def get_latest_performance(
    db,
    project_id: int,
):
    return (
        db.query(ProjectPerformanceDB)
        .filter(
            ProjectPerformanceDB.project_id == project_id,
        )
        .order_by(
            ProjectPerformanceDB.reporting_period.desc()
        )
        .first()
    )


def get_project_evidence(project_id: int):
    db = SessionLocal()

    try:
        project = (
            db.query(ProjectDB)
            .filter(ProjectDB.id == project_id)
            .first()
        )

        if not project:
            return None

        performance = get_latest_performance(
            db,
            project.id,
        )

        if performance:
            source = (
                db.query(SourceDB)
                .filter(
                    SourceDB.id == performance.source_id,
                )
                .first()
            )
        else:
            source = (
                db.query(SourceDB)
                .filter(
                    SourceDB.id == project.source_id,
                )
                .first()
            )

        if not source:
            return None

        return {
            "project": {
                "id": project.id,
                "project_description": (
                    project.project_description
                ),
                "administrative_description": (
                    project.administrative_description
                ),
                "budget_year": project.budget_year,
                "original_budget": (
                    project.original_budget
                ),
                "q1_performance": (
                    project.q1_performance
                ),
                "ytd_performance": (
                    performance.ytd_performance
                    if performance
                    else project.ytd_performance
                ),
                "performance_percentage": (
                    performance.performance_percentage
                    if performance
                    else project.performance_percentage
                ),
                "balance": (
                    performance.balance
                    if performance
                    else project.balance
                ),
                "source_page": (
                    performance.source_page
                    if performance
                    else project.source_page
                ),
            },
            "source": {
                "id": source.id,
                "title": source.title,
                "publisher": source.publisher,
                "publication_date": (
                    source.publication_date
                ),
                "reporting_period": (
                    source.reporting_period
                ),
                "document_type": source.document_type,
                "url": source.url,
            },
        }

    finally:
        db.close()