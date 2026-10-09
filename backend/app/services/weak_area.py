from collections import Counter


def analyze_areas(questions: list[dict]) -> dict:
    topic_counts = Counter(
        q.get("topic", "Unclassified")
        for q in questions
        if q.get("topic") != "Unclassified"
    )

    difficulty_counts = Counter(
        q.get("difficulty", "Unknown")
        for q in questions
    )

    return {
        "topic_strength": dict(topic_counts),
        "difficulty_distribution": dict(difficulty_counts),
        "total_analyzed": len(questions),
    }
