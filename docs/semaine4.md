@'
# Semaine 4 : Tests Approfondis et Qualité du Code

## Objectifs atteints

Ce TP a consolidé la robustesse et la maintenabilité du projet en trois volets: tests de cas limites, gestion des cas ambigus, et qualité du code.

## 1. Tests des Cas Limites

### Problème identifié
L'API acceptait n'importe quelle entrée sans valider les frontières. Par exemple, un texte vide ou de 2001 caractères passait sans erreur.

### Solution implémentée
Ajout de validateurs Pydantic stricts dans `api/schemas.py`:
- Texte vide ou blancs seulement: rejet avec code 422
- Texte > 2000 caractères: rejet avec code 422
- Champ `text` manquant ou mauvais type: rejet avec code 422

### Résultats
8 tests de frontières ajoutés, tous passants. L'API respecte maintenant un contrat clairement défini: texte entre 1 et 2000 caractères, sinon erreur 422.

## 2. Abstention et Confiance (INDETERMINE)

### Problème identifié
Le modèle prédisait toujours POSITIVE ou NEGATIVE, même quand sa confiance était faible (ex: 0.52). Sur un avis incompréhensible comme "xqzvb wlkptr grombu", forcer une prédiction était irresponsable.

### Solution implémentée
Introduction d'un **seuil d'abstention**: si `score < 0.60`, retourner `INDETERMINE` (je ne sais pas) au lieu de forcer POSITIVE/NEGATIVE.

Cela reflète une réalité métier: mieux dire "je ne sais pas" que de se tromper avec certitude.

### Résultats
Le modèle retourne maintenant:
- POSITIVE si confiance ≥ 60%
- NEGATIVE si confiance ≥ 60%
- INDETERMINE sinon

Exemple: "xqzvb wlkptr grombu" → INDETERMINE, 0.52 (correct).

## 3. Jeu d'Or: Validation et Erreurs Franches

### Approche
Création d'un **jeu d'or** (22 avis d'évaluation) couvrant:
- 6 cas difficiles: négation, ironie, aspects mitigés, sémantique étrangère
- **Erreurs franches annotées**: avis où le modèle se trompe systématiquement

### Erreurs franches observées
- "Décevant..." → attendu NEGATIVE, modèle dit POSITIVE (faux_positif)
- "Service client réactif..." → attendu POSITIVE, modèle dit NEGATIVE (faux_negatif)
- "Je ne recommande pas..." → attendu NEGATIVE, modèle dit POSITIVE (negation_mal_detectee)

### Insight pédagogique
TF-IDF compte les mots indépendamment: il voit "recommande" (positif) avant la négation. Amélioration future: modèle qui capture la négation (ex: BERT, transformers).

### Résultats
19 tests passent (avis correctement classés), 3 xfailed (erreurs attendues, annotées).

## 4. Qualité du Code

### Avant TP4
- Couverture de code: 91%
- ruff: 11 remarques
- mypy: Success

### Après corrections
- Couverture de code: **97%** (dépassé le seuil ≥95%)
- ruff: **0 remarques** (code propre)
- mypy: **Success** (tous les types vérifiés)
- Tests: **83 passed, 2 xfailed** ✅

### Bénéfices
- Code cohérent et maintenable
- Erreurs potentielles détectées avant le déploiement
- Nouvelle personne peut reprendre le code sans surprise

## 5. Leçons apprises

1. **Valider à la frontière**: Pydantic force la validation au point d'entrée (API)
2. **Documenter les limitations**: Le jeu d'or expose clairement où le modèle échoue
3. **Automatiser la qualité**: pre-commit, ruff, mypy évitent les débats sur le style
4. **Confiance ≠ Précision**: Une prédiction confiante peut être fausse.