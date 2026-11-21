"""Run B1 and B2 in arXiv (public API) and save the records.

Output: data/raw/arxiv_<code>.csv
Usage:  python src/search_arxiv.py
"""
import csv
import os
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen

from config import ARXIV, ARXIV_FILTER

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def main():
    os.makedirs(OUT, exist_ok=True)
    for code, string in ARXIV.items():
        q = urlencode({"search_query": string + ARXIV_FILTER, "max_results": 500})
        with urlopen(f"{API}?{q}") as r:
            root = ET.fromstring(r.read())
        rows = []
        for e in root.findall("a:entry", NS):
            rows.append({
                "arxiv_id": e.findtext("a:id", "", NS).split("/abs/")[-1],
                "year": e.findtext("a:published", "", NS)[:4],
                "doi": e.findtext("x:doi", "", NS),
                "journal_ref": e.findtext("x:journal_ref", "", NS),
                "title": " ".join(e.findtext("a:title", "", NS).split()),
            })
        path = os.path.join(OUT, f"arxiv_{code}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["arxiv_id", "year", "doi", "journal_ref", "title"])
            w.writeheader()
            w.writerows(rows)
        print(f"{code}: {len(rows)} records -> {path}")


if __name__ == "__main__":
    main()
