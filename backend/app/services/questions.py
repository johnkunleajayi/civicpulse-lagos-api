import re

from sqlalchemy import or_

from app.database.connection import SessionLocal
from app.database.models import BudgetSummaryDB, ProjectDB


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


PROJECT_CATEGORIES = {
    "rail": [
        "rail",
        "blueline",
        "blue line",
        "red line",
    ],
    "transport": [
        "transport",
        "traffic",
        "bus",
        "rail",
        "waterways",
        "waterway",
    ],
    "health": [
        "hospital",
        "health",
        "children hospital",
        "medical",
    ],
    "infrastructure": [
        "infrastructure",
        "expressway",
        "road",
    ],
    "agriculture": [
        "agriculture",
        "market hub",
        "produce hub",
        "wholesale market",
    ],
    "fire": [
        "fire",
        "rescue",
    ],
}


CATEGORY_ADMINISTRATIONS = {
    "rail": [
        "Lagos State Metropolitan Area Transport",
    ],
    "transport": [
        "Ministry of Transportation",
        "Lagos State Metropolitan Area Transport",
        "Lagos State Waterways Authority",
    ],
    "health": [
        "Ministry of Health",
    ],
    "infrastructure": [
        "Office of Infrastructure",
    ],
    "agriculture": [
        "Ministry of Agriculture Hqtrs",
    ],
    "fire": [
        "Fire Service",
    ],
}


def is_aggregate_question(question: str):
    question_lower = question.lower()

    aggregate_terms = [
        "total",
        "overall",
        "all projects",
        "capital expenditure",
        "capital spending",
        "capital budget",
        "percentage of the capital budget",
        "percent of the capital budget",
        "projects in q1",
        "projects in the first quarter",
    ]

    return any(
        term in question_lower
        for term in aggregate_terms
    )


def is_ranking_question(question: str):
    question_lower = question.lower()

    ranking_terms = [
        "highest budget",
        "highest budgets",
        "largest budget",
        "largest budgets",
        "biggest budget",
        "biggest budgets",
        "biggest projects",
        "biggest capital projects",
        "largest projects",
        "largest capital projects",
        "highest-funded",
        "highest funded",
        "most expensive",
    ]

    if any(
        term in question_lower
        for term in ranking_terms
    ):
        return True

    if re.search(
        r"\btop\s+\d+\b",
        question_lower,
    ):
        return True

    ranking_words = [
        "largest",
        "biggest",
        "highest",
        "most expensive",
    ]

    has_ranking_word = any(
        word in question_lower
        for word in ranking_words
    )

    has_project_word = any(
        word in question_lower
        for word in [
            "project",
            "projects",
        ]
    )

    return has_ranking_word and has_project_word


def extract_ranking_limit(question: str):
    question_lower = question.lower()

    match = re.search(
        r"\btop\s+(\d+)\b",
        question_lower,
    )

    if match:
        return int(match.group(1))

    return 10


def detect_project_category(question: str):
    question_lower = question.lower()

    db = SessionLocal()

    try:
        projects = (
            db.query(ProjectDB)
            .filter(ProjectDB.budget_year == 2026)
            .all()
        )

        question_words = {
            word
            for word in re.findall(
                r"[a-z0-9]+(?:-[a-z0-9]+)?",
                question_lower,
            )
            if len(word) >= 4 and word not in STOP_WORDS
        }

        for project in projects:
            description_lower = project.project_description.lower()

            project_words = {
                word
                for word in re.findall(
                    r"[a-z0-9]+(?:-[a-z0-9]+)?",
                    description_lower,
                )
                if len(word) >= 4
            }

            matched_words = question_words.intersection(
                project_words
            )

            if len(matched_words) >= 2:
                return None

        for category, terms in PROJECT_CATEGORIES.items():
            for term in terms:
                if term in question_lower:
                    return category

        return None

    finally:
        db.close()


def find_budget_summary(question: str):
    db = SessionLocal()

    try:
        summary = (
            db.query(BudgetSummaryDB)
            .filter(
                BudgetSummaryDB.budget_year == 2026,
                BudgetSummaryDB.reporting_period == "Q1 2026",
            )
            .first()
        )

        if not summary:
            return None

        return {
            "id": summary.id,
            "metric": summary.metric,
            "budget_year": summary.budget_year,
            "reporting_period": summary.reporting_period,
            "original_budget": summary.original_budget,
            "q1_performance": summary.q1_performance,
            "performance_percentage": summary.performance_percentage,
            "source_id": summary.source_id,
            "source_page": summary.source_page,
        }

    finally:
        db.close()


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


def find_category_projects(category: str):
    db = SessionLocal()

    try:
        category_terms = PROJECT_CATEGORIES.get(category, [])
        administration_terms = CATEGORY_ADMINISTRATIONS.get(
            category,
            [],
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

                query = query.filter(or_(*project_conditions))

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
        category_terms = PROJECT_CATEGORIES.get(category, [])
        administration_terms = CATEGORY_ADMINISTRATIONS.get(
            category,
            [],
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

                query = query.filter(or_(*project_conditions))

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
            for project in projects
        ]

    finally:
        db.close()


def generate_summary_answer(question: str, summary: dict):
    if not summary:
        return "I could not find verified Lagos State budget summary data for Q1 2026."

    question_lower = question.lower()

    if "percentage" in question_lower or "percent" in question_lower:
        return (
            f"Lagos State spent "
            f"{summary['performance_percentage']:.1f}% of its 2026 capital budget "
            f"in Q1 2026."
        )

    if "capital budget" in question_lower:
        return (
            f"Lagos State's total 2026 capital budget is "
            f"₦{summary['original_budget']:,.2f}."
        )

    amount = summary["q1_performance"]

    return (
        f"Lagos State recorded ₦{amount:,.2f} in total capital expenditure "
        f"for Q1 2026, representing "
        f"{summary['performance_percentage']:.1f}% of the "
        f"₦{summary['original_budget']:,.2f} capital budget."
    )


def generate_ranking_answer(
    question: str,
    projects: list[dict],
    category: str | None = None,
):
    if not projects:
        if category:
            return (
                f"I could not find verified Lagos State {category} "
                f"project data for 2026."
            )

        return "I could not find verified Lagos State project data for 2026."

    limit = extract_ranking_limit(question)

    if category:
        category_label = category

        if limit:
            heading = (
                f"The top {limit} Lagos State {category_label} "
                f"projects by 2026 budget are:"
            )
        else:
            heading = (
                f"The Lagos State {category_label} projects "
                f"with the highest 2026 budgets are:"
            )

    elif limit:
        heading = (
            f"The top {limit} Lagos State projects by 2026 budget are:"
        )

    else:
        heading = (
            "The Lagos State projects with the highest 2026 budgets are:"
        )

    lines = [heading]

    for index, project in enumerate(projects, start=1):
        lines.append(
            f"{index}. {project['project_description']} — "
            f"₦{project['original_budget']:,.2f}"
        )

    return "\n".join(lines)


def generate_category_answer(
    question: str,
    category: str,
    projects: list[dict],
):
    if not projects:
        return (
            f"I could not find verified Lagos State {category} "
            f"project data for 2026."
        )

    total_budget = sum(
        project["original_budget"]
        for project in projects
        if project["original_budget"] is not None
    )

    total_spending = sum(
        project["ytd_performance"]
        for project in projects
        if project["ytd_performance"] is not None
    )

    question_lower = question.lower()

    if "percentage" in question_lower or "percent" in question_lower:
        percentage = (
            (total_spending / total_budget) * 100
            if total_budget
            else 0
        )

        return (
            f"Lagos State spent {percentage:.1f}% of the verified "
            f"{category} project budget in Q1 2026."
        )

    if (
        "spend" in question_lower
        or "spent" in question_lower
        or "spending" in question_lower
        or "expenditure" in question_lower
        or "expenditures" in question_lower
        or "money went into" in question_lower
        or "performance" in question_lower
    ):
        lines = [
            f"Lagos State recorded ₦{total_spending:,.2f} in "
            f"expenditure across {len(projects)} verified "
            f"{category} projects in Q1 2026.",
            "",
            "Project breakdown:",
        ]

        for index, project in enumerate(projects, start=1):
            spending = project["ytd_performance"] or 0

            lines.append(
                f"{index}. {project['project_description']} — "
                f"₦{spending:,.2f}"
            )

        return "\n".join(lines)

    if "project" in question_lower and (
        "which" in question_lower
        or "what" in question_lower
        or "list" in question_lower
    ):
        lines = [
            f"I found {len(projects)} verified Lagos State "
            f"{category} projects in the 2026 budget:"
        ]

        for index, project in enumerate(projects, start=1):
            lines.append(
                f"{index}. {project['project_description']} — "
                f"₦{project['original_budget']:,.2f}"
            )

        return "\n".join(lines)

    return (
        f"Lagos State has ₦{total_budget:,.2f} budgeted across "
        f"{len(projects)} verified {category} projects in 2026."
    )


def generate_answer(question: str, projects: list[dict]):
    if not projects:
        return "I could not find a verified Lagos State project matching your question."

    project = projects[0]
    question_lower = question.lower()
    project_name = project["project_description"]

    if "percentage" in question_lower or "percent" in question_lower:
        percentage = project["performance_percentage"]

        return (
            f"{project_name} has used "
            f"{percentage:.1f}% of its original 2026 budget "
            f"as reported for Q1 2026."
        )

    if "spent" in question_lower or "performance" in question_lower:
        amount = project["ytd_performance"]

        return (
            f"{project_name} has recorded "
            f"₦{amount:,.2f} in 2026 year-to-date expenditure "
            f"as reported for Q1 2026."
        )

    if "left" in question_lower or "balance" in question_lower:
        amount = project["balance"]

        return (
            f"The remaining balance for {project_name} "
            f"is ₦{amount:,.2f} against its original 2026 budget."
        )

    budget = project["original_budget"]

    return (
        f"{project_name} has an original 2026 budget "
        f"of ₦{budget:,.2f}."
    )