from collections import Counter


def build_question_dna(questions: list[dict]) -> dict:
    if not questions:
        return {
            "total": 0,
            "years": {},
            "types": {},
            "subjects": {},
            "marks": {}
        }

    return {
        "total": len(questions),
        "years": dict(Counter(str(q["year"]) for q in questions)),
        "types": dict(Counter(q["question_type"] for q in questions)),
        "subjects": dict(Counter(q["subject"] for q in questions)),
        "marks": dict(Counter(str(q["marks"]) for q in questions)),
    }
