# htr-catmus-french-2026

> Pipeline de reconnaissance automatique d'écriture manuscrite (HTR) pour les manuscrits médiévaux français (Old/Middle French, XIIIᵉ-XVᵉ siècle), entraîné sur un sous-corpus de [CATMuS Medieval](https://huggingface.co/datasets/CATMuS/medieval).

**Contexte** : Projet MD5 — Module « Vision par ordinateur », Master Data/IA, HETIC, promotion 2026.

**Équipe** :
- [Nom 1] — Responsable technique
- [Nom 2] — Responsable documentation
- [Nom 3] — Responsable expérimentation
- Khadidja [...] — Responsable données

## Statut du projet

🚧 En développement (volet 1/2). Volet 2 (analyse linguistique) prévu pour le module NLP suivant.

## Aperçu rapide

```
Image de manuscrit → Prétraitement → Segmentation layout → Segmentation lignes
                                                                      ↓
                  JSON livrable + PAGE XML ← Agrégation ← HTR (TrOCR fine-tuné LoRA)
```

## Installation

Prérequis : Python ≥ 3.10.

```bash
git clone https://github.com/<org>/htr-catmus-french-2026.git
cd htr-catmus-french-2026
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Reproduire les résultats

```bash
# 1. Télécharger et préparer le sous-corpus (calcule aussi le SHA-256 du test set)
python -m src.data.prepare_subcorpus

# 2. Lancer le prétraitement
python -m src.preprocessing.run

# 3. Évaluer la baseline (TrOCR zéro fine-tuning)
python -m src.htr.baseline

# 4. Fine-tuner TrOCR avec LoRA
python -m src.htr.finetune_trocr --rank 16

# 5. Évaluer sur le test scellé (à n'exécuter qu'une seule fois !)
python -m src.evaluation.run_on_test
```

**Hash SHA-256 du test set** : `<à remplir après scellage>`

## Structure du dépôt

```
.
├── README.md                          # Ce fichier
├── pyproject.toml                     # Dépendances et configuration
├── .gitignore
├── CONVENTIONS_TRANSCRIPTION.md       # Choix éditoriaux
├── DATA_SOURCES.md                    # Sources, licences, attributions
├── MODEL_CARD.md                      # Performances, limitations, données
├── src/                               # Code source
│   ├── data/                          # Chargement et préparation du corpus
│   ├── preprocessing/                 # Correction inclinaison, CLAHE, binarisation
│   ├── segmentation/                  # Segmentation layout et lignes
│   ├── htr/                           # Modèles HTR (TrOCR, Kraken)
│   └── evaluation/                    # CER, WER, bootstrap, McNemar
├── tests/                             # Suite pytest
├── experiments/
│   └── journal.jsonl                  # Journal de toutes les expériences menées
├── dataset_nlp/                       # Jeu de données JSON livrable au Volet 2
└── segmentations/                     # PAGE XML / polygones par ligne
```

## Métriques cibles

| Métrique | Validation | Excellence | Notre meilleur |
|---|---|---|---|
| CER global | < 15 % | < 8 % | `TBD` |
| WER global | < 25 % | < 15 % | `TBD` |
| IoU segmentation | > 0,75 | > 0,85 | `TBD` |
| Taux `needs_review` | < 30 % | < 20 % | `TBD` |

## Citation

Si vous utilisez ce travail, citez-le ainsi :

```bibtex
@misc{htr-catmus-french-2026,
  title  = {HTR Pipeline for Medieval French Manuscripts on CATMuS Medieval},
  author = {[Auteurs]},
  year   = {2026},
  url    = {https://github.com/<org>/htr-catmus-french-2026}
}
```

## Licences

- Code : MIT
- Données CATMuS Medieval : CC-BY 4.0 (Clérice et al., 2024) — voir `DATA_SOURCES.md`
- Modèle TrOCR : voir conditions Microsoft
