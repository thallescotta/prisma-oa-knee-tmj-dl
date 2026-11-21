# Síntese dos estudos incluídos (v2.1)

Os 25 estudos incluídos, cada um com um resumo e a relação com o foco do doutorado. Esse foco é classificar volumes de RM com poucos dados rotulados, usando redes 3D pré-treinadas, e transferir o modelo do joelho para a ATM. O título da tese ainda não está fechado.

Os resumos foram feitos a partir dos resumos dos artigos e serão conferidos na leitura do texto completo. As métricas não são as mesmas em todos os estudos (acurácia em uns, AUC em outros), então os números não são comparáveis entre si.

As chaves correspondem a `references/included_studies.bib`, e os PDFs estão em `pdfs/`.

## Joelho (RM) – 15 estudos

| Estudo | Resumo | Relação com a tese |
|---|---|---|
| `guida_3dcnn_2021` – Guida *et al.*, 2021 | CNN 3D treinada do zero em volumes de RM de 1.100 joelhos; acurácia de 83,0% no teste, acima de modelos com radiografia. | Mostra o ganho do volume sobre a imagem 2D, mas sem pré-treino. As Contribuições 1 e 2 acrescentam o pré-treino em vídeo. |
| `karim_deepkneeexplainer_2021` – Karim *et al.*, 2021 | DeepKneeExplainer: diagnóstico da OA do joelho a partir de radiografias e RM, com explicação visual das regiões que pesaram na decisão. | Combina modalidades e trata de explicabilidade, ponto ainda ausente nas Contribuições 1 e 2. |
| `namiri_phenotyping_2021` – Namiri *et al.*, 2021 | CNNs classificam quatro fenótipos morfológicos (ósseo, menisco/cartilagem, inflamatório e hipertrófico) em RM de 4.791 participantes da OAI; AUC de 0,89 a 0,96. | Classificação por fenótipo em RM, a mesma ideia dos agrupamentos fenotípicos da ATM que rotulam os dados da Contribuição 3. |
| `ananya_radiologyassistant_2023` – Ananya *et al.*, 2023 | DenseNet com camadas *squeeze-and-excitation* classifica RM da OAI em saudável ou com OA e gera um laudo automático. | Mesma tarefa binária e mesma base da Contribuição 1, mas com cortes 2D. Periódico de menor impacto. |
| `yeoh_tl3d_2023` – Yeoh *et al.*, 2023 | Compara 13 CNNs 3D em volumes 3D DESS da OAI, com pesos 2D da ImageNet replicados na profundidade; a ResNet18 3D chega a AUC de 0,945. | É o estudo mais próximo das Contribuições 1 e 2. A diferença está no pré-treino: imagens 2D adaptadas, contra vídeo (Kinetics-400) já tridimensional na tese. |
| `yeoh_multitask_2023` – Yeoh *et al.*, 2023 | Avalia redes 3D multitarefa, que segmentam e classificam ao mesmo tempo, em RM do joelho da OAI. | Mesma base e mesma representação volumétrica, mas depende de máscaras de segmentação, que não existem para os exames da ATM. |
| `zhong_uda_2023` – Zhong *et al.*, 2023 | Adaptação de domínio não supervisionada de volumes 3D DESS da OAI (318 e 960) para 50 exames TSE/FSE de outra instituição; AUC de 0,90 para o fenótipo cartilagem/menisco. | É o mais próximo da Contribuição 3: transferência entre protocolos de aquisição com poucos exames no destino. A diferença é que a articulação continua a mesma. |
| `daneshmand_osteophytes_2024` – Daneshmand *et al.*, 2024 | Detecta osteófitos a partir da morfologia 2D (radiografia) e 3D (RM). A RM teve acurácia balanceada de 0,71 a 0,80 e superou a radiografia em três de quatro compartimentos. | Mostra que a informação 3D da RM acrescenta à imagem 2D, o que justifica a abordagem volumétrica. |
| `guo_cartilage_2024` – Guo *et al.*, 2024 | Quatro redes de segmentação (UNet, UNet++, ResUNet e TransUNet) em 700 RM de quatro bases diferentes medem e graduam a espessura da cartilagem. | Gradua a doença passando pela segmentação, e com dados de equipamentos e parâmetros diferentes, o mesmo desafio de protocolo da Contribuição 3. |
| `panwar_stacking_2024` – Panwar *et al.*, 2024 | Combina quatro redes pré-treinadas (CNN, AlexNet, ResNet34 e ResNet50) por empilhamento para prever a gravidade da OA em RM; acurácia de 99,71%. | Usa pré-treino, mas em cortes 2D. A acurácia próxima de 100% pede leitura do texto completo para entender como treino e teste foram separados. |
| `panwar_vit_2025` – Panwar *et al.*, 2025 | *Vision transformer* com transferência simples para graduar KL em imagens de RM; acurácia de 88%. | Concorda com a Contribuição 2: a transferência simples supera arquiteturas mais complexas. É multiclasse (KL) e 2D. |
| `liao_ohc_2025` – Liao *et al.*, 2025 | Modelo híbrido ResNet e DenseNet para diagnóstico da OA do joelho em RM; AUC média de 0,863 na validação cruzada em 5 partições e acurácia de 91,8% no teste externo. | Mesmo protocolo de validação cruzada da tese, com o teste externo que a tese ainda não tem. |
| `simran_3dcnnvit_2025` – Simran *et al.*, 2025 | Combina CNN 3D e *vision transformer* 3D em volumes de RM para classificar a degeneração da cartilagem em cinco estágios; acurácia de 90,46%. | Abordagem volumétrica como a da tese, mas multiclasse e sem pré-treino descrito no resumo. |
| `margain_cthmaps_2026` – Margain *et al.*, 2026 | Uma U-Net 3D segmenta osso e cartilagem em RM de 4.796 sujeitos da OAI; uma ResNet converte mapas de espessura num escore de gravidade de 0 a 100, com correlação de 0,81 com especialistas. | Usa a mesma coorte, mas passa por segmentação e mapa 2D. A tese classifica o volume diretamente, sem rótulo de segmentação. |
| `moorthy_csfaunet_2026` – Moorthy *et al.*, 2026 | Rede 3D com atenção que segmenta e classifica volumes de RM da OAI, com acurácia de 99,15%. | Volumétrica e na mesma base, mas exige segmentação. O resumo não informa se a separação entre treino e teste foi por paciente, ponto também em aberto na tese. |

## ATM – 10 estudos

| Estudo | Resumo | Relação com a tese |
|---|---|---|
| `choi_opg_2021` – Choi *et al.*, 2021 | ResNet em 1.189 radiografias panorâmicas confirmadas por tomografia de feixe cônico; acurácia de 0,78 depois de retirar os casos indeterminados. | Referência de desempenho na ATM com imagem 2D de raios X. Mostra a dificuldade dos casos limítrofes. |
| `krishnamoorthy_pfrcnn_2023` – Krishnamoorthy e Baskaran, 2023 | Uma GAN gera radiografias panorâmicas sintéticas, e uma Faster R-CNN progressiva com pirâmide de atributos detecta a OA da ATM. | Usa aumento de dados por imagens sintéticas na ATM, um contraponto ao aumento de dados avaliado na Contribuição 2. 2D, periódico de menor impacto. |
| `nozawa_tmj_2024` – Nozawa *et al.*, 2024 | Quatro redes 2D em RM ponderada em densidade de prótons de 200 côndilos, com validação cruzada em 5 partições; a ResNet18 teve AUC de 0,91 a 0,93 e foi comparada a observadores. | Amostra da mesma ordem da prevista para a Contribuição 3 (100 exames) e mesma validação. Usa cortes 2D, sem transferência entre articulações. |
| `lee_bonescan_2025` – Lee *et al.*, 2025 | Variações da VGG16 em cintilografias ósseas de 1.943 pacientes (3.886 ATMs); AUC acima de 0,90 nas imagens de cabeça e pescoço. | Outra modalidade (medicina nuclear). Mostra que a OA da ATM é detectável por aprendizado profundo, mas não trata de RM. |
| `xu_tmjdjd_2026` – Xu *et al.*, 2026 | ResNet101, DenseNet201 e MobileNetV2 classificam doença articular degenerativa da ATM em cortes sagitais e coronais de RM de 104 pacientes, com a tomografia como referência. | Classificação na RM da ATM, mas em 2D e sem pré-treino em outra articulação. |
| `lang_m4tmd_2026` – Lang *et al.*, 2026 | Modelo multitarefa (ResNet50) com RM multissequência e dados clínicos de 765 participantes (1.410 ATMs); AUC de 0,831 para doença degenerativa, 0,913 para deslocamento do disco e 0,961 para derrame. | Maior base de RM da ATM entre os incluídos; a doença degenerativa foi a tarefa mais difícil. Usa vários cortes 2D, não o volume. |
| `lee_tmjfusion_2026` – Lee *et al.*, 2026 | 1.598 pacientes com divisão treino/validação/teste por paciente; compara modelos de tomografia (sagital e coronal) e de RM (T2 e densidade de prótons), combinações dentro da mesma modalidade e fusão tomografia–RM. | Referência de método para a Contribuição 3: separa os dados por paciente, o que a tese precisa garantir, e compara sequências de RM da ATM. |
| `nguyen_opg_2026` – Nguyen *et al.*, 2026 | YOLOv11 localiza a região do côndilo em radiografias panorâmicas de 651 participantes e classifica a ATM em normal ou com OA, com validação cruzada em 5 partições e comparação com especialistas. | Mesma validação cruzada da tese; mostra o desempenho possível com imagem 2D de baixo custo. |
| `iqbal_cbct_2026` – Iqbal, 2026 | Modelo baseado em YOLO em tomografia de feixe cônico de 420 ATMs; AUC de 0,93, sensibilidade de 88,5% e especificidade de 86,8%, comparável a radiologistas experientes. O auxílio do modelo elevou a sensibilidade do leitor júnior de 76,9% para 86,5%. | Compara o modelo com leitores de experiências diferentes, como a comparação com observadores prevista na Contribuição 3. |
| `trivedi_cbct_2026` – Trivedi *et al.*, 2026 | Detecção automática da OA da ATM em tomografia de feixe cônico com aprendizado profundo. O resumo não está disponível nos indexadores. | Ler o texto completo para resumir; por ora, entra como mais um estudo da ATM em tomografia, sem RM. |

## Padrões

1. **Joelho:** estudos volumétricos com a OAI já existem, mas a maioria depende de segmentação ou usa pré-treino 2D adaptado. Só Yeoh *et al.* (2023) se aproxima do pré-treino 3D das Contribuições 1 e 2.
2. **ATM:** quase todos os estudos trabalham com cortes ou projeções 2D (radiografia panorâmica, tomografia ou cortes de RM). Nenhum classifica o volume de RM inteiro.
3. **Transferência entre articulações:** nenhum estudo usa um modelo treinado no joelho como ponto de partida para a ATM. O mais próximo é Zhong *et al.* (2023), que transfere entre protocolos de aquisição da mesma articulação. Essa é a lacuna da Contribuição 3.
4. **Separação por paciente:** entre os resumos, só o de Lee *et al.* (2026) a declara de forma explícita. Vários resultados acima de 99% precisam ser lidos com essa pergunta em mente.
