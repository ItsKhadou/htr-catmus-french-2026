"""Module de prétraitement des images.

Responsabilité : préparer les images de manuscrits pour l'entrée du modèle HTR.

Sous-modules à implémenter :
    - deskew.py        : correction d'inclinaison (Hough transform ou projection)
    - contrast.py      : amélioration de contraste par CLAHE
    - binarize.py      : binarisation adaptative Sauvola
    - pipeline.py      : chaîne complète paramétrable et reproductible

Note :
    Le CATMuS dataset fournit déjà des crops de lignes. Le prétraitement est
    surtout pertinent pour le pipeline d'inférence sur de nouveaux manuscrits.
"""
