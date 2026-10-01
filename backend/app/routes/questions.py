from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(prefix="/questions", tags=["Questions"])

QUESTIONS_FILE = Path("data/questions/example.json")


@router.get("/")
def get_questions():
    with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
        question = json.load(file)

    return {
        "message": "Questions loaded successfully",
        "count": 1,
        "questions": [question]
    }
