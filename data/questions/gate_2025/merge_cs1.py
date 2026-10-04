import json
import re
from pathlib import Path

base = Path("data/questions/gate_2025")

questions = json.loads(
    (base / "CS1_questions.json").read_text(encoding="utf-8")
)

text = (base / "CS1_Keys_raw.txt").read_text(encoding="utf-8")

pattern = re.compile(
    r"(?m)^(\d{1,2})\n"
    r"1\n"
    r"(MCQ|MSQ|NAT)\n"
    r"(GA|CS-1)\n"
    r"(.+)\n"
    r"(1|2)$"
)

rows = []

for match in pattern.finditer(text):
    qno = int(match.group(1))

    if 1 <= qno <= 65:
        rows.append({
            "question_number": qno,
            "session": 1,
            "question_type": match.group(2),
            "section": match.group(3),
            "correct_answer": match.group(4),
            "marks": float(match.group(5))
        })

rows = sorted(rows, key=lambda x: x["question_number"])

assert len(rows) == 65, f"Expected 65 answers, got {len(rows)}"

expected = list(range(1, 66))
actual = [r["question_number"] for r in rows]

assert actual == expected, f"Question numbering mismatch: {actual}"

for question, answer in zip(questions, rows):
    question.update({
        "session": answer["session"],
        "question_type": answer["question_type"],
        "section": answer["section"],
        "correct_answer": answer["correct_answer"],
        "marks": answer["marks"]
    })

(base / "CS1_questions.json").write_text(
    json.dumps(questions, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Merged questions:", len(questions))
print("Answers:", len(rows))
print("Missing:", 65 - len(rows))
print("Total marks:", sum(q["marks"] for q in questions))
