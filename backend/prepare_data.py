"""
prepare_data.py  --  Merges the Lens.org CSV exports into ONE clean file.

Run this whenever you add new CSV files to the  data/  folder:

    python backend/prepare_data.py

Input : every *.csv inside the  data/  folder (Lens.org exports)
Output: backend/indian_patents.csv  with columns
        patent_no, title, abstract, year, applicant, status, url

Not AI, just data cleaning:
  - removes duplicate patents (same patent number)
  - if a patent appears twice, keeps the copy that HAS an abstract
  - tidies ALL-CAPS titles
"""
import csv
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data")
OUT_FILE = os.path.join(ROOT, "backend", "indian_patents.csv")

csv.field_size_limit(10 ** 8)  # some Lens columns are very long


def tidy_title(title):
    title = " ".join((title or "").replace('"', " ").split())
    if title.isupper():          # "WATER PURIFICATION DEVICE" -> "Water Purification Device"
        title = title.title()
    return title


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            patent_no = (row.get("Display Key") or "").strip()
            title = tidy_title(row.get("Title"))
            if not patent_no or not title:
                continue
            yield {
                "patent_no": patent_no,
                "title": title,
                "abstract": " ".join((row.get("Abstract") or "").split()),
                "year": (row.get("Publication Year") or "").strip(),
                "applicant": (row.get("Applicants") or "").split(";;")[0].strip(),
                "status": (row.get("Legal Status") or "").strip().title(),
                "url": (row.get("URL") or "").strip(),
            }


def main():
    files = sorted(glob.glob(os.path.join(IN_DIR, "*.csv")))
    if not files:
        print("No CSV files found in", IN_DIR)
        return

    best = {}  # patent_no -> row
    total_read = 0
    for path in files:
        for row in read_rows(path):
            total_read += 1
            old = best.get(row["patent_no"])
            if old is None or (row["abstract"] and not old["abstract"]):
                best[row["patent_no"]] = row

    rows = sorted(best.values(), key=lambda r: r["patent_no"])
    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["patent_no", "title", "abstract", "year", "applicant", "status", "url"])
        writer.writeheader()
        writer.writerows(rows)

    with_abs = sum(1 for r in rows if r["abstract"])
    print(f"Files read          : {len(files)}")
    print(f"Rows read           : {total_read}")
    print(f"Unique patents saved: {len(rows)}")
    print(f"  with abstract     : {with_abs}")
    print(f"  title only        : {len(rows) - with_abs}")
    print("Saved to", OUT_FILE)


if __name__ == "__main__":
    main()
