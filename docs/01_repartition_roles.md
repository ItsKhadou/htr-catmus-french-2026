# Répartition des rôles — Équipe HTR CATMuS

Équipe de 4 personnes, 4 rôles principaux. Chaque membre porte un rôle principal et est en backup d'un autre.

## Les 4 rôles

### Rôle 1 — Responsable technique (Tech Lead)
**Mission** : garantir la qualité du code, l'architecture du pipeline et l'infrastructure.

**Responsabilités principales :**
- Mise en place du repo GitHub et de la CI (tests automatiques sur chaque PR)
- Revue des merge requests (toutes les PR doivent être relues par lui/elle ou le binôme)
- Architecture du pipeline (découpage en modules, interfaces entre composants)
- Gestion des dépendances (`pyproject.toml`, gel des versions)
- Setup de l'infrastructure d'entraînement (Colab, Kaggle, GCP)

**Livrables associés :**
- `src/` (qualité globale)
- `pyproject.toml`
- `tests/` (couverture minimale du pipeline)
- README technique

**Profil idéal** : la personne la plus à l'aise avec Python, git workflow et MLOps.

---

### Rôle 2 — Responsable documentation (Doc Lead)
**Mission** : produire l'article scientifique et toute la documentation utilisateur.

**Responsabilités principales :**
- Rédaction de l'article scientifique (commencer dès semaine 1)
- Rédaction et maintenance du README
- Rédaction de la `MODEL_CARD.md`
- Cohérence du style et de la terminologie
- Relecture finale avant rendu

**Livrables associés :**
- `article/` (LaTeX ou Markdown)
- `README.md`
- `MODEL_CARD.md`
- Slides de présentation

**Profil idéal** : la personne la plus à l'aise en rédaction scientifique en français, méthodique sur la structure.

---

### Rôle 3 — Responsable expérimentation (Experiment Lead)
**Mission** : faire tourner les expériences, suivre les métriques, sélectionner les meilleurs modèles.

**Responsabilités principales :**
- Conception des protocoles d'entraînement (LoRA r=8, r=16, ablations…)
- Maintien de `experiments/journal.jsonl` (chaque run enregistré : hyperparamètres, CER val, durée, checkpoint)
- Calcul des intervalles de confiance bootstrap et du test de McNemar
- Production des courbes d'apprentissage et figures de l'article
- Sélection finale du meilleur modèle pour le test scellé

**Livrables associés :**
- `experiments/journal.jsonl`
- Courbes d'apprentissage (figures de l'article)
- Métriques finales sur le test set

**Profil idéal** : la personne la plus rigoureuse sur la méthodologie expérimentale et les statistiques.

---

### Rôle 4 — Responsable données (Data Lead)
**Mission** : sélection, qualité, licences et structuration des données.

**Responsabilités principales :**
- Sélection finale du sous-corpus CATMuS (langues, siècles, manuscrits)
- Documentation du sous-corpus (`DATA_SOURCES.md`)
- Définition et maintenance du `CONVENTIONS_TRANSCRIPTION.md`
- Conception du data contract JSON (schéma de sortie pour le Volet 2 NLP)
- Calcul et journalisation des hash SHA-256 des splits
- Production du jeu de données final exporté

**Livrables associés :**
- `DATA_SOURCES.md`
- `CONVENTIONS_TRANSCRIPTION.md`
- `dataset_nlp/` (jeu de données JSON livrable)
- `segmentations/` (PAGE XML ou polygones JSON)

**Profil idéal** : la personne la plus à l'aise avec les structures de données, les schémas et la rigueur formelle. *Probablement Khadidja, vu ton background BI.*

---

## Matrice RACI simplifiée

Pour chaque livrable majeur, qui est responsable, qui contribue ?

| Livrable | Responsable | Contributeurs |
|---|---|---|
| Article scientifique | Doc | Tous |
| Code pipeline | Tech | Tous |
| Sélection corpus | Data | Tech |
| Conventions transcription | Data | Doc |
| Fine-tuning et runs | Expé | Tech |
| Journal d'expériences | Expé | — |
| Évaluation test scellé | Expé | Data |
| Data contract JSON | Data | Tech |
| PAGE XML segmentation | Data | Tech |
| Model card | Doc | Expé |
| Slides | Doc | Tous |
| Reproduction (README) | Tech | Doc |

## Règle de défense du projet

Le brief impose que **tout membre de l'équipe sache présenter et défendre n'importe quelle partie du projet**. Donc même si chacun a un rôle principal, tout le monde doit comprendre l'ensemble. Concrètement :

- À chaque rétrospective hebdo, chaque responsable explique en 5 min ce qu'il a fait
- Avant le rendu, organiser une session de simulation où chacun défend une partie qui n'est pas la sienne

## Cadence proposée

- **Stand-up quotidien** : 15 min, format Slack ou Discord — ce que j'ai fait, ce que je fais aujourd'hui, ce qui me bloque
- **Rétrospective hebdo** : 30 min, en visio — bilan métriques, blocages, ajustement de la suite
- **Revue de PR** : sous 24h, par la personne désignée comme binôme (voir tableau ci-dessous)

## Binômes de revue de PR

Pour que personne ne valide ses propres PR :

| Auteur | Reviewer principal | Backup |
|---|---|---|
| Tech | Expé | Data |
| Doc | Data | Tech |
| Expé | Tech | Doc |
| Data | Doc | Expé |

## Workflow Git

- `main` : protégée, jamais de push direct
- `dev` : branche d'intégration
- `feature/<nom>` : une branche par fonctionnalité
- Merge `feature/*` → `dev` via PR avec review obligatoire
- Merge `dev` → `main` à chaque jalon validé (fin de semaine)

---

*Ce document est une proposition. À adapter selon les forces et préférences de l'équipe en réunion 1.*
