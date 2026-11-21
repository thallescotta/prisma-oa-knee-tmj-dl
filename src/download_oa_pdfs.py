"""Download the open-access PDFs listed in references/included_studies.csv.

Only rows with redistribute_pdf starting with "yes" and a PMCID are downloaded,
through Europe PMC. The others must be saved by hand from the DOI link.
Check the licence printed on each PDF before committing it.

Usage:  python src/download_oa_pdfs.py
"""
import csv
import os
from urllib.request import Request, urlopen

ROOT = os.path.join(os.path.dirname(__file__), "..")
URL = "https://europepmc.org/articles/{pmcid}?pdf=render"


def main():
    with open(os.path.join(ROOT, "references", "included_studies.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if not r["redistribute_pdf"].startswith("yes"):
            print(f"skip   {r['key']}: licence does not allow redistribution")
            continue
        out = os.path.join(ROOT, "pdfs", r["pdf_file"])
        if os.path.exists(out):
            continue
        if not r["pmcid"]:
            print(f"manual {r['key']}: https://doi.org/{r['doi']}")
            continue
        req = Request(URL.format(pmcid=r["pmcid"]), headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req) as resp, open(out, "wb") as f:
            f.write(resp.read())
        print(f"ok     {r['key']}")


if __name__ == "__main__":
    main()
