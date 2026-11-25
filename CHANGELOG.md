# Histórico de versões

## 2.3.0 – 25/11/2026
- Lido o texto completo de Wang *et al.* (2023, *Intelligent Automation and Soft Computing*, `scopus-b1-272`, CC BY 4.0): DenseNet201 em cortes 2D de volumes 3D DESS da OAI-ZIB, 120 joelhos, tarefa com/sem OA. Atende a CI1–CI4 e a nenhum CE: **incluído** (`wang_densenet_2023`). PDF em `pdfs/`.
- Total: 26 incluídos (16 de joelho e 10 de ATM); 2 registros do Scopus continuam aguardando leitura. Fluxograma, tabelas, `docs/lista_pdfs.md`, `docs/sintese.md` e BibTeX atualizados.
- Jung *et al.* (2023, *Oral Diseases*): texto completo obtido pelo Portal CAPES e usado para conferir os números citados na tese. Continua fora da revisão (CE5) e fora do repositório, porque a licença (© Wiley) não permite redistribuição.

## 2.2.0 – 22/11/2026
- Scopus e ACM Digital Library acessados pelo autor pelo Portal de Periódicos da CAPES (login institucional da UFCI/RJ, CAFe). Scopus B1: 353 registros (139 duplicatas, 214 triados). ACM B1: 1 registro (duplicata do IEEE Xplore); ACM B2: zero.
- Critério novo CE11 (idioma diferente de inglês ou português) e situação nova `AGUARDANDO` (texto completo de acesso aberto ainda não lido): 3 registros do Scopus.
- Total: 803 identificados, 337 duplicatas, 466 triados, 380 excluídos na triagem, 86 textos buscados, 58 não obtidos (56 CE5, 2 CE10), 25 incluídos.
- Pendentes: Scopus B2 (zero implausível) e Web of Science (consulta recusada na busca por campo).
- PDFs de Iqbal et al. (2026, CC BY) e Trivedi et al. (2026, CC BY-NC-ND) passam para `pdfs/`; PDFs de contexto (Bien et al., 2018; Lee et al., 2024) em `pdfs/contexto/`.

## 2.1.0 – 21/11/2026
- Critério novo CE10 (texto completo não obtido). Manfredonia et al. (2024) e Yan (2021) foram excluídos: os dois são de acesso aberto, mas o download falhou (CAPTCHA na SciTePress; bloqueio no site da Hindawi/Wiley).
- Incluídos: 25 (15 de joelho e 10 de ATM). Textos completos não obtidos: 39 (37 sem acesso aberto, CE5; 2 com download que falhou, CE10).
- PDFs dos 21 estudos de licença aberta em `pdfs/`. Licenças conferidas na primeira página de cada PDF.
- `docs/sintese.md`: resumo dos 25 estudos, relação de cada um com a tese e padrões do conjunto.
- Correções: licença de Yeoh et al. (2023, IEEE Access) é CC BY-NC-ND 4.0; páginas de Simran et al. (2025) são 1647–1667.

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
