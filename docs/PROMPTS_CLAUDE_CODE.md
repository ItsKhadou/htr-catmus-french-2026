# Prompts pour Claude Code — séquence guidée

Ce fichier contient une **séquence de prompts à donner à Claude Code dans l'ordre**. Chaque prompt est borné : Claude Code fait UNE chose à la fois, tu vérifies que ça marche, tu commit, tu passes au suivant. C'est plus fiable que de demander tout d'un coup.

## Avant de commencer

1. **Place `CLAUDE.md` à la racine du repo.** Claude Code le lira automatiquement à chaque session.
2. **Ouvre le notebook `notebook_baseline_catmus.ipynb` en parallèle** : il sert de référence pour les premiers prompts.
3. **Configure ton environnement** :
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   pytest tests/ -v  # tout doit passer (14 tests)
   ```
4. **Token HuggingFace** : `huggingface-cli login` (pour les checkpoints).

## Comment donner les prompts à Claude Code

Dans VSCode, ouvre la sidebar Claude Code et colle le prompt. Avant chaque prompt, vérifie que tu es sur une branche feature (pas main) :

```bash
git checkout -b feature/<nom-de-la-feature>
```

Après chaque prompt complété par Claude Code :

```bash
pytest tests/ -v     # vérifie que rien n'est cassé
ruff check src/      # lint
git diff             # relis les changements
git add -A && git commit -m "feat: ..."
```

---

## PROMPT 1 — Refactoriser le notebook en module de préparation du corpus

**Branche** : `feature/data-prepare-subcorpus`

```
Tu travailles sur le projet HTR CATMuS. Lis `CLAUDE.md` à la racine pour le contexte.

OBJECTIF : refactoriser la logique de chargement et filtrage de CATMuS Medieval du notebook `notebook_baseline_catmus.ipynb` (à la racine du dossier parent, hors repo) en un module Python propre, testé et utilisable en CLI.

LIVRABLES :

1. Crée `src/data/prepare_subcorpus.py` avec :
   - Une fonction `load_catmus_medieval() -> DatasetDict` qui charge le dataset depuis HuggingFace
   - Une fonction `filter_subcorpus(ds, languages: list[str], centuries: list[int]) -> dict[str, Dataset]` qui retourne un dict avec les clés "train", "val", "test" issues du split natif `gen_split`
   - Une fonction `print_distribution(splits: dict[str, Dataset]) -> None` qui affiche la distribution par siècle et par langue
   - Un main `if __name__ == "__main__":` exécutable via `python -m src.data.prepare_subcorpus` qui exécute tout l'enchaînement et imprime un récapitulatif

2. Crée `src/data/hashing.py` avec :
   - Une fonction `compute_test_set_hash(test_ds: Dataset, text_col: str = "text") -> str` qui calcule le SHA-256 du test set (textes triés concaténés par \n, encodés en UTF-8)
   - Sa docstring doit expliquer pourquoi on hash les textes triés (stabilité, indépendance à l'ordre)

3. Ajoute des tests dans `tests/test_data.py` :
   - `test_filter_subcorpus_returns_three_splits` (mock le dataset ou utilise un petit échantillon)
   - `test_compute_test_set_hash_is_deterministic` (même input = même hash)
   - `test_compute_test_set_hash_is_order_independent` (deux DS avec mêmes textes dans ordres différents donnent le même hash)

4. Mets à jour `src/data/__init__.py` pour exposer les fonctions principales

CONTRAINTES :
- Type hints partout
- Docstrings Google style en français
- Imports triés (stdlib, third-party, locaux)
- Pas de print en plein milieu d'une fonction métier (sauf dans `print_distribution`) — utilise des returns
- Les filtres `TARGET_LANGUAGES` et `TARGET_CENTURIES` du notebook sont des paramètres, pas des globales

CRITÈRE DE SUCCÈS :
- `python -m src.data.prepare_subcorpus` tourne sans erreur et affiche la distribution
- `pytest tests/test_data.py -v` passe
- `ruff check src/data tests/test_data.py` est clean
```

---

## PROMPT 2 — Module de métriques (CER, WER)

**Branche** : `feature/evaluation-metrics`

```
Lis `CLAUDE.md`.

OBJECTIF : créer un module de métriques d'évaluation HTR, testé et documenté.

LIVRABLES :

1. Crée `src/evaluation/metrics.py` avec :
   - `compute_cer(predictions: list[str], references: list[str]) -> float` — Character Error Rate global (somme des distances Levenshtein / somme des longueurs des références)
   - `compute_wer(predictions: list[str], references: list[str]) -> float` — Word Error Rate (idem au niveau mots après split sur whitespace)
   - `compute_cer_per_sample(predictions, references) -> list[float]` — CER par échantillon (utile pour bootstrap et analyse d'erreurs)
   - Toutes lèvent `ValueError` si les listes ont des longueurs différentes
   - Toutes utilisent `editdistance` pour la distance Levenshtein

2. Crée `tests/test_metrics.py` avec au moins ces cas :
   - CER 0 si prédiction == référence (identité)
   - CER positif sur exemple connu : `compute_cer(["hello"], ["hallo"]) == 0.2`
   - WER 0 si prédiction == référence (identité)
   - ValueError si listes de longueurs différentes
   - Robuste à liste vide ou références vides

CONTRAINTES :
- Type hints
- Docstrings en français
- Numpy/torch optionnels — préférer Python pur pour la robustesse

CRITÈRE DE SUCCÈS :
- `pytest tests/test_metrics.py -v` passe (au moins 6 tests)
- `ruff check src/evaluation tests/test_metrics.py` clean
```

---

## PROMPT 3 — Baseline TrOCR zéro fine-tuning en CLI

**Branche** : `feature/htr-baseline`

```
Lis `CLAUDE.md`. Tu peux te référer aux modules `src/data/` et `src/evaluation/` que tu as déjà créés.

OBJECTIF : transformer la baseline du notebook en un script CLI qui produit le même CER, journalisé dans `experiments/journal.jsonl`.

LIVRABLES :

1. Crée `src/htr/baseline.py` avec :
   - Une fonction `run_baseline(splits: dict[str, Dataset], sample_size: int = 100, model_name: str = "microsoft/trocr-base-handwritten") -> dict` qui :
     - Charge TrOCR et son processor
     - Échantillonne `sample_size` lignes du split val
     - Lance l'inférence
     - Calcule CER et WER via `src.evaluation.metrics`
     - Retourne un dict avec `cer`, `wer`, `sample_size`, `duration_seconds`, `device`
   - Une fonction `log_run_to_journal(entry: dict, journal_path: Path) -> None` qui append une ligne JSON à `experiments/journal.jsonl`
   - Un main CLI avec `argparse` qui accepte `--sample-size`, `--quick` (alias pour `--sample-size 50`)

2. Le main doit :
   - Appeler `fixer_seeds(42)`
   - Charger le sous-corpus via `src.data.prepare_subcorpus`
   - Lancer `run_baseline`
   - Logger le résultat dans le journal avec le timestamp, le commit git si dispo
   - Imprimer un résumé lisible

3. Ajoute `tests/test_baseline.py` avec :
   - Un test que `log_run_to_journal` produit du JSONL valide
   - Un test mock que `run_baseline` retourne bien les bonnes clés (pas besoin de charger vraiment TrOCR — utiliser un mock pour le modèle)

CONTRAINTES :
- L'inférence doit fonctionner sur CPU si pas de GPU (mode lent mais fonctionnel)
- Pas de hard-coding des chemins : tout via `pathlib` et un `--journal-path` optionnel
- Le script doit pouvoir tourner dans Colab ET en local sans modif

CRITÈRE DE SUCCÈS :
- `python -m src.htr.baseline --quick` tourne et écrit une ligne dans le journal
- Le CER retourné est cohérent avec celui du notebook (à 1-2 points près à cause du sample size différent)
- Tous les tests passent
```

---

## PROMPT 4 — Fine-tuning TrOCR par LoRA

**Branche** : `feature/htr-finetune-lora`

```
Lis `CLAUDE.md` et les modules `src/data/`, `src/evaluation/`, `src/htr/baseline.py` existants.

OBJECTIF : implémenter le fine-tuning de TrOCR par LoRA sur le sous-corpus CATMuS, avec early stopping sur le val CER.

LIVRABLES :

1. Crée `src/htr/finetune_trocr.py` avec :
   - Une dataclass `TrainingConfig` (lora_r: int, lora_alpha: int, learning_rate: float, batch_size: int, max_epochs: int, eval_every_n_steps: int, patience: int, output_dir: Path)
   - Une fonction `build_lora_model(base_model_name: str, lora_r: int, lora_alpha: int) -> PeftModel` qui wrappe TrOCR avec LoRA (target_modules à choisir judicieusement pour TrOCR — chercher dans la doc PEFT)
   - Une fonction `train(config, train_ds, val_ds) -> dict` qui :
     - Construit le modèle
     - Boucle d'entraînement avec accumulation de gradient si nécessaire
     - Évalue le CER val tous les `eval_every_n_steps`
     - Sauvegarde le meilleur checkpoint
     - Implémente early stopping (arrêt si val CER ne baisse pas pendant `patience` évaluations)
     - Retourne les métriques finales et le chemin du meilleur checkpoint
   - Une fonction `evaluate_checkpoint(checkpoint_path, val_ds) -> dict` réutilisable
   - Un main CLI avec argparse pour tous les hyperparamètres

2. Le main doit :
   - Logger chaque évaluation intermédiaire ET le résultat final dans `experiments/journal.jsonl`
   - Sauvegarder les courbes d'apprentissage en CSV dans `experiments/runs/<run_id>/learning_curve.csv`
   - Imprimer une commande prête à copier pour évaluer le checkpoint sauvegardé

3. Tests dans `tests/test_finetune.py` :
   - `TrainingConfig` valide les valeurs (lora_r > 0, learning_rate > 0)
   - `build_lora_model` retourne bien un `PeftModel` (peut être skip si pas de GPU avec `@pytest.mark.gpu`)

CONTRAINTES :
- Mémoire : doit tenir sur T4 16GB en fp16. Batch size par défaut à 4-8.
- Utiliser `accelerate` pour la gestion multi-device
- Le checkpoint final est sauvegardé en format PEFT (juste les poids LoRA, ~quelques MB)

CRITÈRE DE SUCCÈS :
- `python -m src.htr.finetune_trocr --lora-r 8 --max-epochs 3 --eval-every-n-steps 500` tourne sur Colab T4
- Le val CER baisse au fil des epochs (graphique à inspecter dans le CSV)
- Le journal contient une entrée par évaluation
- Tous les tests passent
```

---

## PROMPT 5 — Intervalles de confiance bootstrap

**Branche** : `feature/evaluation-bootstrap`

```
Lis `CLAUDE.md`.

OBJECTIF : calculer des intervalles de confiance bootstrap (N=1000) sur le CER.

LIVRABLES :

1. Crée `src/evaluation/bootstrap.py` avec :
   - `bootstrap_cer(predictions, references, n_iterations: int = 1000, confidence: float = 0.95, seed: int = 42) -> dict`
   - Retourne un dict avec `cer_mean`, `ci_lower`, `ci_upper`, `n_iterations`, `confidence_level`
   - Utilise le ré-échantillonnage avec remise au niveau des **paires (pred, ref)**, pas des caractères

2. Tests dans `tests/test_bootstrap.py` :
   - Sur un exemple synthétique, vérifier que l'IC contient bien la moyenne
   - Vérifier la reproductibilité avec seed fixé
   - Vérifier que `cer_mean` est proche du CER global (sans bootstrap)

CONTRAINTE :
- Performance : 1000 itérations sur 1000 lignes ne doit pas prendre plus de 10 secondes

CRITÈRE DE SUCCÈS :
- `pytest tests/test_bootstrap.py -v` passe
- L'IC sur exemple synthétique a la couverture nominale attendue
```

---

## PROMPT 6 — Data contract JSON

**Branche** : `feature/data-contract`

```
Lis `CLAUDE.md`. Le brief impose un jeu de données de sortie JSON validé par un schéma — c'est le livrable principal vers le Volet 2 NLP.

OBJECTIF : définir et valider le schéma du jeu de données de sortie.

LIVRABLES :

1. Crée `src/data/data_contract.py` avec :
   - Un schéma Pydantic `TranscriptionLine` avec champs :
     - `line_id: str` (identifiant unique)
     - `manuscript_id: str`
     - `folio: str | None`
     - `line_number: int | None`
     - `text: str` (la transcription)
     - `language: str` (ISO 639)
     - `century: int`
     - `polygon: list[tuple[int, int]] | None` (coordonnées en pixels)
     - `confidence: float` (entre 0 et 1)
     - `needs_review: bool`
     - `source_image_url: str | None`
   - Une fonction `export_dataset(lines: list[TranscriptionLine], output_path: Path) -> None` qui écrit en JSON pretty-printed
   - Une fonction `validate_dataset_file(path: Path) -> list[TranscriptionLine]` qui charge et valide
   - Un schéma JSON correspondant exporté dans `dataset_nlp/schema.json`

2. Crée `tests/test_data_contract.py` :
   - Un test que `TranscriptionLine` rejette les confidences hors [0, 1]
   - Un test que `validate_dataset_file` détecte un fichier mal formé
   - Un test que `export_dataset` produit un JSON parseable

CRITÈRE DE SUCCÈS :
- Tests passent
- `dataset_nlp/schema.json` est valide JSON Schema Draft-07
```

---

## PROMPT 7 — Évaluation finale sur le test scellé

**Branche** : `feature/evaluation-final`

```
Lis `CLAUDE.md`. ATTENTION : ce script évalue sur le test set SCELLÉ. Il ne doit être exécuté qu'UNE SEULE FOIS avant le rendu.

OBJECTIF : produire l'évaluation finale + le jeu de données de sortie pour le Volet 2.

LIVRABLES :

1. Crée `src/evaluation/run_on_test.py` avec :
   - Une fonction `run_final_evaluation(checkpoint_path: Path, test_ds: Dataset) -> dict` qui :
     - Charge le checkpoint LoRA
     - Lance l'inférence sur tout le test set
     - Calcule CER, WER, bootstrap CI
     - Marque les lignes `needs_review` (confidence < seuil, ou autre critère)
     - Exporte le jeu de données via `src.data.data_contract.export_dataset` dans `dataset_nlp/transcriptions.json`
     - Log dans le journal avec un tag spécial `"final": true`
   - Vérification du hash SHA-256 du test set : si différent de celui dans `DATA_SOURCES.md`, **lève une exception** (sécurité contre la contamination)
   - Un main CLI : `python -m src.evaluation.run_on_test --checkpoint <path>`

2. Tests :
   - Vérifier que la fonction de hash refuse un test set modifié

CONTRAINTE NON-NÉGOCIABLE :
- Ce script est exécuté UNE FOIS, à la fin. Documenter ça clairement en haut du fichier en commentaire.
- Imprimer un avertissement et demander confirmation avant exécution
```

---

## Tips généraux pour driver Claude Code

1. **Un prompt = une branche = un commit**. Ne mélange pas plusieurs features dans la même session.
2. **Toujours valider les tests après**. Si Claude Code dit que c'est fait, fais `pytest tests/ -v` toi-même.
3. **Lis le diff avant de commit**. `git diff` est ton ami.
4. **Si Claude Code propose un truc qui te surprend**, demande pourquoi avant d'accepter.
5. **N'hésite pas à dire « non, refais comme ça »** si l'implémentation s'écarte des conventions.
6. **Si bloqué**, le fallback : explique le contexte (le quoi et le pourquoi), pas juste le quoi.

## Calendrier suggéré

| Semaine | Prompts à exécuter | Livrable attendu |
|---|---|---|
| 1 | 1, 2, 3 | Pipeline baseline fonctionnel en CLI + CER zéro-shot loggé |
| 2 | 4, 5 | Premier fine-tuning LoRA r=8 + CI bootstrap calculé sur val |
| 3 | 4 (r=16), ablations | Modèle final sélectionné sur val |
| 4 | 6, 7 (préparation seulement) | Data contract figé + script d'évaluation finale prêt |
| 5 | 7 (exécution UNE FOIS) + rédaction article | Test set évalué + jeu de données livré |

Bonne route.
