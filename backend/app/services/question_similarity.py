import re


STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and", "or",
    "of", "to", "in", "on", "for", "with", "by", "from", "that",
    "this", "which", "what", "following", "using", "used"
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    }


def similarity_score(question_a: dict, question_b: dict) -> float:
    words_a = tokenize(question_a.get("question_text", ""))
    words_b = tokenize(question_b.get("question_text", ""))

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    score = len(intersection) / len(union)

    if question_a.get("topic") == question_b.get("topic"):
        score += 0.2

    return min(round(score, 3), 1.0)


def find_similar_questions(
    target: dict,
    questions: list[dict],
    limit: int = 5
) -> list[dict]:
    results = []

    for question in questions:
        if question.get("question_id") == target.get("question_id"):
            continue

        score = similarity_score(target, question)

        if score > 0:
            results.append({
                "question_id": question.get("question_id"),
                "year": question.get("year"),
                "topic": question.get("topic"),
                "similarity": score,
                "question_text": question.get("question_text", "")
            })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:limit]
