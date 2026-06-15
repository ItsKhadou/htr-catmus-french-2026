"""Module de segmentation.

Responsabilité : détecter les zones de texte, illustrations, marges, puis
extraire les lignes individuelles avec polygones.

Sous-modules à implémenter :
    - layout.py       : segmentation de structure de page (SAM ou dhSegment)
    - lines.py        : extraction des lignes avec Kraken BLLA
    - polygons.py     : production des polygones (PAGE XML ou JSON)
    - reading_order.py : ordre de lecture pour pages multi-colonnes
"""
