"""Compute the PRISMA 2020 numbers from the screening decisions and draw the flow diagram.

Input:  data/screening_decisions.csv (one row per record: base, id, string, ano,
        acesso_aberto, tipo, titulo, etapa, decisao). `decisao` is INCLUIDO or a criterion code.
Output: data/prisma_counts.json, data/selection_table.md and figures/prisma2020.tex
        (compile the .tex with pdflatex to get the PDF of the diagram).

The title/abstract decisions are made by the reviewer, not by code: this script only
aggregates them, so every number of the diagram can be traced back to rows of the CSV.

Usage:  python src/prisma_counts.py
"""
import csv
import json
import os
from collections import Counter, OrderedDict

from config import DEDUP_ORDER, NOT_EXECUTED

ROOT = os.path.join(os.path.dirname(__file__), "..")
T2_CODES = ("CE1", "CE2", "CE3", "CE4", "CE7", "CE8", "CE9", "CE11")
LABELS = {"CE1": "revisões, editoriais", "CE2": "só segmentação/imagem", "CE3": "outro desfecho ou articulação",
          "CE4": "joelho sem RM", "CE7": "trabalhos do autor", "CE8": "sem aprendizado profundo",
          "CE9": "preprints, resumos, teses", "CE11": "outro idioma"}


def load():
    with open(os.path.join(ROOT, "data", "screening_decisions.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def counts(rows):
    dec = Counter(r["decisao"] for r in rows)
    by_base = Counter(r["base"] for r in rows)
    screened = len(rows) - dec["CE6"]
    excl = {c: dec[c] for c in T2_CODES if dec[c]}
    sought = screened - sum(excl.values())
    not_retrieved = dec["CE5"] + dec["CE10"]
    awaiting = dec["AGUARDANDO"]
    assessed = sought - not_retrieved - awaiting
    inc = [r for r in rows if r["decisao"] == "INCLUIDO"]
    return OrderedDict(
        identified_by_base=OrderedDict((b, by_base[b]) for b in DEDUP_ORDER if by_base[b] or b in by_base),
        identified_total=len(rows),
        duplicates_removed=dec["CE6"],
        screened=screened,
        excluded_title_abstract=excl,
        excluded_title_abstract_total=sum(excl.values()),
        reports_sought=sought,
        reports_not_retrieved=not_retrieved,
        not_retrieved_CE5_no_open_access=dec["CE5"],
        not_retrieved_CE10_download_failed=dec["CE10"],
        reports_awaiting_full_text=awaiting,
        reports_assessed=assessed,
        reports_excluded=assessed - len(inc),
        included_total=len(inc),
        included_knee=sum(r["string"] == "B1" for r in inc),
        included_tmj=sum(r["string"] == "B2" for r in inc),
        not_executed=NOT_EXECUTED,
    )


def selection_table(rows):
    out = ["| Base | String | Identificados | Após T1 | Após T2 | Incluídos |", "|---|---|---|---|---|---|"]
    groups = OrderedDict()
    for r in rows:
        groups.setdefault((r["base"], r["string"]), []).append(r)
    tot = [0, 0, 0, 0]
    for (base, s), g in groups.items():
        vals = [len(g), sum(r["decisao"] != "CE6" for r in g), sum(r["etapa"] == "T3" for r in g),
                sum(r["decisao"] == "INCLUIDO" for r in g)]
        tot = [a + b for a, b in zip(tot, vals)]
        out.append(f"| {base} | {s} | " + " | ".join(map(str, vals)) + " |")
    out.append("| **Total** | | " + " | ".join(f"**{v}**" for v in tot) + " |")
    return "\n".join(out) + "\n"


def tikz(c):
    """PRISMA 2020 diagram in the style of the classic Portuguese template (orange banner, blue side tabs)."""
    def two_cols(items):
        items = list(items)
        half = (len(items) + 1) // 2
        left, right = items[:half], items[half:] + [""] * (2 * half - len(items))
        body = r" \\ ".join(f"{a} & {b}" for a, b in zip(left, right))
        return r"\begin{tabular}{@{}l@{\hspace{10pt}}l@{}}" + body + r"\end{tabular}"
    bases = two_cols(f"{b}: {n}" for b, n in c["identified_by_base"].items())
    excl = r"\begin{tabular}{@{}l@{}}" + r" \\ ".join(
        f"{k} -- {LABELS[k]}: {v}" for k, v in c["excluded_title_abstract"].items()) + r"\end{tabular}"
    ne = ", ".join(NOT_EXECUTED)
    return rf"""% Gerado por src/prisma_counts.py -- não editar à mão; rode o script de novo.
\documentclass[border=6pt]{{standalone}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage[scaled]{{helvet}}
\renewcommand{{\familydefault}}{{\sfdefault}}
\usepackage{{tikz}}
\usetikzlibrary{{positioning,calc}}
\definecolor{{azulborda}}{{RGB}}{{79,129,189}}
\definecolor{{azulaba}}{{RGB}}{{91,155,213}}
\definecolor{{laranja}}{{RGB}}{{247,184,38}}
\begin{{document}}
\begin{{tikzpicture}}[font=\small,
  caixa/.style={{draw=azulborda, line width=0.9pt, fill=white, align=center, text width=5.6cm, inner sep=6pt}},
  lado/.style={{draw=azulborda, line width=0.9pt, fill=white, align=center, text width=6.4cm, inner sep=6pt}},
  linha/.style={{draw=azulaba, line width=1.6pt}},
  aba/.style={{draw=azulborda, fill=azulaba, rounded corners=6pt, text=white, font=\bfseries\large, minimum width=0.9cm}}]
\node[caixa] (id) at (0,0) {{Nº total de registros nas bases pesquisadas:\\[2pt] (N = {c['identified_total']})\\[3pt]
  {{\footnotesize {bases}}}}};
\node[lado, right=1.4cm of id] (dup) {{Removidos antes da triagem:\\[2pt] duplicatas entre bases (N = {c['duplicates_removed']})}};
\node[caixa, below=1.0cm of id] (tri) {{Registros triados por título e resumo:\\[2pt] (N = {c['screened']})}};
\node[lado, right=1.4cm of tri] (ex1) {{Excluídos após título e resumo:\\[2pt] (N = {c['excluded_title_abstract_total']})\\[3pt]
  {{\footnotesize {excl}}}}};
\node[caixa, below=2.6cm of tri] (bus) {{Textos completos buscados:\\[2pt] (N = {c['reports_sought']})}};
\node[lado, right=1.4cm of bus] (ce5) {{Textos completos não obtidos:\\[2pt] (N = {c['reports_not_retrieved']})\\[3pt]
  {{\footnotesize CE5 -- sem acesso aberto: {c['not_retrieved_CE5_no_open_access']}\\ CE10 -- download bloqueado ou indisponível: {c['not_retrieved_CE10_download_failed']}}}}};
\node[caixa, below=1.0cm of bus] (ele) {{Estudos elegíveis (texto completo):\\[2pt] (N = {c['reports_assessed']})}};
\node[lado, right=1.4cm of ele] (ex2) {{Removidos após leitura do texto completo:\\[2pt] (N = {c['reports_excluded']})\\[3pt]
  {{\footnotesize Aguardando leitura do texto completo: {c['reports_awaiting_full_text']}}}}};
\node[caixa, below=1.2cm of ele] (inc) {{Estudos incluídos nesta revisão:\\[2pt] (N = {c['included_total']})\\[2pt]
  {{\footnotesize joelho: {c['included_knee']}; ATM: {c['included_tmj']}}}}};
\path let \p1=(id.north west), \p2=(dup.north east) in node[draw=black!70, fill=laranja, rounded corners=6pt,
  minimum width=\x2-\x1, minimum height=0.9cm, font=\large, anchor=south] (banner) at (\x1/2+\x2/2, \y1+0.4cm)
  {{Identificação de estudos a partir de bases de dados}};
\foreach \a/\b in {{id/tri, tri/bus, bus/ele, ele/inc}} \draw[linha] (\a) -- (\b);
\foreach \a/\b in {{id/dup, tri/ex1, bus/ce5, ele/ex2}} \draw[linha] (\a) -- (\b);
\path let \p1=(id.north), \p2=(id.south) in node[aba, rotate=90, minimum width=\y1-\y2] at ($(id.west)+(-0.8,0)$) {{Identificação}};
\path let \p1=(tri.north), \p2=(ele.south) in node[aba, rotate=90, minimum width=\y1-\y2] at ($(tri.north west)!0.5!(ele.south west)+(-0.8,0)$) {{Triagem}};
\path let \p1=(inc.north), \p2=(inc.south) in node[aba, rotate=90, minimum width=\y1-\y2+0.4cm] at ($(inc.west)+(-0.8,0)$) {{Inclusão}};
% A lista de bases não executadas vai na legenda da figura (texto), não dentro do fluxograma.
\end{{tikzpicture}}
\end{{document}}
"""


def main():
    rows = load()
    c = counts(rows)
    print(json.dumps(c, indent=2, ensure_ascii=False))
    with open(os.path.join(ROOT, "data", "prisma_counts.json"), "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    with open(os.path.join(ROOT, "data", "selection_table.md"), "w", encoding="utf-8") as f:
        f.write(selection_table(rows))
    with open(os.path.join(ROOT, "figures", "prisma2020.tex"), "w", encoding="utf-8") as f:
        f.write(tikz(c))


if __name__ == "__main__":
    main()
