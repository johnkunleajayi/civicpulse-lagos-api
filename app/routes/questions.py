from fastapi import APIRouter

from app.schemas.question import QuestionRequest, QuestionResponse
from app.services.evidence import get_project_evidence
from app.services.questions import find_projects, generate_answer


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post("/", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    projects = find_projects(request.question)
    answer = generate_answer(request.question, projects)

    evidence = []

    if projects:
        project_evidence = get_project_evidence(projects[0]["id"])

        if project_evidence:
            evidence.append(project_evidence)

    return {
        "question": request.question,
        "answer": answer,
        "evidence": evidence,
    }