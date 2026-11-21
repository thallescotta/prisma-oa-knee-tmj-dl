"""Run the IEEE Xplore strings (B1, B2) through the official IEEE Xplore API.

Requires a free API key (https://developer.ieee.org): export IEEE_API_KEY=...
Without a key, run the same strings in the Advanced Search ("Command Search"),
filter 2021-2026 and export the results as CSV to data/raw/ieee_<code>.csv.

Usage:  python src/search_ieee.py
"""
import csv
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

from config import IEEE, YEAR_END, YEAR_START

API = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def search(querytext, key):
    rows, start = [], 1
    while True:
        q = urlencode({"querytext": querytext, "start_year": YEAR_START, "end_year": YEAR_END,
                       "max_records": 200, "start_record": start, "apikey": key, "format": "json"})
        with urlopen(f"{API}?{q}") as r:
            data = json.load(r)
        arts = data.get("articles", [])
        for a in arts:
            rows.append({
                "article_number": a.get("article_number", ""),
                "title": a.get("title", ""),
                "year": a.get("publication_year", ""),
                "venue": a.get("publication_title", ""),
                "content_type": a.get("content_type", ""),
                "doi": a.get("doi", ""),
                "open_access": a.get("access_type", "") == "OPEN_ACCESS",
            })
        start += len(arts)
        if not arts or start > data.get("total_records", 0):
            return rows


def main():
    key = os.environ.get("IEEE_API_KEY")
    if not key:
        raise SystemExit("Set IEEE_API_KEY or export the results manually (see the docstring).")
    os.makedirs(OUT, exist_ok=True)
    for code, string in IEEE.items():
        rows = search(string, key)
        for r in rows:
            r["string"] = code
        path = os.path.join(OUT, f"ieee_{code}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["article_number"])
            w.writeheader()
            w.writerows(rows)
        print(f"{code}: {len(rows)} records -> {path}")


if __name__ == "__main__":
    main()
