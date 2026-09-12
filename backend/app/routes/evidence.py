from fastapi import APIRouter, HTTPException

from app.schemas.evidence import EvidenceResponse
from app.services.evidence import get_project_evidence


router = APIRouter(
    prefix="/evidence",
    tags=["Evidence"],
)


@router.get(
    "/projects/{project_id}",
    response_model=EvidenceResponse,
)
def get_project_evidence_endpoint(project_id: int):
    evidence = get_project_evidence(project_id)

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail="Project evidence not found",
        )

    return evidence