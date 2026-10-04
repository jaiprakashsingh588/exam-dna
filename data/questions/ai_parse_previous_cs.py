from pathlib import Path
import json
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE = Path("data/questions/gate_2010_2023_clean")
OUT = BASE / "ai_parsed"
OUT.mkdir(exist_ok=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for source in sorted((BASE / "question_candidates").glob("*_candidates.txt")):
    output = OUT / f"{source.stem.replace('_candidates', '')}.json"

    if output.exists():
        print(f"SKIP {source.name}")
        continue

    text = source.read_text(encoding="utf-8", errors="ignore")

    prompt = f"""
You are parsing a historical GATE Computer Science question paper.

Convert the supplied OCR text into JSON.

Rules:
- Extract only questions actually present in the OCR.
- Do NOT invent missing text.
- Preserve question wording as closely as possible.
- Preserve all visible options.
- If OCR is unclear, use null rather than guessing.
- Do NOT determine or invent the correct answer.
- Identify question type only when clear: MCQ, MSQ, NAT, or null.
- Keep question number as an integer.

Return ONLY valid JSON in this format:

{{
  "questions": [
    {{
      "question_number": 1,
      "question_text": "...",
      "options": ["A", "B", "C", "D"],
      "question_type": "MCQ"
    }}
  ]
}}

OCR text:
{text}
"""

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            result = response.text.strip()

            if result.startswith("```"):
                result = result.replace("```json", "").replace("```", "").strip()

            data = json.loads(result)

            if "questions" not in data:
                raise ValueError("Missing questions field")

            output.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            print(f"DONE {source.name} -> {len(data['questions'])} questions")
            break

        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(3)
    else:
        print(f"ERROR {source.name}: {last_error}")

print("AI parsing complete.")
