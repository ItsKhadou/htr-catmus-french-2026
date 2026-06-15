# Conventions de transcription

Ce document fixe les choix éditoriaux retenus pour la transcription dans ce projet. Il s'inscrit dans la continuité des conventions du dataset source CATMuS Medieval.

## 1. Héritage CATMuS

Le projet CATMuS Medieval (Clérice et al., 2024) propose un cadre normalisé pour la transcription des manuscrits médiévaux en écriture latine. Notre approche consiste à **respecter les conventions CATMuS** plutôt qu'à en réinventer.

Les principes de transcription CATMuS sont décrits en détail dans :
- Clérice, T., Pinche, A., Vlachou-Efstathiou, M., et al. (2024). *CATMuS Medieval: A multilingual large-scale cross-century dataset in Latin script for handwritten text recognition and beyond*. HAL inria-04453952.
- Documentation officielle du dataset sur HuggingFace : <https://huggingface.co/datasets/CATMuS/medieval>

## 2. Niveau de transcription retenu

**Semi-diplomatique.**

Justification : ce niveau est celui retenu par CATMuS pour assurer la cohérence inter-manuscrits. Il préserve les graphies caractéristiques tout en permettant une normalisation minimale (résolution de certaines abréviations, restitution des lettres élidées entre crochets).

| Niveau | Description | Retenu ? |
|---|---|---|
| Diplomatique strict | Restitue exactement chaque signe, sans résolution | ✗ |
| **Semi-diplomatique** | **Résout certaines abréviations, conserve la casse et la ponctuation d'origine** | **✓** |
| Normalisé | Modernise l'orthographe et la ponctuation | ✗ |

## 3. Traitement des abréviations

Les manuscrits médiévaux sont massivement abrégés (suspensions, contractions, signes tironiens).

**Convention CATMuS appliquée** :
- Les abréviations sont **résolues** entre parenthèses : `dñs` → `d(omi)n(u)s`
- Le signe d'abréviation lui-même n'est pas conservé dans la transcription
- L'esperluette tironienne (⁊) est transcrite `&` ou résolue selon la langue (`et` en latin, `et` en ancien français)

## 4. Traitement des lacunes

- **Lacune dont le texte est restituable** par conjecture ou contexte : `[texte restitué]`
- **Lacune illisible ou détruite, longueur estimable** : `[...]` ou `[…]` selon la longueur
- **Caractère ambigu ou douteux** : `c(?)`

## 5. Ratures et corrections

Pour les manuscrits CATMuS, les corrections sont en général déjà acceptées (texte final retenu). Si une ligne contient une rature visible et significative :
- Le texte rayé n'est **pas** retranscrit
- Une note marginale dans le champ `notes` du JSON peut signaler la présence d'une correction

## 6. Casse et ponctuation

- **Casse** : conservée telle quelle (les majuscules médiévales sont souvent ornementales, ne pas les modifier)
- **Ponctuation** : conservée telle quelle (le point médian `·`, le `punctus` `.`, et les autres signes anciens sont transcrits comme ils apparaissent)
- **Espaces** : un espace standard entre mots ; les fines ou doubles espaces ne sont pas distingués

## 7. Caractères spéciaux

Le jeu de caractères de transcription comprend :
- Lettres latines de base (a-z, A-Z)
- Lettres accentuées (à, é, è, ê, î, ô, û, ç…)
- Lettres anciennes : `þ` (thorn), `ð` (eth), `æ`, `œ`, `ſ` (s long)
- Signes diacritiques : tilde nasal `ã`, `õ`, `ñ`
- Ponctuation : `· . , ; : ! ?`
- Crochets éditoriaux : `[ ] ( )`

L'encodage de référence est **UTF-8 NFC** (forme normalisée composée).

## 8. Numéros de folio et structure

Chaque ligne transcrite est associée à :
- `manuscript_id` : identifiant CATMuS du manuscrit
- `folio` : recto/verso et numéro de feuillet (ex. `12r`, `45v`)
- `line_number` : numéro de ligne dans la page (ex. `7`)
- `polygon` : coordonnées du polygone englobant la ligne

## 9. Mélanges linguistiques (code-switching)

Les manuscrits médiévaux français contiennent fréquemment des passages en latin (citations, rubriques, formules liturgiques). Dans ce projet :
- La **langue principale** de chaque ligne est documentée dans le champ `language`
- Les passages très courts (un mot, un syntagme) en autre langue ne déclenchent pas de changement de langue
- Les rubriques latines complètes sont marquées `lang: "lat"`

## 10. Évolution du document

Ce fichier doit être mis à jour à chaque décision éditoriale prise en cours de projet. **Toute décision non documentée ici n'existe pas du point de vue de l'évaluation.**

| Date | Auteur | Modification |
|---|---|---|
| YYYY-MM-DD | [Data Lead] | Création initiale du document |
