from backend.app.services.ai_client import generate_text


def analyze_question(question: dict) -> str:
    prompt = f"""
Analyze this historical GATE CSE question for ExamDNA.

Return concise JSON with:
- core_concept
- concepts
- difficulty
- question_pattern
- trap_or_key_idea
- preparation_priority

Do not predict any future GATE question.

Question:
{question.get("question_text", "")}

Options:
{question.get("options", [])}

Year:
{question.get("year")}

Existing topic:
{question.get("topic")}
"""

    return generate_text(prompt)
