"""Smoke tests — vérifient que le squelette du projet est sain.

Ces tests doivent passer dès le commit initial. Ils ne valident pas la qualité
du modèle, seulement la cohérence structurelle du dépôt.
"""

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


class TestRepoStructure:
    """Vérifie que les fichiers et dossiers obligatoires existent."""

    def test_readme_exists(self):
        assert (REPO_ROOT / "README.md").is_file()

    def test_pyproject_exists(self):
        assert (REPO_ROOT / "pyproject.toml").is_file()

    def test_conventions_exists(self):
        assert (REPO_ROOT / "CONVENTIONS_TRANSCRIPTION.md").is_file()

    def test_data_sources_exists(self):
        assert (REPO_ROOT / "DATA_SOURCES.md").is_file()

    def test_model_card_exists(self):
        assert (REPO_ROOT / "MODEL_CARD.md").is_file()

    def test_src_modules_present(self):
        modules = ["data", "preprocessing", "segmentation", "htr", "evaluation"]
        for m in modules:
            assert (REPO_ROOT / "src" / m / "__init__.py").is_file(), (
                f"Module manquant : src/{m}/__init__.py"
            )

    def test_experiments_journal_exists(self):
        assert (REPO_ROOT / "experiments" / "journal.jsonl").is_file()


class TestPythonImports:
    """Vérifie que les modules du package sont importables."""

    def test_import_src(self):
        import src  # noqa: F401

    def test_import_data(self):
        from src import data  # noqa: F401

    def test_import_preprocessing(self):
        from src import preprocessing  # noqa: F401

    def test_import_segmentation(self):
        from src import segmentation  # noqa: F401

    def test_import_htr(self):
        from src import htr  # noqa: F401

    def test_import_evaluation(self):
        from src import evaluation  # noqa: F401


class TestExperimentJournalFormat:
    """Le journal d'expériences doit être un JSONL valide."""

    def test_journal_is_valid_jsonl(self):
        journal_path = REPO_ROOT / "experiments" / "journal.jsonl"
        with open(journal_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Ligne {line_num} du journal invalide : {e}")


# Test de non-régression CER : à activer une fois la baseline en place
@pytest.mark.skip(reason="À activer une fois la baseline TrOCR évaluée")
class TestCERNonRegression:
    """Empêche le CER de remonter au-dessus du seuil de validation (15 %)."""

    SEUIL_VALIDATION_CER = 0.15

    def test_baseline_cer_under_threshold(self):
        # À implémenter : charger le dernier run du journal, vérifier CER val < seuil
        pass
