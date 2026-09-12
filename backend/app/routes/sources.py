from fastapi import APIRouter

from app.database.connection import SessionLocal
from app.database.models import SourceDB
from app.schemas.source import SourceResponse


router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)


@router.get("/", response_model=list[SourceResponse])
def get_sources():
    db = SessionLocal()

    try:
        sources = db.query(SourceDB).all()

        return sources

    finally:
        db.close()