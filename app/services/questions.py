from sqlalchemy import or_

from app.database.connection import SessionLocal
from app.database.models import ProjectDB


STOP_WORDS = {
    "what",
    "when",
    "where",
    "which",
    "who",
    "how",
    "much",
    "was",
    "were",
    "the",
    "for",
    "from",
    "about",
    "does",
    "did",
    "this",
    "that",
    "with",
    "have",
    "has",
    "been",
    "budgeted",
    "spent",
}


def find_projects(question: str):
    db = SessionLocal()

    try:
        words = question.lower().replace("?", "").split()

        search_words = [
            word
            for word in words
            if len(word) >= 4 and word not in STOP_WORDS
        ]

        query = db.query(ProjectDB)

        if search_words:
            conditions = [
                ProjectDB.project_description.ilike(f"%{word}%")
                for word in search_words
            ]

            query = query.filter(or_(*conditions))

        projects = query.all()

        scored_projects = []

        for project in projects:
            description = project.project_description.lower()

            matched_words = [
                word
                for word in search_words
                if word in description
            ]

            score = sum(len(word) for word in matched_words)

            scored_projects.append((score, project))

        scored_projects.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            {
                "id": project.id,
                "administrative_code": project.administrative_code,
                "administrative_description": project.administrative_description,
                "project_description": project.project_description,
                "budget_year": project.budget_year,
                "original_budget": project.original_budget,
                "q1_performance": project.q1_performance,
                "ytd_performance": project.ytd_performance,
                "performance_percentage": project.performance_percentage,
                "balance": project.balance,
                "source_id": project.source_id,
                "source_page": project.source_page,
            }
            for score, project in scored_projects
            if score > 0
        ]

    finally:
        db.close()


def generate_answer(question: str, projects: list[dict]):
    if not projects:
        return "I could not find a verified Lagos State project matching your question."

    project = projects[0]
    question_lower = question.lower()

    if "percentage" in question_lower or "percent" in question_lower:
        percentage = project["performance_percentage"]

        return (
            f"The {project['project_description']} has used "
            f"{percentage:.1f}% of its original 2026 budget "
            f"as reported for Q1 2026."
        )

    if "spent" in question_lower or "performance" in question_lower:
        amount = project["ytd_performance"]

        return (
            f"The {project['project_description']} has recorded "
            f"₦{amount:,.2f} in 2026 year-to-date expenditure "
            f"as reported for Q1 2026."
        )

    if "left" in question_lower or "balance" in question_lower:
        amount = project["balance"]

        return (
            f"The remaining balance for the {project['project_description']} "
            f"is ₦{amount:,.2f} against its original 2026 budget."
        )

    budget = project["original_budget"]

    return (
        f"The {project['project_description']} has an original 2026 budget "
        f"of ₦{budget:,.2f}."
    )