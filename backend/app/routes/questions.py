from fastapi import APIRouter
import json
from pathlib import Path
import re

from backend.app.models.question import Question, Source

router = APIRouter(prefix="/questions", tags=["Questions"])

QUESTIONS_DIR = Path("data/questions")
FIXTURE_FILE = QUESTIONS_DIR / "example.json"


def normalize(item, file_path):
    if "question_text" not in item:
        item["question_text"] = item.get("raw_text", "")

    if "question_id" not in item:
        number = item.get("question_number", "unknown")
        item["question_id"] = f"{file_path.stem}_{number}"

    if "year" not in item:
        match = re.search(r"(20\d{2})", str(file_path))
        item["year"] = int(match.group(1)) if match else 0

    item.setdefault("subject", "Computer Science and Information Technology")
    item.setdefault("topic", "Unclassified")
    if item.get("topic") == "Unclassified":
        from backend.app.services.topic_classifier import classify_topic
        item["topic"] = classify_topic(item.get("question_text", ""), item.get("topic", ""))
    item.setdefault("question_type", "Unknown")
    item.setdefault("options", [])
    item.setdefault("correct_answer", None)
    item.setdefault("marks", 0)
    item.setdefault("difficulty", "Unknown")
    item.setdefault("concepts", [])
    item.setdefault("source", {"type": "historical_pyq"})

    return item


@router.get("/")
def get_questions():
    questions = []

    for file_path in sorted(QUESTIONS_DIR.rglob("*.json")):
        if file_path == FIXTURE_FILE:
            continue
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = [data]

            for item in data:
                if not isinstance(item, dict):
                    continue

                if "question_text" not in item and "raw_text" not in item:
                    continue

                try:
                    item = normalize(item, file_path)
                    question = Question(**item)
                    questions.append(question.model_dump())
                except Exception:
                    continue

        except Exception:
            continue

    return {
        "message": "Questions loaded successfully",
        "count": len(questions),
        "questions": questions
    }


@router.get("/stats")
def question_stats():
    data = get_questions()["questions"]

    years = {}
    subjects = {}
    types = {}

    for q in data:
        years[str(q["year"])] = years.get(str(q["year"]), 0) + 1
        subjects[q["subject"]] = subjects.get(q["subject"], 0) + 1
        types[q["question_type"]] = types.get(q["question_type"], 0) + 1

    return {
        "total_questions": len(data),
        "by_year": years,
        "by_subject": subjects,
        "by_question_type": types
    }


@router.get("/dna")
def question_dna():
    from backend.app.services.question_dna import build_question_dna

    questions = get_questions()["questions"]

    return build_question_dna(questions)


@router.get("/search")
def search_questions(
    year: int | None = None,
    question_type: str | None = None,
    subject: str | None = None,
    limit: int = 20
):
    questions = get_questions()["questions"]

    if year is not None:
        questions = [q for q in questions if q["year"] == year]

    if question_type is not None:
        questions = [
            q for q in questions
            if q["question_type"].lower() == question_type.lower()
        ]

    if subject is not None:
        questions = [
            q for q in questions
            if subject.lower() in q["subject"].lower()
        ]

    return {
        "count": len(questions),
        "questions": questions[:limit]
    }


@router.get("/areas")
def question_areas():
    from backend.app.services.weak_area import analyze_areas
    questions = get_questions()["questions"]
    return analyze_areas(questions)


@router.get("/{question_id}/analyze")
def analyze_question_by_id(question_id: str):
    from backend.app.services.question_analyzer import analyze_question

    questions = get_questions()["questions"]

    for question in questions:
        if question["question_id"] == question_id:
            return {
                "question_id": question_id,
                "analysis": analyze_question(question)
            }

    return {"error": "Question not found"}


@router.get("/intelligence")
def question_intelligence():
    from backend.app.services.question_dna import build_question_dna

    questions = get_questions()["questions"]
    dna = build_question_dna(questions)

    return {
        "total_questions": dna["total"],
        "year_distribution": dna["years"],
        "question_type_distribution": dna["types"],
        "subject_distribution": dna["subjects"],
        "topic_distribution": dna["topics"],
        "concept_distribution": dna["concepts"],
        "difficulty_distribution": dna["difficulty"],
        "preparation_priority": dna["priority"],
        "top_topics": dna["top_topics"],
        "top_concepts": dna["top_concepts"],
    }


@router.get("/{question_id}/similar")
def similar_questions(question_id: str, limit: int = 5):
    from backend.app.services.question_similarity import find_similar_questions

    questions = get_questions()["questions"]

    for question in questions:
        if question["question_id"] == question_id:
            return {
                "question_id": question_id,
                "similar_questions": find_similar_questions(
                    question,
                    questions,
                    limit
                )
            }

    return {"error": "Question not found"}


@router.get("/{question_id}/family")
def question_family(question_id: str):
    from backend.app.services.question_family import build_question_family

    questions = get_questions()["questions"]

    for question in questions:
        if question["question_id"] == question_id:
            return build_question_family(
                question,
                questions
            )

    return {"error": "Question not found"}


@router.get("/practice")
def adaptive_practice(
    topic: str | None = None,
    difficulty: str | None = None,
    question_type: str | None = None,
    limit: int = 10
):
    questions = get_questions()["questions"]

    if topic:
        questions = [
            q for q in questions
            if topic.lower() in q.get("topic", "").lower()
        ]

    if difficulty:
        questions = [
            q for q in questions
            if q.get("difficulty", "").lower() == difficulty.lower()
        ]

    if question_type:
        questions = [
            q for q in questions
            if q.get("question_type", "").lower() == question_type.lower()
        ]

    return {
        "count": min(len(questions), limit),
        "filters": {
            "topic": topic,
            "difficulty": difficulty,
            "question_type": question_type
        },
        "questions": questions[:limit]
    }


def question_areas():
    from backend.app.services.weak_area import analyze_areas

    questions = get_questions()["questions"]

    return analyze_areas(questions)


@router.get("/{question_id}/practice")
def generate_practice(question_id: str):
    from backend.app.services.practice_generator import generate_practice_variant

    questions = get_questions()["questions"]

    for question in questions:
        if question["question_id"] == question_id:
            return {
                "question_id": question_id,
                "practice_variant": generate_practice_variant(question)
            }

    return {"error": "Question not found"}
