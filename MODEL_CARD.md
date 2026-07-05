# Model Card — HTR CATMuS French XIII-XV

## Vue d'ensemble

- **Nom** : htr-catmus-french-2026
- **Base** : microsoft/trocr-base-handwritten
- **Fine-tuning** : LoRA (r=8, α=16)
- **Sous-corpus** : Old/Middle French, XIIIᵉ-XVᵉ siècle
- **Split** : train/val/test = 40520/2265/2265
- **Test SHA-256** : `209328c0af25635caec7270ee5f07b8b4d0b7d3e39e506eb84a8ff83212de317`

## Performances

| Métrique | Baseline (zéro-shot val) | Fine-tuné (test scellé) |
|---|---|---|
| CER | 67.93 % | **23.29 %** |
| WER | 103.01 % | **56.24 %** |
| IC 95 % (bootstrap N=1000) | — | [22.14 %, 24.47 %] |

Amélioration : **+44.64 points** de CER.

## Hyperparamètres

- Learning rate : 5e-05
- Batch size effectif : 16
- Epochs : 2
- Warmup ratio : 0.1
- Précision : fp16
- Early stopping patience : 3
- Seed : 42

## Limitations

- Tokenizer TrOCR (base GPT-2 anglais) sous-optimal pour les caractères médiévaux
- Sous-corpus limité aux XIIIᵉ-XVᵉ (pas de généralisation aux siècles antérieurs)
- Confidence basée sur une heuristique simple (à raffiner via generate scores)
- Pas de gestion explicite des marginalia et abréviations non résolues

Voir article scientifique pour discussion détaillée.
