from datetime import date
import re
from decimal import Decimal, InvalidOperation

import pdfplumber

from app.database.connection import SessionLocal
from app.database.models import ProjectDB, ProjectPerformanceDB, SourceDB


PDF_PATH = "app/database/source/Y2026-LASG-Q2-BIR.pdf"

SOURCE_URL = (
    "https://lagosmepb.org/wp-content/uploads/"
    "Y2026-LASG-Q2-BIR.pdf"
)

Q1_REPORTING_PERIOD = "Q1 2026"
Q2_REPORTING_PERIOD = "Q2 2026"
BUDGET_YEAR = 2026

TABLE_START_PAGE = 58
TABLE_END_PAGE = 70


def clean_text(value):
    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip()


def parse_decimal(value):
    value = clean_text(value)

    if value in {"-", ""}:
        return Decimal("0")

    value = value.replace(",", "").replace(" ", "")

    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def parse_percentage(value):
    value = clean_text(value)

    if value in {"-", ""}:
        return Decimal("0")

    value = value.replace("%", "").replace(" ", "")

    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def extract_project_rows():
    rows = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_index in range(
            TABLE_START_PAGE - 1,
            TABLE_END_PAGE,
        ):
            page = pdf.pages[page_index]

            tables = page.extract_tables()

            if not tables:
                continue

            table = tables[0]

            for row in table:
                if not row or len(row) < 7:
                    continue

                administrative = clean_text(row[0])
                project_description = clean_text(row[1])

                if administrative.lower().startswith(
                    "administrative code"
                ):
                    continue

                if not re.match(
                    r"^\d{12}\s+-\s+",
                    administrative,
                ):
                    continue

                if not project_description:
                    continue

                rows.append(
                    {
                        "page": page_index + 1,
                        "administrative": administrative,
                        "project_description": project_description,
                        "original_budget": row[2],
                        "q2_performance": row[3],
                        "ytd_performance": row[4],
                        "performance_percentage": row[5],
                        "balance": row[6],
                    }
                )

    return rows


def parse_project_row(row):
    administrative = row["administrative"]

    match = re.match(
        r"^(\d{12})\s+-\s+(.*)$",
        administrative,
    )

    if not match:
        return None

    administrative_code = match.group(1)
    administrative_description = clean_text(
        match.group(2)
    )

    original_budget = parse_decimal(
        row["original_budget"]
    )

    q2_performance = parse_decimal(
        row["q2_performance"]
    )

    ytd_performance = parse_decimal(
        row["ytd_performance"]
    )

    performance_percentage = parse_percentage(
        row["performance_percentage"]
    )

    balance = parse_decimal(
        row["balance"]
    )

    if original_budget is None:
        return None

    if q2_performance is None:
        q2_performance = Decimal("0")

    if ytd_performance is None:
        ytd_performance = Decimal("0")

    q1_performance = ytd_performance - q2_performance

    if q1_performance < 0:
        q1_performance = Decimal("0")

    return {
        "administrative_code": administrative_code,
        "administrative_description": administrative_description,
        "project_description": row["project_description"],
        "budget_year": BUDGET_YEAR,
        "original_budget": original_budget,
        "q1_performance": q1_performance,
        "q2_performance": q2_performance,
        "ytd_performance": ytd_performance,
        "performance_percentage": performance_percentage,
        "balance": balance,
        "source_page": row["page"],
    }


def get_or_create_source(db):
    source = (
        db.query(SourceDB)
        .filter(SourceDB.url == SOURCE_URL)
        .first()
    )

    if source:
        return source

    source = SourceDB(
        title="Lagos State Q2 2026 Budget Performance Report",
        publisher="Lagos State Government",
        publication_date=date(2026, 7, 27),
        reporting_period=Q2_REPORTING_PERIOD,
        document_type="Budget Performance Report",
        url=SOURCE_URL,
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


def find_or_create_project(db, data):
    project = (
        db.query(ProjectDB)
        .filter(
            ProjectDB.administrative_code
            == data["administrative_code"],
            ProjectDB.project_description
            == data["project_description"],
            ProjectDB.budget_year
            == BUDGET_YEAR,
        )
        .first()
    )

    if project:
        return project, False

    project = ProjectDB(
        administrative_code=data["administrative_code"],
        administrative_description=data[
            "administrative_description"
        ],
        project_description=data[
            "project_description"
        ],
        budget_year=BUDGET_YEAR,
        original_budget=data["original_budget"],
        q1_performance=None,
        ytd_performance=None,
        performance_percentage=None,
        balance=None,
        source_id=data["source_id"],
        source_page=data["source_page"],
    )

    db.add(project)
    db.flush()

    return project, True


def save_performance(
    db,
    project,
    reporting_period,
    period_performance,
    ytd_performance,
    performance_percentage,
    balance,
    source_id,
    source_page,
):
    existing = (
        db.query(ProjectPerformanceDB)
        .filter(
            ProjectPerformanceDB.project_id
            == project.id,
            ProjectPerformanceDB.reporting_period
            == reporting_period,
        )
        .first()
    )

    if existing:
        existing.period_performance = period_performance
        existing.ytd_performance = ytd_performance
        existing.performance_percentage = (
            performance_percentage
        )
        existing.balance = balance
        existing.source_id = source_id
        existing.source_page = source_page

        return "updated"

    performance = ProjectPerformanceDB(
        project_id=project.id,
        reporting_period=reporting_period,
        period_performance=period_performance,
        ytd_performance=ytd_performance,
        performance_percentage=performance_percentage,
        balance=balance,
        source_id=source_id,
        source_page=source_page,
    )

    db.add(performance)

    return "added"


def import_projects():
    rows = extract_project_rows()

    print(
        f"Extracted table rows: {len(rows)}"
    )

    db = SessionLocal()

    try:
        source = get_or_create_source(db)

        added_projects = 0
        existing_projects = 0
        q1_added = 0
        q1_updated = 0
        q2_added = 0
        q2_updated = 0
        skipped_rows = 0

        for row in rows:
            data = parse_project_row(row)

            if not data:
                skipped_rows += 1
                continue

            data["source_id"] = source.id

            project, added = find_or_create_project(
                db,
                data,
            )

            if added:
                added_projects += 1
            else:
                existing_projects += 1

                project.original_budget = (
                    data["original_budget"]
                )
                project.administrative_description = (
                    data["administrative_description"]
                )
                project.source_id = source.id
                project.source_page = data["source_page"]

            q1_result = save_performance(
                db=db,
                project=project,
                reporting_period=Q1_REPORTING_PERIOD,
                period_performance=data[
                    "q1_performance"
                ],
                ytd_performance=data[
                    "q1_performance"
                ],
                performance_percentage=(
                    (
                        data["q1_performance"]
                        / data["original_budget"]
                    )
                    * 100
                    if data["original_budget"]
                    else Decimal("0")
                ),
                balance=(
                    data["original_budget"]
                    - data["q1_performance"]
                ),
                source_id=source.id,
                source_page=data["source_page"],
            )

            if q1_result == "added":
                q1_added += 1
            else:
                q1_updated += 1

            q2_result = save_performance(
                db=db,
                project=project,
                reporting_period=Q2_REPORTING_PERIOD,
                period_performance=data[
                    "q2_performance"
                ],
                ytd_performance=data[
                    "ytd_performance"
                ],
                performance_percentage=data[
                    "performance_percentage"
                ],
                balance=data["balance"],
                source_id=source.id,
                source_page=data["source_page"],
            )

            if q2_result == "added":
                q2_added += 1
            else:
                q2_updated += 1

        db.commit()

        print(
            f"Projects added: {added_projects}"
        )
        print(
            f"Existing projects matched: "
            f"{existing_projects}"
        )
        print(
            f"Q1 performance records added: "
            f"{q1_added}"
        )
        print(
            f"Q1 performance records updated: "
            f"{q1_updated}"
        )
        print(
            f"Q2 performance records added: "
            f"{q2_added}"
        )
        print(
            f"Q2 performance records updated: "
            f"{q2_updated}"
        )
        print(
            f"Rows skipped: {skipped_rows}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_projects()