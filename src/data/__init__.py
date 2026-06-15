"""Module de gestion des données.

Responsabilité : chargement, filtrage et préparation du sous-corpus CATMuS Medieval.

Sous-modules à implémenter :
    - prepare_subcorpus.py : filtrage CATMuS → sous-corpus Old/Middle French XIIIᵉ-XVᵉ
    - splits.py            : extraction des splits train/val/test via gen_split natif
    - hashing.py           : calcul du SHA-256 du test set scellé
    - data_contract.py     : schéma JSON du livrable pour le Volet 2 NLP
"""

import random

SEED_DEFAULT = 42


def fixer_seeds(seed: int = SEED_DEFAULT) -> None:
    """Fixe les seeds de toutes les sources d'aléatoire utilisées dans le projet.

    À appeler en début de chaque script ou notebook pour garantir
    la reproductibilité des résultats.

    Args:
        seed: Valeur de seed (défaut 42).

    Example:
        >>> from src.data import fixer_seeds
        >>> fixer_seeds(42)
    """
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


__all__ = ["fixer_seeds", "SEED_DEFAULT"]
