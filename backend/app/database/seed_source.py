from datetime import date

from app.database.connection import SessionLocal
from app.database.models import SourceDB


source = SourceDB(
    title="Lagos State Q1 2026 Budget Performance Report",
    publisher="Lagos State Government",
    publication_date=date(2026, 4, 30),
    reporting_period="Q1 2026",
    document_type="Budget Performance Report",
    url="https://lagosmepb.org/wp-content/uploads/Lagos%20Q1%272026%20BPR%20Publication.pdf",
)


db = SessionLocal()

try:
    db.add(source)
    db.commit()
    db.refresh(source)

    print(f"Source created successfully with ID: {source.id}")

finally:
    db.close()