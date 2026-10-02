from fastapi import APIRouter
import json
from pathlib import Path

from backend.app.models.question import Question

router = APIRouter(prefix="/questions", tags=["Questions"])

QUESTIONS_DIR = Path("data/questions")


@router.get("/")
def get_questions():
    questions = []

    for file_path in sorted(QUESTIONS_DIR.glob("*.json")):
        with file_path.open("r", encoding="utf-8") as file:
            question_data = json.load(file)

        question = Question(**question_data)
        questions.append(question.model_dump())

    return {
        "message": "Questions loaded successfully",
        "count": len(questions),
        "questions": questions
    }
