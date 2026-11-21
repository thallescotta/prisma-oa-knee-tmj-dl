# Histórico de versões

## 2.0.0 – 21/11/2026
- Seis bases novas: Europe PMC, SciELO, BVS/LILACS, SBC OpenLib, arXiv e Semantic Scholar. No total, 8 bases executadas (4 de saúde e 4 de computação).
- Cinco bases registradas como consideradas e não executadas (Scopus, Web of Science, Embase, ACM DL e dblp), com o motivo e o passo a passo para executá-las.
- Critérios novos: CE8 (sem aprendizado profundo) e CE9 (preprint, tese, resumo de congresso ou parecer). O CE4 agora vale para joelho sem RM em qualquer modalidade (radiografia, TC, sensores ou texto).
- 449 registros identificados, 252 triados e 27 incluídos (17 de joelho e 10 de ATM).
- Guida et al. (2021) passa a entrar pela busca no Semantic Scholar, e não mais por "outras fontes".
- O fluxograma PRISMA é gerado automaticamente por `src/prisma_counts.py`, no estilo do modelo clássico em português (faixa laranja e abas azuis).
- Arquivos novos: `docs/bases.md`, com como cada base foi consultada, e `docs/lista_pdfs.md`, com os links e licenças dos 27 PDFs.
- Scripts novos: `search_europepmc.py`, `search_arxiv.py` e `search_semanticscholar.py`.

## 1.0.0 – 21/11/2026
- Primeira versão: PubMed e IEEE Xplore, 16 estudos incluídos.
