# Como a busca foi feita em cada base

Todas as buscas foram feitas em **21/11/2026**, com período de publicação **2021–2026**. As strings exatas estão em `src/config.py`. Este arquivo explica como cada base foi consultada, que filtros foram usados e o que foi exportado.

Ordem de deduplicação: PubMed → IEEE Xplore → Europe PMC → SciELO → BVS/LILACS → SBC OpenLib → arXiv → Semantic Scholar. Quando um registro aparece em mais de uma base, ele vale só na primeira. Nas seguintes ele é marcado como duplicata (CE6). A comparação usa PMID, DOI e título.

## Resumo

| Área | Base | Interface | Strings | Registros | Novos (após T1) | Incluídos |
|---|---|---|---|---|---|---|
| Saúde | PubMed/MEDLINE | API E-utilities (`src/search_pubmed.py`) | B1, B2 | 98 | 98 | 14 |
| Computação | IEEE Xplore | Command Search, campo *Abstract* (`src/search_ieee.py` com chave) | B1, B2 | 29 | 27 | 1 |
| Saúde | Europe PMC | API REST, campo `TITLE_ABS` (`src/search_europepmc.py`) | B1, B2 | 97 | 27 | 1 |
| Saúde | SciELO | Busca do site (search.scielo.org), todos os índices | S1 | 2 | 1 | 0 |
| Saúde | BVS/LILACS | Portal Regional da BVS, coleção LILACS Plus | S1 (DeCS) | 4 | 3 | 0 |
| Computação | SBC OpenLib | Busca de cada série (SBCAS e SBCAS Estendido) | S2 | 4 | 4 | 0 |
| Computação | arXiv | API (`src/search_arxiv.py`), campo `abs` | B1, B2 | 8 | 6 | 0 |
| Computação | Semantic Scholar | Graph API, *bulk search* (`src/search_semanticscholar.py`) | B1, B2 | 207 | 86 | 11 |
| | **Total** | | | **449** | **252** | **27** |

## PubMed/MEDLINE (saúde)

- **Strings:** B1 e B2 com descritores MeSH e termos livres em título e resumo (`[tiab]`).
- **Filtro:** `2021:2026[dp]`. O critério de acesso aberto (CI4) foi aplicado depois, na etapa T3, com o subconjunto `"free full text"[sb]` do próprio PubMed.
- **Resultado:** B1 = 75; B2 = 23.

## IEEE Xplore (computação)

- **Strings:** B1 e B2 adaptadas. O IEEE não indexa MeSH, então os termos livres foram buscados no campo *Abstract*.
- **Filtro:** anos 2021–2026. O acesso aberto foi verificado pelo selo *Open Access* da base.
- **Resultado:** B1 = 26; B2 = 3. Duas duplicatas com o PubMed.
- **Reprodução:** `src/search_ieee.py` usa a API oficial, que pede uma chave gratuita. Sem chave, cole as strings em *Advanced Search → Command Search* e exporte o CSV.

## Europe PMC (saúde)

- **Strings:** B1 e B2 com os mesmos blocos lógicos, no campo `TITLE_ABS`.
- **Filtro:** `PUB_YEAR:[2021 TO 2026]`.
- **Resultado:** B1 = 72; B2 = 25. Destes, 67 já estavam no PubMed (mesmo PMID). A Europe PMC acrescenta *preprints* (Research Square, medRxiv, bioRxiv) e resumos de congresso, que foram excluídos por CE9.

## SciELO (saúde, América Latina)

- **String S1**, em português e inglês, unindo joelho e ATM numa só busca, porque a base é pequena e a interface não aceita a string completa com RM:
  `(osteoarthritis OR osteoartrite OR osteoartrose) AND (knee OR joelho OR temporomandibular) AND ("deep learning" OR "aprendizado profundo" OR "aprendizagem profunda" OR "neural network" OR "rede neural" OR "redes neurais")`
- **Filtro:** os dois resultados já estavam dentro de 2021–2026.
- **Resultado:** 2. Um é duplicata do PubMed (CE6) e o outro usa radiografia do joelho (CE4).

## BVS/LILACS (saúde, América Latina)

- **String S1 com descritores DeCS** (`mh:`) e termos livres; ver `src/config.py`.
- **Coleção:** LILACS Plus. A coleção completa repete o MEDLINE, já coberto pelo PubMed.
- **Resultado:** 4. São 1 duplicata, 1 revisão e 2 estudos do joelho sem RM.
- **Observação:** o portal bloqueia acesso automatizado. A busca foi feita pela interface web e os resultados foram copiados à mão.

## SBC OpenLib (computação, Brasil)

- **String S2:** `osteoarthritis OR osteoartrite OR temporomandibular OR knee OR joelho`. A busca do OJS não aceita parênteses aninhados, e os anais da SBC sobre o tema são poucos.
- **Séries consultadas:** Anais do SBCAS e Anais Estendidos do SBCAS, de 2021 a 2026. A busca no portal inteiro exige login.
- **Resultado:** 4 no SBCAS e 0 no SBCAS Estendido. Dois usam radiografia (CE4) e dois são do próprio autor (CE7).

## arXiv (computação, preprints)

- **Strings:** B1 e B2 no campo `abs`.
- **Filtro:** `submittedDate:[202101010000 TO 202612312359]`.
- **Resultado:** B1 = 8; B2 = 0. Todos são *preprints*: os que não tinham versão publicada já identificada foram excluídos por CE9.

## Semantic Scholar (computação e multidisciplinar)

- **Strings:** B1 e B2 na sintaxe da *bulk search* (`+` = AND, `|` = OR), aplicadas a título e resumo.
- **Filtro:** `year=2021-2026`.
- **Resultado:** B1 = 171; B2 = 36. Destes, 84 já estavam no PubMed ou na Europe PMC (mesmo PMID) e 37 eram duplicatas do IEEE, do arXiv ou de *preprints* da Europe PMC.
- **Por que esta base:** ela cobre anais de computação (IEEE, ACM, Springer, SciTePress) e periódicos fora do MEDLINE. Foi daqui que vieram 11 dos 27 incluídos, entre eles o estudo de Guida et al. (2021), que na v1.0 só tinha entrado por busca manual.
- **Limite:** a busca não é tão controlada quanto a do PubMed, porque o índice tem ranqueamento e variações de grafia. Por isso a triagem dessa base foi a mais trabalhosa.

## Bases consideradas e não executadas

| Base | Motivo | Como executar |
|---|---|---|
| Scopus | Exige login institucional | Portal de Periódicos CAPES → acesso CAFe → TITLE-ABS-KEY com a lógica de B1 e B2 |
| Web of Science | Exige login institucional | Portal CAPES → CAFe → campo TS= com a lógica de B1 e B2 |
| Embase | Exige login institucional | Portal CAPES → CAFe → Emtree + termos livres |
| ACM Digital Library | Verificação anti-robô impede acesso automatizado | Busca avançada, campo *Abstract*, 2021–2026 |
| dblp | Verificação anti-robô impede acesso automatizado | Busca por título (o dblp não indexa resumos) |

Quando essas bases forem executadas, acrescente as linhas ao `data/screening_decisions.csv` e rode `python src/prisma_counts.py`. O fluxograma e as tabelas são gerados de novo automaticamente.
