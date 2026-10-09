import json

from backend.app.services.ai_client import generate_text


def generate_practice_variant(question: dict) -> dict:
    prompt = f"""
Create ONE GATE CSE practice question inspired by this historical question.

Do not reproduce the original question verbatim.
Do not predict any future GATE paper.
Keep the same underlying concept but change the values or scenario.

Return ONLY valid JSON:
{{
  "question_text": "string",
  "options": ["string"],
  "correct_answer": "string",
  "concept": "string",
  "difficulty": "Easy|Medium|Hard"
}}

Historical question:
{question.get("question_text", "")}

Options:
{question.get("options", [])}
"""

    text = generate_text(prompt).strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)
