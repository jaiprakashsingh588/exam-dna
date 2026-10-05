import json
import time

from backend.app.services.ai_client import generate_text


def analyze_question(question: dict) -> dict:
    prompt = f"""
You are the ExamDNA historical GATE question analyzer.

Analyze this historical GATE CSE question.

Return ONLY valid JSON.
Keep every field concise.

Required JSON:
{{
  "core_concept": "string",
  "concepts": ["string"],
  "difficulty": "Easy|Medium|Hard",
  "question_pattern": "string",
  "trap_or_key_idea": "string",
  "preparation_priority": "Low|Medium|High"
}}

Do NOT predict future GATE questions.
Do NOT invent information.

Year: {question.get("year")}
Type: {question.get("question_type")}

Question:
{question.get("question_text", "")}

Options:
{question.get("options", [])}
"""

    last_error = None

    for attempt in range(2):
        try:
            text = generate_text(prompt).strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            required = [
                "core_concept",
                "concepts",
                "difficulty",
                "question_pattern",
                "trap_or_key_idea",
                "preparation_priority"
            ]

            if all(key in data for key in required):
                return data

            raise ValueError("Incomplete AI JSON response")

        except Exception as error:
            last_error = error
            if attempt == 0:
                time.sleep(2)

    return {
        "core_concept": "Unclassified",
        "concepts": [],
        "difficulty": "Unknown",
        "question_pattern": "Analysis unavailable",
        "trap_or_key_idea": str(last_error),
        "preparation_priority": "Unknown"
    }
