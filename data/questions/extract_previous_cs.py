from pathlib import Path
from pypdf import PdfReader

base = Path("data/questions/gate_2010_2023")

pdfs = sorted(base.glob("*.pdf"))

print("PDFs found:", len(pdfs))

for pdf in pdfs:
    try:
        reader = PdfReader(str(pdf))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        output = pdf.with_name(pdf.stem + "_raw.txt")
        output.write_text(text, encoding="utf-8")

        print(f"{pdf.name}: {len(reader.pages)} pages -> {len(text)} chars")

    except Exception as e:
        print(f"ERROR {pdf.name}: {e}")

print("Extraction complete.")
