from app.database.connection import SessionLocal
from app.database.models import ProjectDB, SourceDB


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

        source = (
            db.query(SourceDB)
            .filter(SourceDB.id == project.source_id)
            .first()
        )

        return {
            "project": project,
            "source": source,
        }

    finally:
        db.close()