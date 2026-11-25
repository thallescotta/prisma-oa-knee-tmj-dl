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
| Computação | Semantic Scholar | Graph API, *bulk search* (`src/search_semanticscholar.py`) | B1, B2 | 207 | 86 | 9 |
| | **Total** | | | **449** | **252** | **25** |

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
- **Por que esta base:** ela cobre anais de computação (IEEE, ACM, Springer, SciTePress) e periódicos fora do MEDLINE. Foi daqui que vieram 9 dos 25 incluídos, entre eles o estudo de Guida et al. (2021), que na v1.0 só tinha entrado por busca manual.
- **Limite:** a busca não é tão controlada quanto a do PubMed, porque o índice tem ranqueamento e variações de grafia. Por isso a triagem dessa base foi a mais trabalhosa.

## Bases de acesso restrito (Portal de Periódicos da CAPES)

Scopus, Web of Science e ACM Digital Library foram acessadas pelo autor em 22/11/2026 pelo Portal de Periódicos da CAPES, com login institucional da UFCI/RJ (CAFe), com as strings abaixo.

| Base | String | Resultado em 22/11/2026 | Situação |
|---|---|---|---|
| Scopus | B1 | 353 registros | Incorporados. A lista de resultados impressa foi convertida em `data/scopus_b1_2026-11-22.csv` (título, autores, fonte, ano). Como a impressão não traz resumos, os registros novos foram triados pelo título; os 29 que passaram foram conferidos pelo resumo e pelo status de acesso aberto no OpenAlex. |
| Scopus | B2 | relatado como zero | **Não incorporado.** O zero é implausível: Nozawa *et al.* (2024), indexado no Scopus, atende à string B2. Rodar de novo. |
| ACM DL | B1 | 1 registro (ACM Full-Text Collection) | Incorporado: duplicata de um registro do IEEE Xplore (CE6). |
| ACM DL | B2 | zero (ACM Full-Text Collection) | Incorporado como zero. |
| Web of Science | B1 e B2 | "Search Error: Invalid query" | **Não executado.** A string foi colada na busca por campo (*Fielded Search*), que não aceita `TS=`; usar a aba *Query Builder*. |

Dois registros do Scopus passaram na triagem, estão em acesso aberto e aguardam a leitura do texto completo (`decisao = AGUARDANDO`): `scopus-b1-039` (MVMI, *Biomedical Signal Processing and Control*, 2025, cópia aberta no HAL) e `scopus-b1-101` (*Image and Vision Computing*, 160, 105574, 2025). O terceiro, `scopus-b1-272` (Wang *et al.*, *Intelligent Automation and Soft Computing*, 2023, DOI 10.32604/iasc.2023.036766, CC BY 4.0), foi lido em 25/11/2026 e incluído (`wang_densenet_2023`).

Primeira tentativa (descartada): antes destas strings, a mesma string foi colada nas três bases sem adaptar a sintaxe, e as três retornaram zero. Esse zero não é usado.

**Scopus** (Advanced search)

```
B1: TITLE-ABS-KEY(("knee osteoarthritis" OR (knee AND osteoarthritis)) AND (mri OR "magnetic resonance") AND ("deep learning" OR "convolutional neural network*" OR "neural network*") AND (classif* OR grading OR diagnos* OR detection)) AND PUBYEAR > 2020 AND PUBYEAR < 2027
B2: TITLE-ABS-KEY((temporomandibular OR tmj) AND (osteoarthritis OR "degenerative joint disease") AND ("deep learning" OR "convolutional neural network*" OR "neural network*")) AND PUBYEAR > 2020 AND PUBYEAR < 2027
```

**Web of Science Core Collection** (Advanced Search, Query Builder)

```
B1: TS=(("knee osteoarthritis" OR (knee AND osteoarthritis)) AND (MRI OR "magnetic resonance") AND ("deep learning" OR "convolutional neural network*" OR "neural network*") AND (classif* OR grading OR diagnos* OR detection)) AND PY=(2021-2026)
B2: TS=((temporomandibular OR TMJ) AND (osteoarthritis OR "degenerative joint disease") AND ("deep learning" OR "convolutional neural network*" OR "neural network*")) AND PY=(2021-2026)
```

**ACM Digital Library** (ACM Guide to Computing Literature, filtro 2021–2026)

```
B1: Abstract:("knee osteoarthritis" AND (MRI OR "magnetic resonance") AND ("deep learning" OR "neural network"))
B2: Abstract:((temporomandibular OR TMJ) AND osteoarthritis AND ("deep learning" OR "neural network"))
```

Exportação: Scopus em CSV (título, autores, ano, DOI, resumo), Web of Science em Excel (*Full Record*), ACM em BibTeX. Depois, acrescente as linhas ao `data/screening_decisions.csv` e rode `python src/prisma_counts.py`.

## Bases consideradas e não executadas

| Base | Motivo |
|---|---|
| Embase | Não consultada nesta versão |
| dblp | Indexa só títulos, sem resumos; verificação anti-robô impede acesso automatizado |

## Textos completos não obtidos (CE10)

Dois estudos de acesso aberto passaram na triagem, mas o PDF não pôde ser obtido em 21/11/2026:

| Estudo | DOI | Motivo |
|---|---|---|
| Manfredonia *et al.* (2024), ICAART, SciTePress, CC BY-NC-ND 4.0 | 10.5220/0012471200003636 | O download na página da SciTePress exige CAPTCHA, e a tentativa falhou |
| Yan (2021), *Scientific Programming* (Hindawi, hoje Wiley) | 10.1155/2021/2803857 | O site antigo da Hindawi redireciona para a Wiley, que bloqueou o acesso ("Sorry, you have been blocked"). Não há retratação registrada no Crossref |

Eles aparecem no fluxograma junto com os de CE5, na caixa "Textos completos não obtidos", como o PRISMA 2020 pede para *reports not retrieved*. Se os PDFs forem obtidos depois, basta trocar a decisão no CSV para INCLUIDO e rodar `src/prisma_counts.py`.
