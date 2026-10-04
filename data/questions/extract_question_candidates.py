from pathlib import Path
import re

base = Path("data/questions/gate_2010_2023_clean")
out = base / "question_candidates"
out.mkdir(exist_ok=True)

pattern = re.compile(
    r"(?im)^\s*(?:Q\.?\s*)?(\d{1,2})[\.\):\-]?\s+"
)

for raw in sorted(base.glob("*_ocr.txt")):
    text = raw.read_text(encoding="utf-8", errors="ignore")
    matches = list(pattern.finditer(text))

    candidates = []

    for i, match in enumerate(matches):
        qno = int(match.group(1))

        if not 1 <= qno <= 100:
            continue

        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        body = text[start:end].strip()

        if len(body) >= 30:
            candidates.append((qno, body))

    output = out / f"{raw.stem}_candidates.txt"

    with output.open("w", encoding="utf-8") as f:
        for qno, body in candidates:
            f.write(f"===== Q{qno} =====\n")
            f.write(body)
            f.write("\n\n")

    print(raw.name, "->", len(candidates), "candidates")

print("Candidate extraction complete.")
