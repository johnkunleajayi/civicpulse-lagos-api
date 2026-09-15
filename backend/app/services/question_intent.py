import re

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
    "project",
    "projects",
    "cost",
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
        "lagos budget 2026",
        "lagos state budget 2026",
        "lagos 2026 budget",
        "lagos state 2026 budget",
        "2026 lagos budget",
        "2026 lagos state budget",
    ]

    return any(
        term in question_lower
        for term in aggregate_terms
    )


def is_out_of_scope_question(question: str):
    question_lower = question.lower()

    historical_terms = [
        "since 1999",
        "from 1999",
        "after 1999",
        "before 2026",
        "before 2025",
        "historical",
        "history of",
        "over the years",
        "past projects",
        "previous projects",
        "projects since",
        "projects from",
    ]

    if any(
        term in question_lower
        for term in historical_terms
    ):
        return True

    year_matches = re.findall(
        r"\b(19\d{2}|20\d{2})\b",
        question_lower,
    )

    for year in year_matches:
        if int(year) != 2026:
            return True

    return False


def has_information_intent(question: str):
    question_lower = question.lower()

    information_terms = [
        "budget",
        "cost",
        "funding",
        "funded",
        "allocated",
        "allocation",
        "spent",
        "spending",
        "expenditure",
        "balance",
        "remaining",
        "left",
        "performance",
        "progress",
        "percentage",
        "percent",
        "rate",
        "q1",
        "first quarter",
        "how much",
        "how many",
        "which projects",
        "what projects",
        "list projects",
        "show projects",
    ]

    return any(
        term in question_lower
        for term in information_terms
    )


def is_underspecified_question(question: str):
    question_lower = question.lower().strip()

    normalized_question = re.sub(
        r"[^\w\s]",
        " ",
        question_lower,
    )

    words = normalized_question.split()

    if not words:
        return True

    if is_ranking_question(question):
        return False

    if is_aggregate_question(question):
        return False

    if len(words) <= 2:
        meaningful_words = [
            word
            for word in words
            if word not in STOP_WORDS
            and not re.fullmatch(r"\d{4}", word)
        ]

        if (
            "lagos" in words
            or "lagos state" in question_lower
            or "2026" in words
        ):
            if not any(
                term in question_lower
                for terms in PROJECT_CATEGORIES.values()
                for term in terms
            ):
                return True

        if not meaningful_words:
            return True

    broad_terms = [
        "lagos budget",
        "lagos state budget",
        "lagos 2026",
        "lagos state 2026",
        "lagos 2026 budget",
        "lagos state 2026 budget",
        "2026 budget",
        "2026 projects",
    ]

    if question_lower in broad_terms:
        return True

    if (
        "lagos" in words
        and "2026" in words
        and "budget" in words
    ):
        has_category_reference = any(
            term in question_lower
            for terms in PROJECT_CATEGORIES.values()
            for term in terms
        )

        if not has_category_reference:
            return True

    if not has_information_intent(question):
        has_category_reference = any(
            term in question_lower
            for terms in PROJECT_CATEGORIES.values()
            for term in terms
        )

        if has_category_reference:
            return True

        if len(words) <= 2:
            return True

    return False


def generate_underspecified_answer(question: str):
    return (
        "I can help with verified Lagos State information from the "
        "2026 budget and Q1 2026 Budget Performance Report. "
        "Could you be more specific? For example, you can ask about "
        "a project's budget, Q1 spending, remaining balance, or the "
        "largest projects."
    )


def generate_scope_answer(question: str):
    return (
        "I can currently verify Lagos State project information "
        "from the 2026 budget and Q1 2026 Budget Performance Report. "
        "I don't have verified evidence covering the historical period "
        "asked about in this question."
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