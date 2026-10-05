from typing import Any
import json
import time

from dotenv import load_dotenv

from backend.app.services.ai_client import generate_text

load_dotenv()


def parse_syllabus(raw_text: str) -> dict[str, Any]:
    prompt = f"""
Parse the following official GATE syllabus into structured JSON.

Rules:
- Return ONLY valid JSON.
- Do not invent topics.
- Preserve the meaning of the official syllabus.
- Group all syllabus content under the correct subject.
- Do not leave topics empty when the source contains topics.
- Include every subject present in the source text.

Required structure:
{{
  "exam": "GATE",
  "year": 2027,
  "paper": "Computer Science and Information Technology",
  "paper_code": "CS",
  "subjects": [
    {{
      "id": "string",
      "name": "string",
      "topics": ["string"]
    }}
  ]
}}

Official syllabus text:
{raw_text}
"""

    last_error = None

    for attempt in range(3):
        try:
            text = generate_text(prompt).strip()

            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            if not data.get("subjects"):
                raise ValueError("AI returned no subjects")

            if any(not subject.get("topics") for subject in data["subjects"]):
                raise ValueError("AI returned an empty topic list")

            return data

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(3)

    raise RuntimeError(f"AI syllabus parsing failed: {last_error}")


def save_syllabus(data: dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
