from pathlib import Path
import json

base = Path("data/questions/gate_2010_2023_clean")

papers = [
    ("CS2010.pdf", 2010, "CS"),
    ("CS2011.pdf", 2011, "CS"),
    ("CS2012.pdf", 2012, "CS"),
    ("CS2013.pdf", 2013, "CS"),
    ("CS2014.pdf", 2014, "CS"),
    ("CS2015.pdf", 2015, "CS"),
    ("CS2016.pdf", 2016, "CS"),
    ("CS1-2017.pdf", 2017, "CS-1"),
    ("CS2-2017.pdf", 2017, "CS-2"),
    ("CS2018.pdf", 2018, "CS"),
    ("CS2019.pdf", 2019, "CS"),
    ("CS2020.pdf", 2020, "CS"),
    ("CS1-2021.pdf", 2021, "CS-1"),
    ("CS2-2021.pdf", 2021, "CS-2"),
    ("CS2022.pdf", 2022, "CS"),
    ("CS2023.pdf", 2023, "CS"),
]

manifest = []

for filename, year, paper in papers:
    pdf = base / filename
    ocr = base / f"{pdf.stem}_ocr.txt"

    manifest.append({
        "year": year,
        "paper": paper,
        "filename": filename,
        "pdf_exists": pdf.exists(),
        "ocr_exists": ocr.exists(),
        "source_status": "official_site_linked_bulk_archive",
        "answer_key_status": "not_verified"
    })

output = base / "manifest.json"
output.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Manifest created:", output)
print("Papers:", len(manifest))
print("PDFs found:", sum(x["pdf_exists"] for x in manifest))
print("OCR files found:", sum(x["ocr_exists"] for x in manifest))
