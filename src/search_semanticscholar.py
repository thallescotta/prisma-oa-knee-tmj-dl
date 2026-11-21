"""Run B1 and B2 in Semantic Scholar (Graph API, bulk search) and save the records.

The public endpoint is rate limited; with a free key (https://www.semanticscholar.org/product/api)
export S2_API_KEY=... . Output: data/raw/semanticscholar_<code>.csv
Usage:  python src/search_semanticscholar.py
"""
import csv
import json
import os
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import SEMANTIC_SCHOLAR, YEAR_END, YEAR_START

API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,year,externalIds,publicationTypes,venue,isOpenAccess"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def get(params):
    headers = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}
    for attempt in range(8):
        try:
            with urlopen(Request(f"{API}?{urlencode(params)}", headers=headers)) as r:
                return json.load(r)
        except HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(3 + 3 * attempt)
    raise SystemExit("Rate limited by Semantic Scholar; try again later or use S2_API_KEY.")


def main():
    os.makedirs(OUT, exist_ok=True)
    for code, string in SEMANTIC_SCHOLAR.items():
        rows, token = [], None
        while True:
            params = {"query": string, "year": f"{YEAR_START}-{YEAR_END}", "fields": FIELDS}
            if token:
                params["token"] = token
            data = get(params)
            for p in data.get("data", []):
                ids = p.get("externalIds") or {}
                rows.append({"paper_id": p["paperId"], "year": p.get("year"), "pmid": ids.get("PubMed", ""),
                             "doi": ids.get("DOI", ""), "arxiv": ids.get("ArXiv", ""),
                             "types": "/".join(p.get("publicationTypes") or []), "venue": p.get("venue", ""),
                             "open_access": p.get("isOpenAccess"), "title": p.get("title", "")})
            token = data.get("token")
            if not token:
                break
        path = os.path.join(OUT, f"semanticscholar_{code}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["paper_id"])
            w.writeheader()
            w.writerows(rows)
        print(f"{code}: {len(rows)} records -> {path}")


if __name__ == "__main__":
    main()
