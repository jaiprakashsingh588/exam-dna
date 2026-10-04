from pathlib import Path
import json
import re

base = Path("data/questions/gate_2010_2023")
out = base / "parsed"
out.mkdir(exist_ok=True)

pattern = re.compile(
    r"(?ms)^Q\.?\s*(\d{1,2})\s+(.*?)(?=^Q\.?\s*\d{1,2}\s+|\Z)"
)

for raw in sorted(base.glob("*_raw.txt")):
    text = raw.read_text(encoding="utf-8", errors="ignore")
    questions = []

    for match in pattern.finditer(text):
        qno = int(match.group(1))
        body = match.group(2).strip()

        if 1 <= qno <= 100:
            questions.append({
                "question_number": qno,
                "question_text": body
            })

    output = out / f"{raw.stem.replace('_raw', '')}_questions.json"
    output.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"{raw.name}: {len(questions)} questions")

print("Parsing complete.")
