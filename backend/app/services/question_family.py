from collections import defaultdict

from backend.app.services.question_similarity import (
    find_similar_questions,
)


def build_question_family(
    target: dict,
    questions: list[dict],
    threshold: float = 0.20,
) -> dict:
    similar = find_similar_questions(
        target,
        questions,
        limit=20,
    )

    family = [
        question
        for question in similar
        if question["similarity"] >= threshold
    ]

    return {
        "question_id": target.get("question_id"),
        "topic": target.get("topic"),
        "family_size": len(family) + 1,
        "members": [
            {
                "question_id": target.get("question_id"),
                "year": target.get("year"),
                "similarity": 1.0,
            }
        ] + [
            {
                "question_id": question["question_id"],
                "year": question["year"],
                "similarity": question["similarity"],
            }
            for question in family
        ],
    }
