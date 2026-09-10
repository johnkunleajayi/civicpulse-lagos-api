from fastapi import APIRouter

from app.database.connection import SessionLocal
from app.database.models import SourceDB


router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)


@router.get("/")
def get_sources():
    db = SessionLocal()

    try:
        sources = db.query(SourceDB).all()

        return sources

    finally:
        db.close()