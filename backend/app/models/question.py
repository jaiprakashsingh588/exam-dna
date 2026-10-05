from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    type: str = "historical_pyq"
    url: Optional[str] = None


class Question(BaseModel):
    question_id: str
    year: int
    subject: str = "Computer Science and Information Technology"
    topic: str = "Unclassified"
    question_type: str = "Unknown"
    question_text: str
    options: list[str] = []
    correct_answer: Optional[str] = None
    marks: float = 0
    difficulty: str = "Unknown"
    concepts: list[str] = []
    source: Source = Source()
