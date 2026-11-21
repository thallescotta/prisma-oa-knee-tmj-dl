"""Compute the PRISMA 2020 numbers from the screening decisions.

Input:  data/screening_decisions.csv  (one row per record; columns: fonte, id, string,
        ano, oa, tipo, titulo, etapa, decisao). `decisao` is INCLUIDO or a criterion code.
Output: printed counts, data/prisma_counts.json and a Markdown table (data/selection_table.md).

The title/abstract decisions (stage T2) are made by the reviewer, not by code; this
script only aggregates them, so every number in the flow diagram can be traced back
to a row of the CSV.

Usage:  python src/prisma_counts.py
"""
import csv
import json
import os
from collections import Counter, OrderedDict

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")


def load():
    with open(os.path.join(DATA, "screening_decisions.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def counts(rows):
    db = [r for r in rows if r["etapa"] != "T4"]
    other = [r for r in rows if r["etapa"] == "T4"]
    dec = Counter(r["decisao"] for r in db)
    identified = Counter(r["fonte"] for r in db)
    screened = len(db) - dec["CE6"]
    excl_t2 = {c: dec[c] for c in ("CE1", "CE2", "CE3", "CE4", "CE7")}
    sought = screened - sum(excl_t2.values())
    assessed = sought - dec["CE5"]
    included_db = dec["INCLUIDO"]
    return OrderedDict(
        identified_by_source=dict(identified),
        identified_total=len(db),
        duplicates_removed=dec["CE6"],
        screened=screened,
        excluded_title_abstract=excl_t2,
        excluded_title_abstract_total=sum(excl_t2.values()),
        reports_sought=sought,
        reports_not_retrieved_CE5=dec["CE5"],
        reports_assessed=assessed,
        reports_excluded=assessed - included_db,
        other_sources_identified=len(other),
        other_sources_included=sum(r["decisao"] == "INCLUIDO" for r in other),
        included_total=included_db + sum(r["decisao"] == "INCLUIDO" for r in other),
    )


def selection_table(rows):
    lines = ["| Fonte | String | Identificados | T1 | T2 | T3 | Incluídos |", "|---|---|---|---|---|---|---|"]
    groups = OrderedDict()
    for r in rows:
        groups.setdefault((r["fonte"], r["string"]), []).append(r)
    for (fonte, s), g in groups.items():
        t1 = sum(r["decisao"] != "CE6" for r in g)
        t2 = sum(r["etapa"] in ("T3", "T4") for r in g)
        inc = sum(r["decisao"] == "INCLUIDO" for r in g)
        lines.append(f"| {fonte} | {s} | {len(g)} | {t1} | {t2} | {inc} | {inc} |")
    return "\n".join(lines) + "\n"


def main():
    rows = load()
    c = counts(rows)
    print(json.dumps(c, indent=2, ensure_ascii=False))
    with open(os.path.join(DATA, "prisma_counts.json"), "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    with open(os.path.join(DATA, "selection_table.md"), "w", encoding="utf-8") as f:
        f.write(selection_table(rows))


if __name__ == "__main__":
    main()
