from collections import Counter


def build_question_dna(questions: list[dict]) -> dict:
    if not questions:
        return {
            "total": 0,
            "years": {},
            "types": {},
            "subjects": {},
            "topics": {},
            "concepts": {},
            "difficulty": {},
            "priority": {},
            "marks": {},
        }

    year_counts = Counter(str(q.get("year", "Unknown")) for q in questions)
    type_counts = Counter(q.get("question_type", "Unknown") for q in questions)
    subject_counts = Counter(q.get("subject", "Unknown") for q in questions)
    topic_counts = Counter(q.get("topic", "Unknown") for q in questions)
    difficulty_counts = Counter(q.get("difficulty", "Unknown") for q in questions)
    priority_counts = Counter(
        q.get("preparation_priority", "Unknown") for q in questions
    )
    marks_counts = Counter(str(q.get("marks", 0)) for q in questions)

    concept_counts = Counter()

    for question in questions:
        concepts = question.get("concepts", [])

        if isinstance(concepts, list):
            for concept in concepts:
                if concept:
                    concept_counts[str(concept)] += 1

    return {
        "total": len(questions),
        "years": dict(year_counts),
        "types": dict(type_counts),
        "subjects": dict(subject_counts),
        "topics": dict(topic_counts),
        "concepts": dict(concept_counts),
        "difficulty": dict(difficulty_counts),
        "priority": dict(priority_counts),
        "marks": dict(marks_counts),
        "top_topics": [(topic, count) for topic, count in topic_counts.most_common() if topic != "Unclassified"][:10],
        "top_concepts": concept_counts.most_common(20),
    }
