from pathlib import Path
import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

source = Path("data/questions/gate_2010_2023_clean/question_candidates/CS2010_ocr_candidates.txt")
text = source.read_text(encoding="utf-8")

start = text.find("===== Q1 =====")
end = text.find("===== Q6 =====")

chunk = text[start:end]

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = f"""
Parse these historical GATE CS questions into JSON.

Rules:
- Extract only questions present in the text.
- Do not invent missing information.
- Preserve OCR wording as much as possible.
- Do not determine correct answers.
- If options are unclear, use an empty list.
- question_type must be MCQ, MSQ, NAT, or null.

Return ONLY valid JSON:

{{
  "questions": [
    {{
      "question_number": 1,
      "question_text": "...",
      "options": [],
      "question_type": null
    }}
  ]
}}

TEXT:
{chunk}
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)

result = response.text.strip()

if result.startswith("```"):
    result = result.replace("```json", "").replace("```", "").strip()

data = json.loads(result)

output = Path("data/questions/gate_2010_2023_clean/ai_parsed_test.json")
output.parent.mkdir(exist_ok=True)
output.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Questions parsed:", len(data["questions"]))
print("Saved:", output)
