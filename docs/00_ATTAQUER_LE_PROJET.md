# Kit de démarrage — Projet HTR CATMuS Medieval (Volet 1)

Ce kit te donne tout ce qu'il faut pour démarrer en semaine 1.

## Ce qu'il y a dans ce dossier

| Fichier | À quoi ça sert | Quand le sortir |
|---|---|---|
| `00_ATTAQUER_LE_PROJET.md` | Ce fichier — guide d'ensemble | Maintenant |
| `01_repartition_roles.md` | Grille de répartition des 4 rôles à proposer à l'équipe | Réunion 1 |
| `02_plan_article.md` | Plan détaillé section par section de l'article scientifique | Réunion 1, puis tout le projet |
| `notebook_baseline_catmus.ipynb` | Notebook Colab qui charge CATMuS, filtre le sous-corpus, et calcule un premier CER baseline TrOCR | Jour 3-4 |
| `repo_skeleton/` | Squelette du dépôt GitHub, prêt à initialiser et pousser | Jour 1-2 |

## Ordre d'opérations recommandé pour la semaine 1

### Réunion de cadrage (jour 1, ~1h30)
1. Présenter le projet à l'équipe (le brief PDF)
2. Discuter la grille de rôles (`01_repartition_roles.md`) et attribuer
3. Discuter le plan d'article (`02_plan_article.md`) — qui écrit quoi quand
4. Décider du compute principal (Colab gratuit + Kaggle ? GCP gratuit ?)
5. Créer le repo GitHub (nom recommandé : `htr-catmus-french-2026`)

### Jours 2-3 — Setup technique
1. Cloner le repo, copier le contenu de `repo_skeleton/` dedans, premier commit
2. Mettre en place l'environnement Python via `pyproject.toml`
3. Faire tourner `pytest` pour vérifier que le squelette est sain
4. Brancher le repo sur HuggingFace Hub (token) pour les checkpoints futurs

### Jours 3-4 — Premier contact avec CATMuS
1. Ouvrir le notebook dans Colab
2. Le faire tourner intégralement
3. Récupérer : stats du sous-corpus, SHA-256 du test set, premier CER baseline
4. Coller ces résultats dans `experiments/journal.jsonl`

### Jour 5 — Premier squelette d'article
1. Ouvrir `02_plan_article.md`
2. Le responsable documentation rédige : introduction, début de l'état de l'art, description des données
3. Le reste viendra au fil des semaines

## Règles d'or à ne jamais oublier

- **Test set scellé dès jour 3** — calculer le SHA-256 et ne plus jamais y toucher
- **Seeds fixés partout** — `fixer_seeds(42)` en début de chaque script
- **Pipeline end-to-end avant perfection** — viser un CER de 25-30 % en fin de semaine 2 plutôt qu'un fine-tuning splendide en semaine 5
- **Rédaction en parallèle du code** — pas en fin de projet
- **Documenter chaque expérience** dans `experiments/journal.jsonl`

Bonne chance.
