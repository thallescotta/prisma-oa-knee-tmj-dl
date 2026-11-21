"""Run the PubMed strings (B1, B2) through NCBI E-utilities and save the records.

Output: data/raw/pubmed_<code>.csv with PMID, title, year, journal, DOI, PMCID,
publication types and a flag for PubMed's "free full text" subset.

Usage:  python src/search_pubmed.py            (optional: export NCBI_API_KEY=...)
"""
import csv
import os
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import urlopen

from config import PUBMED, YEAR_END, YEAR_START

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
API_KEY = os.environ.get("NCBI_API_KEY")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def _get(endpoint, **params):
    if API_KEY:
        params["api_key"] = API_KEY
    with urlopen(EUTILS + endpoint + "?" + urlencode(params)) as r:
        data = r.read()
    time.sleep(0.35 if not API_KEY else 0.12)  # NCBI rate limits
    return data


def esearch(term):
    import json
    res = json.loads(_get("esearch.fcgi", db="pubmed", retmode="json", retmax=10000, term=term))
    return res["esearchresult"]["idlist"]


def efetch(pmids):
    rows = []
    for i in range(0, len(pmids), 200):
        root = ET.fromstring(_get("efetch.fcgi", db="pubmed", retmode="xml", id=",".join(pmids[i:i + 200])))
        for art in root.iter("PubmedArticle"):
            g = lambda path: (art.findtext(path) or "").strip()
            ids = {a.get("IdType"): a.text for a in art.iter("ArticleId")}
            rows.append({
                "pmid": g("MedlineCitation/PMID"),
                "title": "".join(art.find("MedlineCitation/Article/ArticleTitle").itertext()).strip(),
                "year": g("MedlineCitation/Article/Journal/JournalIssue/PubDate/Year")
                        or g("MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate")[:4],
                "journal": g("MedlineCitation/Article/Journal/Title"),
                "doi": ids.get("doi", ""),
                "pmcid": ids.get("pmc", ""),
                "pub_types": "; ".join(p.text for p in art.iter("PublicationType")),
            })
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    period = f" AND {YEAR_START}:{YEAR_END}[dp]"
    for code, string in PUBMED.items():
        ids = esearch(string + period)
        free = set(esearch(string + period + ' AND "free full text"[sb]'))
        rows = efetch(ids)
        for r in rows:
            r["free_full_text"] = r["pmid"] in free
            r["string"] = code
        path = os.path.join(OUT, f"pubmed_{code}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["pmid"])
            w.writeheader()
            w.writerows(rows)
        print(f"{code}: {len(ids)} records ({len(free)} free full text) -> {path}")


if __name__ == "__main__":
    main()
