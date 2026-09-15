import re

from sqlalchemy import or_

from app.database.connection import SessionLocal
from app.database.models import ProjectDB, ProjectPerformanceDB
from app.services.question_intent import (
    CATEGORY_ADMINISTRATIONS,
    PROJECT_CATEGORIES,
    STOP_WORDS,
)


def get_latest_performance(db, project_id):
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


def project_to_dict(db, project):
    performance = get_latest_performance(
        db,
        project.id,
    )

    return {
        "id": project.id,
        "administrative_code": project.administrative_code,
        "administrative_description": project.administrative_description,
        "project_description": project.project_description,
        "budget_year": project.budget_year,
        "original_budget": project.original_budget,

        "reporting_period": (
            performance.reporting_period
            if performance
            else None
        ),
        "period_performance": (
            performance.period_performance
            if performance
            else None
        ),
        "ytd_performance": (
            performance.ytd_performance
            if performance
            else None
        ),
        "performance_percentage": (
            performance.performance_percentage
            if performance
            else None
        ),
        "balance": (
            performance.balance
            if performance
            else None
        ),

        "source_id": (
            performance.source_id
            if performance
            else project.source_id
        ),
        "source_page": (
            performance.source_page
            if performance
            else project.source_page
        ),
    }


def find_projects(question: str):
    db = SessionLocal()

    try:
        words = re.findall(
            r"[a-z0-9]+(?:-[a-z0-9]+)?",
            question.lower(),
        )

        search_words = [
            word
            for word in words
            if len(word) >= 4 and word not in STOP_WORDS
        ]

        projects = (
            db.query(ProjectDB)
            .filter(ProjectDB.budget_year == 2026)
            .all()
        )

        scored_projects = []

        for project in projects:
            description = project.project_description.lower()

            description_words = set(
                re.findall(
                    r"[a-z0-9]+(?:-[a-z0-9]+)?",
                    description,
                )
            )

            expanded_description_words = set(
                description_words
            )

            for word in description_words:
                if "-" in word:
                    expanded_description_words.update(
                        part
                        for part in word.split("-")
                        if len(part) >= 4
                    )

            expanded_search_words = set(search_words)

            for word in search_words:
                if "-" in word:
                    expanded_search_words.update(
                        part
                        for part in word.split("-")
                        if len(part) >= 4
                    )

            matched_words = [
                word
                for word in expanded_search_words
                if word in expanded_description_words
            ]

            score = sum(
                len(word)
                for word in matched_words
            )

            if score > 0:
                scored_projects.append(
                    (score, project)
                )

        scored_projects.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            project_to_dict(db, project)
            for score, project in scored_projects
        ]

    finally:
        db.close()


def find_category_projects(category: str):
    db = SessionLocal()

    try:
        category_terms = PROJECT_CATEGORIES.get(
            category,
            [],
        )

        administration_terms = (
            CATEGORY_ADMINISTRATIONS.get(
                category,
                [],
            )
        )

        if not category_terms and not administration_terms:
            return []

        if administration_terms:
            administration_conditions = [
                ProjectDB.administrative_description.ilike(
                    f"%{administration}%"
                )
                for administration in administration_terms
            ]

            query = db.query(ProjectDB).filter(
                ProjectDB.budget_year == 2026,
                or_(*administration_conditions),
            )

            if category_terms:
                project_conditions = [
                    ProjectDB.project_description.ilike(
                        f"%{term}%"
                    )
                    for term in category_terms
                ]

                query = query.filter(
                    or_(*project_conditions)
                )

        else:
            project_conditions = [
                ProjectDB.project_description.ilike(
                    f"%{term}%"
                )
                for term in category_terms
            ]

            query = db.query(ProjectDB).filter(
                ProjectDB.budget_year == 2026,
                or_(*project_conditions),
            )

        projects = (
            query
            .order_by(ProjectDB.original_budget.desc())
            .all()
        )

        return [
            project_to_dict(db, project)
            for project in projects
        ]

    finally:
        db.close()


def find_ranked_category_projects(
    category: str,
    limit: int | None = None,
):
    db = SessionLocal()

    try:
        category_terms = PROJECT_CATEGORIES.get(
            category,
            [],
        )

        administration_terms = (
            CATEGORY_ADMINISTRATIONS.get(
                category,
                [],
            )
        )

        if not category_terms and not administration_terms:
            return []

        if administration_terms:
            administration_conditions = [
                ProjectDB.administrative_description.ilike(
                    f"%{administration}%"
                )
                for administration in administration_terms
            ]

            query = db.query(ProjectDB).filter(
                ProjectDB.budget_year == 2026,
                or_(*administration_conditions),
            )

            if category_terms:
                project_conditions = [
                    ProjectDB.project_description.ilike(
                        f"%{term}%"
                    )
                    for term in category_terms
                ]

                query = query.filter(
                    or_(*project_conditions)
                )

        else:
            project_conditions = [
                ProjectDB.project_description.ilike(
                    f"%{term}%"
                )
                for term in category_terms
            ]

            query = db.query(ProjectDB).filter(
                ProjectDB.budget_year == 2026,
                or_(*project_conditions),
            )

        query = query.order_by(
            ProjectDB.original_budget.desc()
        )

        if limit:
            query = query.limit(limit)

        projects = query.all()

        return [
            project_to_dict(db, project)
            for project in projects
        ]

    finally:
        db.close()


def find_ranked_projects(limit: int | None = None):
    db = SessionLocal()

    try:
        query = (
            db.query(ProjectDB)
            .filter(ProjectDB.budget_year == 2026)
            .order_by(ProjectDB.original_budget.desc())
        )

        if limit:
            query = query.limit(limit)

        projects = query.all()

        return [
            project_to_dict(db, project)
            for project in projects
        ]

    finally:
        db.close()