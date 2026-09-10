from fastapi import APIRouter, HTTPException, Query

from app.database.connection import SessionLocal
from app.database.models import ProjectDB


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("/")
def get_projects(
    search: str | None = Query(default=None),
):
    db = SessionLocal()

    try:
        query = db.query(ProjectDB)

        if search:
            query = query.filter(
                ProjectDB.project_description.ilike(f"%{search}%")
            )

        projects = query.all()

        return projects

    finally:
        db.close()


@router.get("/{project_id}")
def get_project(project_id: int):
    db = SessionLocal()

    try:
        project = (
            db.query(ProjectDB)
            .filter(ProjectDB.id == project_id)
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        return project

    finally:
        db.close()