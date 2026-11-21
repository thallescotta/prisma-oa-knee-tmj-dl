"""Search configuration: Boolean strings, period and databases.

Every string is versioned here so that the search can be re-run and audited.
B1 = knee (narrow, MRI only); B2 = temporomandibular joint (broad, any imaging modality).
"""

SEARCH_DATE = "2026-11-21"  # date of the search reported in the qualification text
YEAR_START, YEAR_END = 2021, 2026

# Building blocks (MeSH descriptors + free-text terms in title/abstract)
DL = ('("Deep Learning"[MeSH] OR "Neural Networks, Computer"[MeSH] '
      'OR "deep learning"[tiab] OR "convolutional neural network*"[tiab])')
KNEE = '("Osteoarthritis, Knee"[MeSH] OR "knee osteoarthritis"[tiab])'
MRI = '("Magnetic Resonance Imaging"[MeSH] OR MRI[tiab] OR "magnetic resonance"[tiab])'
TASK = '(classif*[tiab] OR grading[tiab] OR diagnos*[tiab] OR detection[tiab])'
TMJ = ('("Temporomandibular Joint"[MeSH] OR "Temporomandibular Joint Disorders"[MeSH] '
       'OR temporomandibular[tiab])')
OA = '("Osteoarthritis"[MeSH] OR osteoarthritis[tiab] OR "degenerative joint disease"[tiab])'

PUBMED = {
    "B1": f"{KNEE} AND {MRI} AND {DL} AND {TASK}",
    "B2": f"{TMJ} AND {OA} AND {DL}",
}

# IEEE Xplore does not index MeSH: the same logic is applied to the abstract field.
_DL_IEEE = '("Abstract":"deep learning" OR "Abstract":"convolutional neural network" OR "Abstract":"neural network")'
IEEE = {
    "B1": ('("Abstract":"knee osteoarthritis") AND ("Abstract":MRI OR "Abstract":"magnetic resonance") AND '
           f'{_DL_IEEE} AND ("Abstract":classification OR "Abstract":grading OR "Abstract":diagnosis OR "Abstract":detection)'),
    "B2": ('("Abstract":temporomandibular OR "Abstract":TMJ) AND '
           f'("Abstract":osteoarthritis OR "Abstract":"degenerative joint disease") AND {_DL_IEEE}'),
}

# Eligibility criteria (codes used in data/screening_decisions.csv)
CRITERIA = {
    "CI1": "Primary study using deep learning to classify, grade or detect OA (or a degenerative finding) of the knee or TMJ",
    "CI2": "Knee: MRI input. TMJ: any imaging modality",
    "CI3": "Published 2021-2026, in English or Portuguese",
    "CI4": "Full text available in open access",
    "CE1": "Review, systematic review, meta-analysis, bibliometrics, perspective or retraction",
    "CE2": "Only segmentation, quantification, reconstruction or image enhancement (no OA classification)",
    "CE3": "Other outcome: progression, arthroplasty, ligament/meniscus injury, other disease",
    "CE4": "Knee with radiograph-only or clinical-text-only input",
    "CE5": "Full text not available in open access",
    "CE6": "Duplicate record across databases",
    "CE7": "Author's own work (already reported as Contribution 1 or 2)",
}
