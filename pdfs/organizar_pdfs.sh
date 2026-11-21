#!/usr/bin/env bash
# Copia os PDFs numerados (1.pdf ... 27.pdf, na ordem de docs/lista_pdfs.md) para pdfs/ com o nome da chave BibTeX.
# Os que não podem ser redistribuídos vão para pdfs/_local/, que o Git ignora.
# Uso (na raiz do repositório):  bash pdfs/organizar_pdfs.sh "/c/Users/Thalles/Downloads/pdfs finais"
set -e
ORIGEM="$1"; DEST="$(dirname "$0")"
[ -d "$ORIGEM" ] || { echo "Pasta de origem não encontrada: $ORIGEM"; exit 1; }
mkdir -p "$DEST/_local"
publicos=(1:ananya_radiologyassistant_2023 2:daneshmand_osteophytes_2024 3:guida_3dcnn_2021 4:guo_cartilage_2024 5:karim_deepkneeexplainer_2021
 6:liao_ohc_2025 7:manfredonia_klgrade_2024 8:margain_cthmaps_2026 9:moorthy_csfaunet_2026 10:namiri_phenotyping_2021
 11:panwar_stacking_2024 12:panwar_vit_2025 13:simran_3dcnnvit_2025 14:yan_cnnmri_2021 15:yeoh_multitask_2023
 16:yeoh_tl3d_2023 17:zhong_uda_2023 18:choi_opg_2021 21:lang_m4tmd_2026 22:lee_bonescan_2025 23:lee_tmjfusion_2026
 24:nguyen_opg_2026 27:xu_tmjdjd_2026)
locais=(19:iqbal_cbct_2026 20:krishnamoorthy_pfrcnn_2023 25:nozawa_tmj_2024 26:trivedi_cbct_2026)
copia() { n="${1%%:*}"; k="${1#*:}"; if [ -f "$ORIGEM/$n.pdf" ]; then cp "$ORIGEM/$n.pdf" "$2/$k.pdf"; echo "ok    $n.pdf -> $2/$k.pdf"; else echo "FALTA $n.pdf ($k)"; fi; }
for p in "${publicos[@]}"; do copia "$p" "$DEST"; done
for p in "${locais[@]}"; do copia "$p" "$DEST/_local"; done
