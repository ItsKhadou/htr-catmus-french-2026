"""Module d'évaluation.

Responsabilité : calculer les métriques de qualité du pipeline.

Sous-modules à implémenter :
    - metrics.py    : CER, WER (Levenshtein normalisé)
    - bootstrap.py  : intervalles de confiance par rééchantillonnage (N=1000)
    - mcnemar.py    : test de McNemar pour comparer deux variantes
    - iou.py        : IoU pour la qualité de segmentation
    - run_on_test.py : évaluation finale sur le test scellé (UN SEUL run autorisé !)
"""
