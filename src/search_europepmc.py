"""Run B1 and B2 in Europe PMC (REST API, no key needed) and save the records.

Output: data/raw/europepmc_<code>.csv  (id, source, pmid, pmcid, doi, year, title, open access)
Usage:  python src/search_europepmc.py
"""
import csv
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

from config import EUROPEPMC, EUROPEPMC_FILTER

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def search(query):
    rows, cursor = [], "*"
    while True:
        q = urlencode({"query": query, "format": "json", "pageSize": 100, "resultType": "lite", "cursorMark": cursor})
        with urlopen(f"{API}?{q}") as r:
            data = json.load(r)
        for x in data["resultList"]["result"]:
            rows.append({k: x.get(k, "") for k in ("id", "source", "pmid", "pmcid", "doi", "pubYear", "title", "isOpenAccess")})
        nxt = data.get("nextCursorMark")
        if not nxt or nxt == cursor or len(rows) >= data["hitCount"]:
            return rows
        cursor = nxt


def main():
    os.makedirs(OUT, exist_ok=True)
    for code, string in EUROPEPMC.items():
        rows = search(string + EUROPEPMC_FILTER)
        path = os.path.join(OUT, f"europepmc_{code}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["id"])
            w.writeheader()
            w.writerows(rows)
        print(f"{code}: {len(rows)} records -> {path}")


if __name__ == "__main__":
    main()
