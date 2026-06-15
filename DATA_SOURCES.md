# Sources des données et attributions

## Corpus d'entraînement et d'évaluation

### CATMuS Medieval

**Description** : Dataset normalisé d'entraînement pour la reconnaissance d'écriture manuscrite sur manuscrits médiévaux en écriture latine (VIIIᵉ-XVIᵉ siècle, 10 langues, 200+ manuscrits).

**Source** : <https://huggingface.co/datasets/CATMuS/medieval>

**Licence** : CC-BY 4.0

**Sous-corpus retenu pour ce projet** : Old French + Middle French, XIIIᵉ-XVᵉ siècle, split natif `gen_split`.

**Hash SHA-256 du test set scellé** : `<à remplir après scellage>`

**Citation** :

```bibtex
@unpublished{clerice2024catmus,
  title  = {CATMuS Medieval: A multilingual large-scale cross-century dataset in Latin script for handwritten text recognition and beyond},
  author = {Cl{\'e}rice, Thibault and Pinche, Ariane and Vlachou-Efstathiou, Malamatenia and Chagu{\'e}, Alix and Camps, Jean-Baptiste and Gille-Levenson, Matthias and Brisville-Fertin, Olivier and Fischer, Franz and Gervers, Michaels and Boutreux, Agn{\`e}s and Manton, Avery and Gabay, Simon and O'Connor, Patricia and Haverals, Wouter and Kestemont, Mike and Vandyck, Caroline},
  year   = {2024},
  note   = {HAL inria-04453952}
}
```

### CATMuS Medieval Segmentation (optionnel, pour les polygones)

**Description** : Sous-ensemble de CATMuS avec annotations de structure de page (SegmOnto).

**Source** : <https://huggingface.co/datasets/CATMuS/medieval-segmentation>

**Licence** : CC-BY 4.0

**Usage dans le projet** : référence pour la production des polygones de lignes (IoU > 0,75).

---

## Modèles pré-entraînés

### TrOCR — Base Handwritten

**Description** : Modèle transformer encoder-decoder pour la reconnaissance d'écriture manuscrite, pré-entraîné par Microsoft.

**Source** : <https://huggingface.co/microsoft/trocr-base-handwritten>

**Licence** : MIT (vérifier conditions d'usage Microsoft)

**Usage dans le projet** : modèle de base, fine-tuné par LoRA sur le sous-corpus CATMuS.

**Citation** :

```bibtex
@article{li2021trocr,
  title   = {TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models},
  author  = {Li, Minghao and Lv, Tengchao and Cui, Lei and Lu, Yijuan and Florencio, Dinei and Zhang, Cha and Li, Zhoujun and Wei, Furu},
  journal = {arXiv preprint arXiv:2109.10282},
  year    = {2021}
}
```

### Kraken (optionnel, pour le bonus comparaison d'architectures)

**Description** : Moteur HTR open-source spécialisé pour les manuscrits historiques.

**Source** : <https://kraken.re>

**Modèles HTR-United utilisés** : `<à remplir>`

**Licence** : Apache 2.0

**Citation** : `<à compléter avec la référence du modèle spécifique>`

### Segment Anything Model (optionnel, segmentation layout)

**Description** : Modèle de segmentation universelle de Meta.

**Source** : <https://github.com/facebookresearch/segment-anything>

**Licence** : Apache 2.0

---

## Autres ressources documentaires

### HTR-United

**Source** : <https://htr-united.github.io>

**Usage** : catalogue de référence pour identifier des modèles et corpus complémentaires.

### Documentation Kraken

**Source** : <https://kraken.re>

### Documentation eScriptorium

**Source** : <https://escriptorium.fr>

---

## Conformité licences

Toutes les sources utilisées sont sous licence libre permettant la recherche et la publication académique. Les modèles pré-entraînés respectent les conditions d'usage non commercial / recherche.

| Source | Licence | Usage commercial | Usage projet OK |
|---|---|---|---|
| CATMuS Medieval | CC-BY 4.0 | Oui (avec attribution) | ✓ |
| CATMuS Segmentation | CC-BY 4.0 | Oui (avec attribution) | ✓ |
| TrOCR | MIT | Oui | ✓ |
| Kraken | Apache 2.0 | Oui | ✓ |
| SAM | Apache 2.0 | Oui | ✓ |
