from pydantic import BaseModel
from datetime import date


class Source(BaseModel):
    title: str
    publisher: str
    publication_date: date
    reporting_period: str
    document_type: str
    url: str