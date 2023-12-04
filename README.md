# Projet GEN 2023

## Installation

***TODO***
1.Faire les mesures énergétiques avec différents outils(Shelly,Carbon,etc.) pour vérifier l'authencité des outils.
2.En changeant l'algorithme du learning, on trouvera des compromises entre la consommation et la preformance.


<details>
<summary><b>Intelligence Artificielle Embarquée : Développement de modèles locaux adaptés à la Surveillance de Santé des Structures</b></summary>


## Contexte

Le domaine de l’intelligence artificielle (IA), grâce aux progrès réalisés dans la microélectronique,  se déploie maintenant au-delà du calcul haute performance. Il est à présent envisageable de développer des solutions où une partie des calculs dévolue aux nœuds les plus performants du cloud sont délocalisés vers la frontière du réseau \[1\] (ce qu’on appelle le « edge computing »). Les solutions d’IA s’installent progressivement sur des  nœuds relativement puissants que l’on qualifie de « high-end devices »\[2\] de l’IoT. Alors qu’elles se cantonnent majoritairement à un rôle d’inférence sur de modèles entraînés par les centres de calculs, des avancés récentes ouvre la voie à un entraînement in situ limitant ainsi l’usage de la bande passante en laissant apparaître une adaptation localisée des solutions.

L’objectif de ce projet est d’étudier la mise en place d’intelligence artificielle pour de la surveillance de bâtiment, structures et machines mécaniques afin de diagnostiquer leur santé (appelé « Structural Health Monitoring » ou SHM en anglais) \[3\]. Les signaux physiques issus de ces structures (principalement des vibrations mécaniques collectées par le biais de capteurs piézoélectriques) sont qualifiés de séries temporelles. Les relevés obtenues sont généralement peu diversifiés au regard des standards de l’IA et nécessite une famille de solutions spécifiques dédiées.

Il s’agira donc d’implémenter, d’entraîner, tester des solutions d’IA qui permettront de caractériser l’état de santé d’une structure mécanique constituée de matériaux hétérogènes (métal et composite), d’en détecter les éventuels défaillances, d’identifier la nature de ces dernières (fissure, corrosion, déformation,…) et leur localisations. L’intérêt de la démarche est de comparer les algorithmes existants pour établir le compromis idéal entre les performances des solutions techniques identifiées et les contraintes matérielles de l’IA en bordure de réseau.

## Déroulé du travail

Le travail se fera en trois étapes :
 - Étude bibliographique et choix d’algorithmes compatibles avec les contraintes matérielle de l’IA embarqué (capacité de mémoire réduite, puissance de calcul limitée) sur la base d’articles fournis \[4\]\[5\]\[6\] :  octobre 2023
 - Développement et entraînement hors ligne de modèles sur la base de jeux de données vibratoires fournies par un laboratoire partenaire, le LTDS (laboratoire de mécanique située sur Centrale Lyon) :  novembre → mi-décembre 2023
 - Implémentation et caractérisation des performances des modèles sur une plateforme matérielle à définir parmi : DSP, FPGA ou Jetson Nano :  mi-décembre 2023 →	janvier 2024

## Compétences développées

- Implémenter des solutions d’intelligence artificielle embarquée : identification d’algorithmes correspondant au cahier des charges, entraînement du modèle et programmation embarquée
- Programmer des “high-end devices” de l’IoT , en particulier la plateforme matérielle Jetson Nano
- Mettre en place un protocole expérimental de mesure et de validation d’hypothèse
- Pratiquer les langages de programmation C, C++ et python
- Une connaissance préalable des frameworks de  Machine Learning TensorFlow ou PyTorch est appréciable
- Mettre en œuvre une démarche de recherche appliquée

## Bibliographie

\[1\]	L. Martin Wisniewski, J.-M. Bec, G. Boguszewski, et A. Gamatié, « Hardware Solutions for Low-Power Smart Edge Computing », JLPEA, vol. 12, no 4, p. 61, nov. 2022, doi: 10.3390/jlpea12040061.

\[2\]	M. O. Ojo, S. Giordano, G. Procissi, et I. N. Seitanidis, « A Review of Low-End, Middle-End, and High-End Iot Devices », IEEE Access, vol. 6, p. 70528‑70554, 2018, doi: 10.1109/ACCESS.2018.2879615.

\[3\]	A. Malekloo, E. Ozer, M. AlHamaydeh, et M. Girolami, « Machine learning and structural health monitoring overview with emerging technology and high-dimensional data source highlights », Structural Health Monitoring, vol. 21, no 4, p. 1906‑1955, juill. 2022, doi: 10.1177/14759217211036880.

\[4\]	O. Mey et D. Neufeld, « Explainable AI Algorithms for Vibration Data-Based Fault Detection: Use Case-Adadpted Methods and Critical Evaluation », Sensors, vol. 22, no 23, p. 9037, nov. 2022, doi: 10.3390/s22239037.

\[5\]	D. Liu, Z. Tang, Y. Bao, et H. Li, « Machine‐learning‐based methods for output‐only structural modal identification », Struct Control Health Monit, vol. 28, no 12, déc. 2021, doi: 10.1002/stc.2843.

\[6\]	F. Schmidt, F. Chabi, et J.-F. Bercher, « SHM analysis for damage detection using time series analysis methods », in Life-Cycle of Structures and Infrastructure Systems, 1re éd.London: CRC Press, 2023, p. 2227‑2234. doi: 10.1201/9781003323020-272.

</details>
