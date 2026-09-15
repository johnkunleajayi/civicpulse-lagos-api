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
    "waterways": [
        "waterways",
        "waterway",
        "water transport",
    ],
    "transport": [
        "transport",
        "traffic",
        "bus",
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
    "waterways": [
        "Lagos State Waterways Authority",
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


SUGGESTION_TOPICS = {
    "budget": [
        "What is Lagos State's 2026 capital budget?",
        "What is the total Lagos State budget for 2026?",
        "How much was allocated to capital projects in 2026?",
        "How much has Lagos spent on capital projects?",
        "What percentage of the capital budget has been spent?",
        "What are the largest Lagos State projects by 2026 budget?",
        "Which Lagos State projects received the most funding?",
        "How much was budgeted for transport projects?",
        "How much was budgeted for health projects?",
        "How much was budgeted for waterways projects?",
    ],
    "spending": [
        "How much has Lagos spent on capital projects?",
        "What percentage of the capital budget has been spent?",
        "How much has Lagos spent on waterways?",
        "How much has Lagos spent on health projects?",
        "How much has Lagos spent on transport projects?",
        "How much has Lagos spent on rail projects?",
        "How much has Lagos spent on infrastructure projects?",
        "Which health projects have received the most spending?",
        "Which transport projects have received the most spending?",
        "Which projects have the highest year-to-date expenditure?",
    ],
    "projects": [
        "What are the largest Lagos State projects by 2026 budget?",
        "Which Lagos State projects have the highest budgets?",
        "What waterways projects are in the 2026 budget?",
        "What health projects are in the 2026 budget?",
        "What transport projects are in the 2026 budget?",
        "What rail projects are in the 2026 budget?",
        "What infrastructure projects are in the 2026 budget?",
        "What agriculture projects are in the 2026 budget?",
        "Which projects have received the most spending?",
        "How much was budgeted for a specific project?",
    ],
    "health": [
        "How much was budgeted for health projects?",
        "How much has Lagos spent on health projects?",
        "What percentage of the health project budget was spent?",
        "What are the largest health projects by 2026 budget?",
        "Which health projects received the most funding?",
        "Which health projects have the highest spending?",
        "How much was budgeted for Ojo General Hospital?",
        "How much has been spent on Ojo General Hospital?",
        "How much was budgeted for Shomolu General Hospital?",
        "How much has been spent on Shomolu General Hospital?",
    ],
    "waterways": [
        "How much has Lagos spent on waterways?",
        "What waterways projects are in the 2026 budget?",
        "How much was budgeted for waterways projects?",
        "What percentage of the waterways project budget was spent?",
        "Which waterways projects have the highest budgets?",
        "Which waterways projects have received the most spending?",
        "How much was budgeted for Omi-Eko?",
        "How much has been spent on Omi-Eko?",
        "How much was budgeted for the Lekki-Epe water transport project?",
        "How much has been spent on the Lekki-Epe water transport project?",
    ],
    "transport": [
        "How much was budgeted for transport projects?",
        "How much has Lagos spent on transport projects?",
        "What percentage of the transport project budget was spent?",
        "What are the largest transport projects?",
        "Which transport projects have the highest budgets?",
        "Which transport projects have received the most spending?",
        "How much was budgeted for rail projects?",
        "How much has Lagos spent on rail projects?",
        "How much was budgeted for waterways projects?",
        "How much has Lagos spent on waterways?",
    ],
    "rail": [
        "How much was budgeted for rail projects?",
        "How much has Lagos spent on rail projects?",
        "What percentage of the rail project budget was spent?",
        "What are the largest rail projects?",
        "Which rail projects have the highest budgets?",
        "Which rail projects have received the most spending?",
        "How much was budgeted for the Blue Line?",
        "How much was budgeted for the Red Line?",
        "How much has been spent on the Blue Line?",
        "How much has been spent on the Red Line?",
    ],
    "infrastructure": [
        "How much was budgeted for infrastructure projects?",
        "How much has Lagos spent on infrastructure projects?",
        "What percentage of the infrastructure project budget was spent?",
        "What are the largest infrastructure projects?",
        "Which infrastructure projects have the highest budgets?",
        "Which infrastructure projects have received the most spending?",
        "How much was budgeted for road projects?",
        "How much has Lagos spent on road projects?",
        "Which road projects have the highest budgets?",
        "Which infrastructure projects have the highest year-to-date expenditure?",
    ],
    "agriculture": [
        "How much was budgeted for agriculture projects?",
        "How much has Lagos spent on agriculture projects?",
        "What percentage of the agriculture project budget was spent?",
        "What are the largest agriculture projects?",
        "Which agriculture projects have the highest budgets?",
        "Which agriculture projects have received the most spending?",
        "How much was budgeted for market hub projects?",
        "How much has Lagos spent on market hub projects?",
        "Which agriculture projects have the highest year-to-date expenditure?",
        "What agriculture projects are included in the 2026 budget?",
    ],
    "fire": [
        "How much was budgeted for fire and rescue projects?",
        "How much has Lagos spent on fire and rescue projects?",
        "What percentage of the fire project budget was spent?",
        "What are the largest fire and rescue projects?",
        "Which fire projects have the highest budgets?",
        "Which fire projects have received the most spending?",
        "How much was budgeted for fire service projects?",
        "How much has Lagos spent on fire service projects?",
        "Which fire projects have the highest year-to-date expenditure?",
        "What fire and rescue projects are included in the 2026 budget?",
    ],
}


GENERAL_SUGGESTIONS = [
    "What is Lagos State's 2026 capital budget?",
    "How much has Lagos spent on capital projects?",
    "What percentage of the capital budget has been spent?",
    "What are the largest Lagos State projects by 2026 budget?",
    "How much has Lagos spent on waterways?",
    "How much has Lagos spent on health projects?",
    "How much has Lagos spent on transport projects?",
    "What are the largest rail projects?",
    "Which infrastructure projects have the highest budgets?",
    "How much was budgeted for a specific project?",
]


def is_aggregate_question(question: str):
    question_lower = question.lower()

    aggregate_terms = [
        "overall budget",
        "total budget",
        "total capital expenditure",
        "total capital spending",
        "total capital budget",
        "overall capital expenditure",
        "overall capital spending",
        "overall capital budget",
        "all projects",
        "capital expenditure",
        "capital spending",
        "capital budget",
        "capital projects",
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
        "q2",
        "second quarter",
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


def has_project_category_reference(question: str):
    question_lower = question.lower()

    return any(
        term in question_lower
        for terms in PROJECT_CATEGORIES.values()
        for term in terms
    )


def detect_clarification_topic(question: str):
    question_lower = question.lower()

    topic_priority = [
        "waterways",
        "health",
        "rail",
        "transport",
        "infrastructure",
        "agriculture",
        "fire",
        "budget",
        "spending",
        "projects",
    ]

    for topic in topic_priority:
        if topic in question_lower:
            return topic

    if "spent" in question_lower:
        return "spending"

    if "expenditure" in question_lower:
        return "spending"

    if "budgeted" in question_lower:
        return "budget"

    return None


def is_ambiguous_spending_question(question: str):
    question_lower = question.lower().strip()

    spending_terms = [
        "spent",
        "spend",
        "spending",
        "expenditure",
        "expenditures",
        "money spent",
        "money used",
        "funds spent",
        "funds used",
    ]

    has_spending_term = any(
        term in question_lower
        for term in spending_terms
    )

    if not has_spending_term:
        return False

    # If the question explicitly identifies a category,
    # administration, project type, or reporting period,
    # it has enough scope to answer.
    if has_project_category_reference(question):
        return False

    specific_scope_terms = [
        "capital expenditure",
        "capital spending",
        "capital projects",
        "capital budget",
        "budget",
        "project",
        "projects",
        "health",
        "hospital",
        "transport",
        "rail",
        "waterways",
        "waterway",
        "agriculture",
        "fire",
        "infrastructure",
        "road",
        "expressway",
        "q1",
        "q2",
        "first quarter",
        "second quarter",
    ]

    if any(
        term in question_lower
        for term in specific_scope_terms
    ):
        return False

    # A question that says "spent on [something]" has
    # identified a specific subject, even when that subject
    # is not one of our predefined categories.
    if re.search(
        r"\b(?:spent|spending|expenditure|expenditures)\b"
        r".*\bon\s+\S+",
        question_lower,
    ):
        return False

    # Broad Lagos spending questions that mention Lagos
    # but do not identify what the spending relates to
    # should be clarified.
    if "lagos" in question_lower:
        return True

    # Broad spending questions that mention Lagos State but
    # do not identify what the spending relates to should be
    # clarified.
    broad_spending_patterns = [
        r"\bhow much has lagos\b",
        r"\bhow much did lagos\b",
        r"\bwhat has lagos\b",
        r"\bwhat did lagos\b",
        r"\bhow much money has lagos\b",
        r"\bhow much money did lagos\b",
        r"\bhow much has lagos state\b",
        r"\bhow much did lagos state\b",
        r"\bhow much money has lagos state\b",
        r"\bhow much money did lagos state\b",
    ]

    if any(
        re.search(pattern, question_lower)
        for pattern in broad_spending_patterns
    ):
        return True

    return False


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

    incomplete_question_patterns = [
        r"^how much has lagos$",
        r"^how much did lagos$",
        r"^how much has lagos state$",
        r"^how much did lagos state$",
        r"^what has lagos$",
        r"^what did lagos$",
        r"^what has lagos state$",
        r"^what did lagos state$",
    ]

    if any(
        re.search(pattern, question_lower)
        for pattern in incomplete_question_patterns
    ):
        return True

    if is_ambiguous_spending_question(question):
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
            if not has_project_category_reference(question):
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
        "lagos spending",
        "lagos state spending",
        "lagos expenditure",
        "lagos state expenditure",
        "lagos projects",
        "lagos state projects",
        "tell me about lagos",
        "tell me about lagos budget",
        "tell me about lagos spending",
        "tell me about lagos projects",
    ]

    if question_lower in broad_terms:
        return True

    if (
        "lagos" in words
        and "2026" in words
        and "budget" in words
    ):
        has_category_reference = has_project_category_reference(
            question
        )

        if not has_category_reference:
            return True

    if not has_information_intent(question):
        has_category_reference = has_project_category_reference(
            question
        )

        if has_category_reference:
            return True

        return True

    broad_question_patterns = [
        r"^tell me about .+$",
        r"^what can you tell me about .+$",
        r"^give me information about .+$",
        r"^show me information about .+$",
        r"^what about .+$",
    ]

    if any(
        re.search(pattern, question_lower)
        for pattern in broad_question_patterns
    ):
        if not is_ranking_question(question):
            if not has_information_intent(question):
                return True

    return False


def generate_underspecified_answer(question: str):
    topic = detect_clarification_topic(question)

    if topic and topic in SUGGESTION_TOPICS:
        suggestions = SUGGESTION_TOPICS[topic]

        topic_labels = {
            "budget": "Lagos's 2026 budget",
            "spending": "Lagos State spending",
            "projects": "Lagos State projects",
            "health": "health projects",
            "waterways": "waterways projects",
            "transport": "transport projects",
            "rail": "rail projects",
            "infrastructure": "infrastructure projects",
            "agriculture": "agriculture projects",
            "fire": "fire and rescue projects",
        }

        topic_label = topic_labels.get(
            topic,
            "Lagos State public information",
        )

        lines = [
            f"I can help you explore verified information about "
            f"{topic_label}, but I need to know what you would like "
            f"to find out.",
            "",
            "Here are some questions CivicPulse can answer:",
        ]

        for index, suggestion in enumerate(
            suggestions[:10],
            start=1,
        ):
            lines.append(
                f"{index}. {suggestion}"
            )

        return "\n".join(lines)

    lines = [
        "I can help you explore verified Lagos State budget and "
        "project information, but I need a little more detail.",
        "",
        "Here are some questions CivicPulse can answer:",
    ]

    for index, suggestion in enumerate(
        GENERAL_SUGGESTIONS[:10],
        start=1,
    ):
        lines.append(
            f"{index}. {suggestion}"
        )

    return "\n".join(lines)


def generate_scope_answer(question: str):
    return (
        "I can currently verify Lagos State project information "
        "from the 2026 budget and Q2 2026 Budget Performance Report. "
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

    for category, terms in PROJECT_CATEGORIES.items():
        for term in terms:
            if term in question_lower:
                return category

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

        return None

    finally:
        db.close()