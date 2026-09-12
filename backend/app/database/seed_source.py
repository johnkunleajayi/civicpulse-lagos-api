from datetime import date

from app.database.connection import SessionLocal
from app.database.models import SourceDB


SOURCE_URL = (
    "https://lagosmepb.org/wp-content/uploads/"
    "Lagos%20Q1%272026%20BPR%20Publication.pdf"
)


db = SessionLocal()

try:
    existing_source = (
        db.query(SourceDB)
        .filter(SourceDB.url == SOURCE_URL)
        .first()
    )

    if existing_source:
        print(
            f"Source already exists with ID: {existing_source.id}"
        )
    else:
        source = SourceDB(
            title="Lagos State Q1 2026 Budget Performance Report",
            publisher="Lagos State Government",
            publication_date=date(2026, 4, 30),
            reporting_period="Q1 2026",
            document_type="Budget Performance Report",
            url=SOURCE_URL,
        )

        db.add(source)
        db.commit()
        db.refresh(source)

        print(
            f"Source created successfully with ID: {source.id}"
        )

finally:
    db.close()