# Plan détaillé de l'article scientifique

Article format ArXiv : 8-12 pages, police 11 pt, interligne simple, marges 2 cm.

**Principe directeur** : commencer la rédaction en semaine 1, **pas** en fin de projet. Les sections « Introduction », « État de l'art » et « Données » peuvent être écrites tout de suite ; les sections « Résultats » et « Discussion » se construisent au fil des expériences.

## Section 1 — Résumé (Abstract, ~200 mots)

**Quand** : à écrire en tout dernier, après que les résultats finaux soient figés.

**Contenu attendu :**
1. Une phrase de contexte (transcription automatique de manuscrits médiévaux français, enjeu de mise à l'échelle)
2. Une phrase sur le problème (besoin de modèles spécialisés sur des corpus diversifiés)
3. Deux à trois phrases sur l'approche (sous-corpus de CATMuS Medieval, fine-tuning TrOCR avec LoRA, pipeline de segmentation, agrégation)
4. Une phrase sur les résultats quantitatifs principaux (CER X.X % ± Y.Y, WER Z.Z %)
5. Une phrase de conclusion / contribution

**Astuce** : le rédiger comme un mini-article complet. Si un évaluateur ne lit que l'abstract, doit-il comprendre ce que vous avez fait et avec quel résultat ? Oui.

---

## Section 2 — Introduction (~1 page)

**Quand** : semaine 1, à raffiner tout au long du projet.

**Plan suggéré :**

**Paragraphe 1 — Mise en contexte large (5-6 phrases)**
Numérisation massive des fonds patrimoniaux (BnF, IIIF), volumes considérables d'images mais absence de transcriptions. Citer les chiffres du brief : 380 000 manuscrits BnF, 11 millions de docs sur Gallica, coût prohibitif de la transcription manuelle.

**Paragraphe 2 — Émergence du HTR (5-6 phrases)**
Domaine HTR, projets fondateurs (CREMMA, GalliCorpora, HTR-United), arrivée de CATMuS comme dataset normalisé. Mentionner CoMMA pour montrer l'actualité.

**Paragraphe 3 — Verrou scientifique (4-5 phrases)**
Manque de données d'entraînement annotées pour des écritures particulières. Variabilité inter-scripteur, abréviations, conventions de transcription divergentes.

**Paragraphe 4 — Contributions du projet (4-5 phrases en bullets ou liste)**
Annoncer clairement :
- Sous-corpus CATMuS Old/Middle French XIIIᵉ-XVᵉ
- Pipeline reproductible bout en bout (prétraitement, segmentation, HTR, agrégation)
- Comparaison TrOCR fine-tuné (LoRA) vs Kraken (si fait pour le bonus)
- Évaluation rigoureuse (CER, WER, IC bootstrap, IAA)
- Jeu de données livrable pour le Volet 2 NLP

**Paragraphe 5 — Structure de l'article (3-4 phrases)**
« La section 2 présente l'état de l'art… »

---

## Section 3 — État de l'art (~1,5 page)

**Quand** : semaine 1-2.

**Sous-sections :**

**3.1 Architectures HTR**
- Approches CNN+RNN+CTC (Kraken et son moteur, basé sur de la convolution + BLSTM + CTC)
- Approches transformer encoder-decoder (TrOCR de Microsoft, Donut)
- Approches vision foundation models (DINO, SAM pour la segmentation)
- Citer 3-5 références par approche

**3.2 Jeux de données médiévaux**
- HTR-United (catalogue)
- CREMMA Médiéval (XIIIᵉ-XVᵉ français)
- GalliCorpora
- CATMuS Medieval (en détail puisque c'est votre source — citer Clérice et al. 2024)
- e-NDP, HIMANIS

**3.3 Métriques d'évaluation**
- CER (Character Error Rate) — définition, lien avec Levenshtein
- WER (Word Error Rate) — limitations en contexte médiéval (segmentation lexicale)
- IAA (Inter-Annotator Agreement) — plafond irréductible
- Intervalles de confiance bootstrap

**3.4 Positionnement de la contribution**
Une demi-page pour situer ce que vous faites par rapport à l'existant. *Vous ne créez pas un nouveau dataset, vous ne proposez pas une nouvelle architecture — votre contribution est un pipeline reproductible et une analyse fine sur un sous-corpus normalisé.* Ne pas survendre.

---

## Section 4 — Données (~1 page)

**Quand** : semaine 1-2, dès que le sous-corpus est figé.

**Contenu :**

**4.1 Source**
CATMuS Medieval. 200+ manuscrits, 10 langues, plus de 160 000 lignes, 5 millions de caractères, du VIIIᵉ au XVIᵉ siècle. Licence CC-BY 4.0. Citer le papier de Clérice et al.

**4.2 Sélection du sous-corpus**
Critères de filtrage explicites :
- Langues : Old French + Middle French
- Siècles : XIIIᵉ-XVᵉ
- Tout type d'écriture conservé pour la variabilité

Tableau récapitulatif :

| Critère | Filtre |
|---|---|
| Langue | `lang ∈ {fro, frm}` (codes ISO) |
| Siècle | `13 ≤ century ≤ 15` |
| Split | `gen_split` natif CATMuS (90/5/5 par manuscrit) |

**4.3 Statistiques descriptives**
- Nombre total de lignes par split
- Distribution par siècle (graphique)
- Distribution par script paléographique
- Longueur moyenne des lignes (en caractères)
- Vocabulaire et fréquence

**4.4 Conventions de transcription**
Référencer `CONVENTIONS_TRANSCRIPTION.md`. Préciser que vous héritez des conventions CATMuS (transcription semi-diplomatique).

**4.5 Hash SHA-256 du test set**
Donner le hash dans l'article — c'est la garantie de non-contamination.

---

## Section 5 — Méthodes (~2 pages)

**Quand** : au fil de l'implémentation (semaines 2-4).

**Sous-sections :**

**5.1 Pipeline d'ensemble**
Schéma global du pipeline (figure à insérer) :
`Image brute → Prétraitement → Segmentation layout → Segmentation lignes → HTR → Post-traitement → JSON de sortie`

**5.2 Prétraitement**
- Correction d'inclinaison
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Binarisation Sauvola
- Paramètres exacts (taille de fenêtre, k, etc.)

**5.3 Segmentation**
- Architecture choisie (Kraken BLLA, ou SAM, ou dhSegment)
- Modèle pré-entraîné utilisé
- Métriques de qualité (IoU)

**5.4 Modèle HTR**
- Architecture : TrOCR-base-handwritten
- Fine-tuning par LoRA : r=8 puis r=16, rang justifié
- Optimiseur, learning rate, scheduler
- Batch size, nombre d'epochs
- Augmentations de données (déformation élastique, contraste, bruit)
- Early stopping sur val CER

**5.5 Agrégation (si Kraken + TrOCR)**
- Algorithme de vote pondéré
- Calibration des scores de confiance

**5.6 Évaluation**
- Métrique principale : CER (formule)
- Métriques complémentaires : WER, IC bootstrap (N=1000)
- Test de McNemar pour la comparaison de variantes
- Calcul du taux `needs_review`

---

## Section 6 — Résultats (~1,5 page)

**Quand** : semaine 4-5.

**Plan :**

**6.1 Baseline zéro fine-tuning**
TrOCR-base-handwritten sans fine-tuning sur val. CER attendu : très mauvais (>80 %), c'est attendu — c'est la justification du fine-tuning.

**6.2 Résultats principaux**
Tableau :

| Modèle | CER val | CER test | WER test | IC bootstrap 95 % |
|---|---|---|---|---|
| Baseline TrOCR (zéro-shot) | X.X % | — | — | — |
| TrOCR LoRA r=8 | X.X % | — | — | — |
| TrOCR LoRA r=16 | X.X % | X.X % | X.X % | [X.X, X.X] |
| Kraken fine-tuné (si) | X.X % | X.X % | X.X % | [X.X, X.X] |
| Agrégation (si) | — | X.X % | X.X % | [X.X, X.X] |

**6.3 Courbes d'apprentissage**
Figure : CER val en fonction des epochs, pour chaque variante.

**6.4 Ablation**
Tableau : impact de chaque composant (avec / sans augmentation, r=8 vs r=16, etc.).

**6.5 Analyse des erreurs résiduelles**
- Distribution des erreurs par type (substitution, insertion, suppression)
- Erreurs par siècle (les écritures anciennes sont-elles plus dures ?)
- Erreurs par longueur de ligne
- Exemples qualitatifs (5-10 lignes avec image + transcription correcte + prédiction)

**6.6 Taux `needs_review`**
Pourcentage de lignes flaguées et critères utilisés.

**6.7 IoU segmentation**
Si vous avez fait la segmentation : IoU moyen, par type de page.

---

## Section 7 — Discussion (~1 page)

**Quand** : semaine 5.

**Plan :**

**7.1 Biais de représentation du corpus** (section éthique — bonus +1)
- Quels siècles, langues, scripts sont sur/sous-représentés
- Conséquence sur la généralisation
- Recommandations pour un corpus plus équilibré

**7.2 Limitations méthodologiques**
- Petite taille du sous-corpus
- Hyperparamètres peu explorés
- Métriques ne capturent pas l'usage final

**7.3 Comparaison avec la littérature**
- Vos chiffres vs ceux rapportés dans le papier CATMuS
- Vos chiffres vs ceux rapportés par CREMMA, HTR-United

**7.4 Implications pour le Volet 2**
- Qualité des transcriptions et impact attendu sur le NLP
- Conventions à respecter en aval

---

## Section 8 — Conclusion et travaux futurs (~0,5 page)

**Quand** : tout dernier.

**Contenu :**
- Résumé des contributions (3-4 phrases)
- Lien avec le Volet 2 (1-2 phrases)
- Pistes ouvertes : autres architectures, fusion multi-modèles, active learning, transfert vers d'autres langues

---

## Section 9 — Références

**Format** : APA ou BibTeX (le brief accepte les deux).

**Références minimales à inclure :**
- Clérice et al. 2024 (CATMuS Medieval) — incontournable
- Li et al. 2021 (TrOCR)
- Kiessling et al. (Kraken)
- Pinche et al. (CREMMA / GalliCorpora)
- Le papier original LoRA (Hu et al. 2021)
- Méthodes : Sauvola, CLAHE, U-Net (Ronneberger), SAM (Kirillov)
- Métriques : Levenshtein, CER en HTR (Sánchez, Romero…)

Cibler **30-50 références**, pas plus.

---

## Section 10 — Annexes

**Contenu :**
- Exemples de transcriptions (image + référence + prédiction)
- Courbes de calibration des scores de confiance
- Description complète du data contract JSON
- Hyperparamètres détaillés
- Commandes exactes pour reproduire les résultats principaux

---

## Calendrier de rédaction

| Semaine | Sections à drafter |
|---|---|
| Semaine 1 | Introduction (paragraphes 1-3), État de l'art (3.1-3.3), Données (4.1-4.4) |
| Semaine 2 | Données (4.5 dès que test set scellé), Méthodes (5.1-5.4) |
| Semaine 3 | Méthodes (suite), premières figures d'ablation |
| Semaine 4 | Résultats principaux, tableaux |
| Semaine 5 | Discussion, Conclusion, Abstract, Annexes, relecture |

## Outils recommandés

- **Rédaction** : Overleaf (LaTeX collaboratif) ou Notion / Google Docs si vous préférez Markdown
- **Bibliographie** : Zotero avec export BibTeX
- **Figures** : Matplotlib pour les courbes, draw.io ou Excalidraw pour les schémas de pipeline
