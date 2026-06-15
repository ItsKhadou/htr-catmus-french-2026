# Contexte projet — pour Claude Code

Ce fichier est lu automatiquement par Claude Code à chaque session. Il fixe le contexte permanent du projet.

## Projet

**Nom** : `htr-catmus-french-2026`
**Objectif** : pipeline complet de reconnaissance automatique d'écriture manuscrite (HTR) sur manuscrits médiévaux français (Old/Middle French, XIIIᵉ-XVᵉ siècle), à partir d'un sous-corpus de CATMuS Medieval.
**Cadre** : projet académique MD5 — Master Data/IA HETIC, promotion 2026, module Vision par ordinateur. Équipe de 4 étudiants.
**Volet** : Volet 1 sur 2 (le Volet 2 sera l'analyse linguistique NLP des transcriptions produites ici).

## Stack technique

- Python ≥ 3.10
- PyTorch 2.2.2 + Transformers 4.40.1 + PEFT 0.10.0 + Datasets 2.19.0
- TrOCR-base-handwritten (microsoft/) fine-tuné par LoRA
- Optionnel : Kraken pour la segmentation des lignes et comparaison HTR (bonus +1)
- Tests : pytest
- Lint/format : ruff + black

Voir `pyproject.toml` pour les versions exactes — **ne pas les modifier sans raison**.

## Conventions de code

- **Noms de variables, fonctions, classes** : en anglais (`load_subcorpus`, `compute_cer`)
- **Docstrings** : Google style, en français
- **Messages utilisateur, prints, commentaires** : en français
- **Type hints obligatoires** sur les signatures publiques
- **Une fonction = une responsabilité** (≤ 40 lignes idéalement)
- **Pas d'effets de bord cachés** : les fonctions qui écrivent sur disque doivent l'annoncer explicitement (nom commençant par `save_`, `write_`, `export_`)
- **Imports** : `isort` avec ruff (`from __future__` puis stdlib puis third-party puis locaux)
- **Chemins** : `pathlib.Path`, jamais de strings concaténés

Exemple de docstring attendue :

```python
def compute_cer(predictions: list[str], references: list[str]) -> float:
    """Calcule le Character Error Rate global.

    Args:
        predictions: Transcriptions prédites par le modèle.
        references: Transcriptions de référence (ground truth).

    Returns:
        CER global entre 0 et 1+ (peut dépasser 1 si beaucoup d'insertions).

    Raises:
        ValueError: Si les deux listes ont des longueurs différentes.

    Example:
        >>> compute_cer(["hello"], ["hallo"])
        0.2
    """
```

## Contraintes non-négociables

1. **Reproductibilité totale.** Toute source d'aléatoire passe par `src.data.fixer_seeds(42)` appelé en début de script.
2. **Test set scellé.** Le hash SHA-256 du test set est dans `DATA_SOURCES.md` après scellage. Aucun code ne doit lire le test set en dehors de `src/evaluation/run_on_test.py`, qui est exécuté **une seule fois** pour le rendu final.
3. **Journal d'expériences obligatoire.** Tout run d'entraînement ou d'évaluation doit ajouter une ligne JSON dans `experiments/journal.jsonl` (un objet par ligne, JSONL valide).
4. **Tests qui passent.** `pytest tests/` doit toujours passer sur `main`. Pas d'exception.
5. **Pas de commit direct sur `main`.** Toute modification passe par une branche `feature/<nom>` et une PR relue.
6. **Pas de données ou checkpoints dans Git.** Voir `.gitignore`. Les checkpoints vont sur HuggingFace Hub.
7. **Pipeline avant perfection.** Mieux vaut un module bout-à-bout fonctionnel à CER 25 % qu'un composant splendide isolé.

## Conventions de transcription

Voir `CONVENTIONS_TRANSCRIPTION.md`. **Hériter des conventions CATMuS** (semi-diplomatique), ne pas en inventer. Les abréviations sont résolues entre parenthèses : `dñs` → `d(omi)n(u)s`.

## Comment vérifier qu'une modification est bonne

```bash
# 1. Linter
ruff check src/ tests/

# 2. Tests
pytest tests/ -v

# 3. Type checking (optionnel mais bon réflexe)
mypy src/

# 4. Si modification du pipeline HTR, faire tourner la baseline locale et vérifier que le CER ne se dégrade pas
python -m src.htr.baseline --quick  # mode rapide sur 50 lignes
```

## Métriques cibles (rappel du brief)

| Métrique | Seuil validation | Seuil excellence |
|---|---|---|
| CER global | < 15 % | < 8 % |
| WER global | < 25 % | < 15 % |
| IoU segmentation | > 0,75 | > 0,85 |
| Taux `needs_review` | < 30 % | < 20 % |

## Ce que Claude Code NE doit pas faire

- ❌ Modifier le test set ou son hash après scellage
- ❌ Toucher au split `gen_split` natif de CATMuS (pas de re-split maison)
- ❌ Mettre les checkpoints ou les données dans Git
- ❌ Ajouter des dépendances sans mettre à jour `pyproject.toml`
- ❌ Supprimer ou réécrire les conventions de transcription sans validation explicite de l'équipe
- ❌ Évaluer sur le test set en dehors du script final dédié

## Ce que Claude Code peut faire librement

- ✅ Refactoriser, factoriser, améliorer la lisibilité
- ✅ Ajouter des tests (toujours apprécié)
- ✅ Compléter les docstrings et les exemples
- ✅ Proposer des optimisations (mais expliquer le compromis)
- ✅ Mettre à jour la documentation au fil des modifications
- ✅ Logger chaque run dans le journal d'expériences

## Documentation de référence

- `README.md` — guide d'installation et de reproduction
- `CONVENTIONS_TRANSCRIPTION.md` — choix éditoriaux
- `DATA_SOURCES.md` — sources, licences, hash SHA-256
- `MODEL_CARD.md` — performances et limitations
- Notebook `notebook_baseline_catmus.ipynb` (à la racine du kit, hors repo) — référence de la baseline à reproduire en CLI

## Workflow Git attendu

```bash
git checkout -b feature/nom-de-la-feature
# ... travail ...
ruff check src/ tests/
pytest tests/ -v
git add -A
git commit -m "feat: description courte"
git push origin feature/nom-de-la-feature
# Ouvrir une PR sur GitHub, demander une revue
```

Messages de commit : préfixer par `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
