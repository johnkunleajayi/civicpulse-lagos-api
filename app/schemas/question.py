from pydantic import BaseModel

from app.schemas.evidence import EvidenceResponse


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    evidence: list[EvidenceResponse]