# Model Card — HTR CATMuS French XIII-XV

> ⚠️ Document à compléter au fil du projet. Les placeholders `<à remplir>` doivent disparaître avant le rendu.

## Vue d'ensemble

- **Nom du modèle** : `htr-catmus-french-2026`
- **Architecture de base** : TrOCR-base-handwritten (Microsoft)
- **Méthode de fine-tuning** : LoRA (r=`<à remplir>`)
- **Tâche** : reconnaissance d'écriture manuscrite (image-to-text) au niveau ligne
- **Langues** : Old French, Middle French
- **Période couverte** : XIIIᵉ-XVᵉ siècle
- **Auteurs** : Équipe MD5, HETIC, promotion 2026
- **Date** : `<à remplir>`
- **Version** : 0.1.0
- **Licence** : MIT (code) / CC-BY 4.0 (données dérivées)

## Usage prévu

### Cas d'usage principal

Transcription automatique de lignes de texte extraites de manuscrits médiévaux français du XIIIᵉ au XVᵉ siècle, dans un pipeline de recherche en humanités numériques.

### Cas d'usage secondaires

- Pré-transcription pour validation humaine en eScriptorium ou Kraken
- Préparation de jeu de données NLP pour le Volet 2 du projet

### Cas d'usage hors périmètre

- ❌ Manuscrits hors période (avant XIIIᵉ ou après XVIᵉ siècle)
- ❌ Langues autres que le français médiéval (latin pur, néerlandais, etc.)
- ❌ Documents tapuscrits ou imprimés
- ❌ Usage juridique ou commercial sans validation humaine

## Données d'entraînement

- **Source** : sous-corpus de CATMuS Medieval (voir `DATA_SOURCES.md`)
- **Filtrage** : Old/Middle French, XIIIᵉ-XVᵉ siècle, split natif `gen_split`
- **Taille** : `<X lignes train, Y val, Z test à remplir>`
- **Hash SHA-256 du test set** : `<à remplir>`

## Performances

### Résultats sur le test scellé

| Métrique | Valeur | IC 95 % bootstrap |
|---|---|---|
| CER global | `<à remplir>` | `[<à remplir>]` |
| WER global | `<à remplir>` | `[<à remplir>]` |
| Taux `needs_review` | `<à remplir>` | — |
| IoU segmentation moyen | `<à remplir>` | — |

### Comparaison avec la baseline

| Modèle | CER val | CER test |
|---|---|---|
| TrOCR-base-handwritten (zéro-shot) | `<à remplir>` | — |
| **Notre modèle (fine-tuné)** | **`<à remplir>`** | **`<à remplir>`** |

## Limitations connues

- **Biais chronologique** : sur-représentation des XIVᵉ-XVᵉ siècles dans CATMuS
- **Biais paléographique** : certains scripts (cursives très ornementées) restent difficiles
- **Taille du corpus** : sous-corpus filtré relativement petit, généralisation limitée
- **Abréviations non vues** : performance dégradée sur les systèmes abréviatifs idiosyncrasiques

## Considérations éthiques

- **Reproduction** : modèle entraîné sur données publiques sous licence libre
- **Représentativité** : voir la section discussion de l'article pour l'analyse des biais
- **Usage humain conseillé** : sortie du modèle à valider par un paléographe avant publication scientifique

## Comment utiliser

```python
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from peft import PeftModel
from PIL import Image

base_model_id = "microsoft/trocr-base-handwritten"
lora_adapter_id = "<votre-org>/htr-catmus-french-2026"

processor = TrOCRProcessor.from_pretrained(base_model_id)
base_model = VisionEncoderDecoderModel.from_pretrained(base_model_id)
model = PeftModel.from_pretrained(base_model, lora_adapter_id)
model.eval()

image = Image.open("ligne_de_manuscrit.png").convert("RGB")
pixel_values = processor(images=image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values, max_length=128)
text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(text)
```

## Citation

```bibtex
@misc{htr-catmus-french-2026,
  title  = {HTR Pipeline for Medieval French Manuscripts on CATMuS Medieval},
  author = {[Auteurs à remplir]},
  year   = {2026},
  url    = {https://github.com/<org>/htr-catmus-french-2026}
}
```
