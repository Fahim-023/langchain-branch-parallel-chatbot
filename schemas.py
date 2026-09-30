from pydantic import BaseModel, Field
from typing import List


class ResponseSchema(BaseModel):
    answer: str = Field(description="A short answer for the subject")
    summary: str = Field(description="A short summary for the subject")
    confidence: int = Field(description="Rating from 1 to 10")
    category: str = Field(description="The category of the query: Programming, Mathematics, or General")
    keywords: List[str] = Field(description="List of relevant tags")