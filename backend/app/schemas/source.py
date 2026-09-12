from datetime import date

from pydantic import BaseModel


class SourceResponse(BaseModel):
    id: int

    title: str
    publisher: str
    publication_date: date
    reporting_period: str
    document_type: str
    url: str