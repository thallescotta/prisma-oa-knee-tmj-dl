"""Search configuration (v2.0): Boolean strings, period and databases.

Every string actually executed is stored here, with the syntax of each database.
B1 = knee (narrow: knee OA + MRI + deep learning + task); B2 = temporomandibular joint
(broad: TMJ + OA + deep learning, any imaging modality); S1/S2 = combined strings used in
small databases whose interface does not support the full B1/B2 syntax.
See docs/bases.md for how each search was run.
"""

SEARCH_DATE_V1 = "2026-11-21"  # PubMed, IEEE Xplore
SEARCH_DATE_V2 = "2026-11-21"  # Europe PMC, SciELO, BVS, SBC OpenLib, arXiv, Semantic Scholar
YEAR_START, YEAR_END = 2021, 2026

# ---------------------------------------------------------------- PubMed/MEDLINE
_DL = ('("Deep Learning"[MeSH] OR "Neural Networks, Computer"[MeSH] '
       'OR "deep learning"[tiab] OR "convolutional neural network*"[tiab])')
PUBMED = {
    "B1": ('("Osteoarthritis, Knee"[MeSH] OR "knee osteoarthritis"[tiab]) AND '
           '("Magnetic Resonance Imaging"[MeSH] OR MRI[tiab] OR "magnetic resonance"[tiab]) AND '
           f'{_DL} AND (classif*[tiab] OR grading[tiab] OR diagnos*[tiab] OR detection[tiab])'),
    "B2": ('("Temporomandibular Joint"[MeSH] OR "Temporomandibular Joint Disorders"[MeSH] OR temporomandibular[tiab]) AND '
           '("Osteoarthritis"[MeSH] OR osteoarthritis[tiab] OR "degenerative joint disease"[tiab]) AND '
           f'{_DL}'),
}
PUBMED_FILTER = f" AND {YEAR_START}:{YEAR_END}[dp]"

# ---------------------------------------------------------------- IEEE Xplore (Command Search, field Abstract)
_DL_IEEE = '("Abstract":"deep learning" OR "Abstract":"convolutional neural network" OR "Abstract":"neural network")'
IEEE = {
    "B1": ('("Abstract":"knee osteoarthritis") AND ("Abstract":MRI OR "Abstract":"magnetic resonance") AND '
           f'{_DL_IEEE} AND ("Abstract":classification OR "Abstract":grading OR "Abstract":diagnosis OR "Abstract":detection)'),
    "B2": ('("Abstract":temporomandibular OR "Abstract":TMJ) AND '
           f'("Abstract":osteoarthritis OR "Abstract":"degenerative joint disease") AND {_DL_IEEE}'),
}

# ---------------------------------------------------------------- Europe PMC (REST API, field TITLE_ABS)
_DL_EPMC = ('("deep learning" OR "convolutional neural network" OR "convolutional neural networks" '
            'OR "neural network" OR "neural networks")')
EUROPEPMC = {
    "B1": ('TITLE_ABS:(("knee osteoarthritis" OR (knee AND osteoarthritis)) AND (MRI OR "magnetic resonance") AND '
           f'{_DL_EPMC} AND (classification OR classify OR grading OR diagnosis OR detection))'),
    "B2": f'TITLE_ABS:((temporomandibular OR TMJ) AND (osteoarthritis OR "degenerative joint disease") AND {_DL_EPMC})',
}
EUROPEPMC_FILTER = f" AND PUB_YEAR:[{YEAR_START} TO {YEAR_END}]"

# ---------------------------------------------------------------- arXiv (API, field abs)
_DL_ARXIV = '(abs:"deep learning" OR abs:"convolutional neural network" OR abs:"neural network")'
ARXIV = {
    "B1": ('(abs:"knee osteoarthritis" OR (abs:knee AND abs:osteoarthritis)) AND (abs:MRI OR abs:"magnetic resonance") AND '
           f'{_DL_ARXIV} AND (abs:classification OR abs:grading OR abs:diagnosis OR abs:detection)'),
    "B2": f'(abs:temporomandibular OR abs:TMJ) AND (abs:osteoarthritis OR abs:"degenerative joint disease") AND {_DL_ARXIV}',
}
ARXIV_FILTER = " AND submittedDate:[202101010000 TO 202612312359]"

# ---------------------------------------------------------------- Semantic Scholar (bulk search; + = AND, | = OR)
SEMANTIC_SCHOLAR = {
    "B1": ('("knee osteoarthritis" | (knee + osteoarthritis)) + (MRI | "magnetic resonance") + '
           '("deep learning" | "convolutional neural network" | "neural network") + '
           '(classification | grading | diagnosis | detection)'),
    "B2": ('(temporomandibular | TMJ) + (osteoarthritis | "degenerative joint disease") + '
           '("deep learning" | "convolutional neural network" | "neural network")'),
}

# ---------------------------------------------------------------- Manual interfaces (no public API used)
SCIELO_S1 = ('(osteoarthritis OR osteoartrite OR osteoartrose) AND (knee OR joelho OR temporomandibular) AND '
             '("deep learning" OR "aprendizado profundo" OR "aprendizagem profunda" OR "neural network" '
             'OR "rede neural" OR "redes neurais")')
BVS_S1 = ('(mh:"Osteoartrite" OR mh:"Osteoartrite do Joelho" OR osteoarthritis OR osteoartrite) AND '
          '(mh:"Articulação Temporomandibular" OR mh:"Transtornos da Articulação Temporomandibular" OR temporomandibular '
          'OR knee OR joelho) AND (mh:"Aprendizagem Profunda" OR mh:"Redes Neurais de Computação" OR "deep learning" '
          'OR "aprendizado profundo")')
SBC_S2 = "osteoarthritis OR osteoartrite OR temporomandibular OR knee OR joelho"  # SBCAS e SBCAS Estendido, 2021-2026

# ---------------------------------------------------------------- Restricted databases (Portal de Periódicos CAPES, CAFe login UFCI/RJ)
SEARCH_DATE_V3 = "2026-11-22"  # Scopus, Web of Science, ACM Digital Library (run by the author in the browser)
_DL_SCOPUS = '("deep learning" OR "convolutional neural network*" OR "neural network*")'
SCOPUS = {
    "B1": ('TITLE-ABS-KEY(("knee osteoarthritis" OR (knee AND osteoarthritis)) AND (mri OR "magnetic resonance") AND '
           f'{_DL_SCOPUS} AND (classif* OR grading OR diagnos* OR detection)) AND PUBYEAR > 2020 AND PUBYEAR < 2027'),
    "B2": ('TITLE-ABS-KEY((temporomandibular OR tmj) AND (osteoarthritis OR "degenerative joint disease") AND '
           f'{_DL_SCOPUS}) AND PUBYEAR > 2020 AND PUBYEAR < 2027'),
}
WOS = {
    "B1": ('TS=(("knee osteoarthritis" OR (knee AND osteoarthritis)) AND (MRI OR "magnetic resonance") AND '
           f'{_DL_SCOPUS} AND (classif* OR grading OR diagnos* OR detection)) AND PY=(2021-2026)'),
    "B2": f'TS=((temporomandibular OR TMJ) AND (osteoarthritis OR "degenerative joint disease") AND {_DL_SCOPUS}) AND PY=(2021-2026)',
}
ACM = {
    "B1": 'Abstract:("knee osteoarthritis" AND (MRI OR "magnetic resonance") AND ("deep learning" OR "neural network"))',
    "B2": 'Abstract:((temporomandibular OR TMJ) AND osteoarthritis AND ("deep learning" OR "neural network"))',
}

# Searches not (validly) executed, reported in the PRISMA notes
NOT_EXECUTED = {
    "Scopus (B2)": "reported as zero records on 2026-11-22; implausible (Nozawa et al. 2024, indexed in Scopus, matches B2); rerun",
    "Web of Science (B1, B2)": "query typed in Fielded Search returned 'Invalid query' on 2026-11-22; rerun in Query Builder",
    "Embase": "not consulted in this version",
    "dblp": "indexes titles only (no abstracts); bot verification blocks automated access",
}

# Eligibility criteria (codes used in data/screening_decisions.csv)
CRITERIA = {
    "CI1": "Primary study using deep learning to classify, grade or detect OA (or a degenerative finding) of the knee or TMJ",
    "CI2": "Knee: MRI input stated in the abstract. TMJ: any imaging modality",
    "CI3": "Published 2021-2026, in English or Portuguese",
    "CI4": "Full text obtained (open access or through the CAPES Journal Portal)",
    "CE1": "Review, systematic review, meta-analysis, bibliometrics, editorial, perspective or retraction",
    "CE2": "Only segmentation, quantification, reconstruction or image enhancement (no OA classification)",
    "CE3": "Other outcome or joint: progression, arthroplasty, ligament/meniscus injury, other disease",
    "CE4": "Knee without MRI input (radiograph, CT, sensors or clinical text only)",
    "CE5": "Full text not yet obtained (not open access; to be sought through the CAPES Journal Portal)",
    "CE6": "Duplicate record (already identified in a database searched earlier)",
    "CE7": "Author's own work (already reported as Contribution 1 or 2)",
    "CE8": "Does not use deep learning (classical machine learning only)",
    "CE9": "Not a peer-reviewed full paper: preprint, thesis, congress abstract or peer-review report",
    "CE10": "Full text not retrieved: open access, but the download was blocked or failed on the publisher's site",
    "CE11": "Not in English or Portuguese (fails CI3)",
}
# AGUARDANDO (decisao): open-access report that passed title/abstract screening and whose full text is still to be read

# Order in which databases were deduplicated (a record is CE6 in every database after the first one)
DEDUP_ORDER = ["PubMed", "IEEE Xplore", "Europe PMC", "SciELO", "BVS/LILACS", "SBC OpenLib", "arXiv", "Semantic Scholar", "Scopus", "ACM Digital Library"]
