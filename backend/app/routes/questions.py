from fastapi import APIRouter

from app.schemas.question import QuestionRequest, QuestionResponse
from app.services.evidence import get_project_evidence
from app.services.questions import (
    detect_project_category,
    extract_ranking_limit,
    find_budget_summary,
    find_category_projects,
    find_projects,
    find_ranked_category_projects,
    find_ranked_projects,
    generate_answer,
    generate_category_answer,
    generate_ranking_answer,
    generate_summary_answer,
    is_aggregate_question,
    is_ranking_question,
)
from app.services.summaries import get_budget_summary_evidence


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post("/", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    category = detect_project_category(request.question)

    if is_ranking_question(request.question):
        limit = extract_ranking_limit(request.question)

        if category:
            projects = find_ranked_category_projects(
                category,
                limit,
            )

            answer = generate_ranking_answer(
                request.question,
                projects,
                category,
            )
        else:
            projects = find_ranked_projects(limit)

            answer = generate_ranking_answer(
                request.question,
                projects,
            )

        evidence = []

        for project in projects:
            project_evidence = get_project_evidence(project["id"])

            if project_evidence:
                evidence.append(project_evidence)

        return {
            "question": request.question,
            "answer": answer,
            "evidence": evidence,
        }

    if category:
        projects = find_category_projects(category)

        answer = generate_category_answer(
            request.question,
            category,
            projects,
        )

        evidence = []

        for project in projects:
            project_evidence = get_project_evidence(project["id"])

            if project_evidence:
                evidence.append(project_evidence)

        return {
            "question": request.question,
            "answer": answer,
            "evidence": evidence,
        }

    if is_aggregate_question(request.question):
        summary = find_budget_summary(request.question)

        answer = generate_summary_answer(
            request.question,
            summary,
        )

        evidence = []

        if summary:
            summary_evidence = get_budget_summary_evidence(
                summary["id"]
            )

            if summary_evidence:
                evidence.append(summary_evidence)

        return {
            "question": request.question,
            "answer": answer,
            "evidence": evidence,
        }

    projects = find_projects(request.question)

    answer = generate_answer(
        request.question,
        projects,
    )

    evidence = []

    if projects:
        project_evidence = get_project_evidence(
            projects[0]["id"]
        )

        if project_evidence:
            evidence.append(project_evidence)

    return {
        "question": request.question,
        "answer": answer,
        "evidence": evidence,
    }