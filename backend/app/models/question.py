from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    type: str
    url: Optional[str] = None


class Question(BaseModel):
    question_id: str
    year: int
    subject: str
    topic: str
    question_type: str
    question_text: str
    options: list[str]
    correct_answer: str
    marks: float
    difficulty: str
    concepts: list[str]
    source: Source
