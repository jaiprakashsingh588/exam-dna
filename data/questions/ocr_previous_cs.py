from pathlib import Path
import subprocess

base = Path("data/questions/gate_2010_2023_clean")

for pdf in sorted(base.glob("*.pdf")):
    output = base / f"{pdf.stem}_ocr.txt"

    if output.exists():
        print(f"SKIP {pdf.name}")
        continue

    print(f"OCR {pdf.name}...")

    prefix = base / f".ocr_{pdf.stem}"

    subprocess.run([
        "pdftoppm",
        "-jpeg",
        "-r", "200",
        str(pdf),
        str(prefix)
    ], check=True)

    pages = sorted(base.glob(f".ocr_{pdf.stem}-*.jpg"))

    with output.open("w", encoding="utf-8") as out:
        for i, page in enumerate(pages, 1):
            print(f"  page {i}/{len(pages)}")
            result = subprocess.run(
                ["tesseract", str(page), "stdout"],
                capture_output=True,
                text=True
            )
            out.write(result.stdout)
            out.write("\n")

            page.unlink()

    print(f"DONE {pdf.name}")

print("OCR complete.")
