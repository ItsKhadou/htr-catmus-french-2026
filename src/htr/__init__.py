"""Module HTR — Reconnaissance d'écriture manuscrite.

Responsabilité : charger, fine-tuner et utiliser les modèles HTR.

Sous-modules à implémenter :
    - baseline.py        : évaluation zéro fine-tuning de TrOCR
    - finetune_trocr.py  : fine-tuning TrOCR par LoRA (r=8, r=16)
    - finetune_kraken.py : fine-tuning Kraken (optionnel, bonus +1)
    - inference.py       : inférence batch sur un dataset
    - aggregation.py     : vote pondéré Needleman-Wunsch (si plusieurs modèles)
"""
