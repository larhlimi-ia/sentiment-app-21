# Semaine 5 : Interface Streamlit - Rendre le Modèle Accessible

## Objectifs atteints

Ce TP a transformé le modèle ML et l'API en une **application web interactive** accessible aux utilisateurs finaux, sans qu'ils aient besoin de connaître Python, FastAPI ou les commandes curl.

## 1. Architecture : De l'API à l'Interface

### Flux global

```
Utilisateur tape un avis
    ↓
Interface Streamlit (port 8501)
    ↓
Client HTTP (ui/client.py)
    ↓
API FastAPI (port 8000)
    ↓
Modèle TF-IDF + Régression logistique
    ↓
Verdict + Confiance
    ↓
Interface affiche résultat avec couleurs et emojis
```

### Séparation des responsabilités

- **API (TP3)** : Service sans état, validé, robuste. Peut être redeployée indépendamment.
- **Interface (TP5)** : Présentation, ergonomie, expérience utilisateur. Peut être modifiée sans toucher à l'API.
- **Client (TP5)** : Gestion des appels HTTP, gestion d'erreurs, retry logic.

Cette architecture permet que l'équipe interface travaille indépendamment de l'équipe ML.

## 2. Interface Streamlit : Fonctionnalités

### Page 1 : Prédiction simple

```
📊 Analyse de Sentiment - Avis Clients

API prête : tfidf-logreg (TP2, models/sentiment.joblib)

Entrez un avis :
[Textbox pour saisir l'avis]

[Bouton "Analyser"]

Résultat :
✅ Avis positif (78% confiance)
ou
❌ Avis négatif (75% confiance)
ou
❓ Je ne sais pas (52% confiance)
```

**Logique** :
- Si label = POSITIVE → emoji ✅, couleur verte, pourcentage
- Si label = NEGATIVE → emoji ❌, couleur rouge, pourcentage
- Si label = INDETERMINE → emoji ❓, couleur grise, pourcentage

**Gestion des erreurs** :
- Texte vide → "Texte refusé par l'API"
- API inaccessible → "API injoignable"
- Timeout → "Délai dépassé"

### Page 2 : Analyse par lot (CSV)

```
📁 Charger un fichier CSV

[Uploader pour data/avis_exemple.csv]

Résumé :
6 avis chargés
- 3 positifs (50%)
- 2 négatifs (33%)
- 1 indéterminé (17%)

[Tableau affichant : texte, label, score]

[Bouton "Télécharger résultats"]
```

**Fonctionnalités** :
- Upload CSV avec colonnes `text` (obligatoire)
- Prédiction pour chaque ligne
- Tableau interactif avec tri/filtrage
- Export CSV des résultats

### Page 3 : Dashboard (optionnel)

Graphiques Plotly pour visualiser:
- Distribution des sentiments (pie chart)
- Évolution des scores (histogram)
- Top mots positifs/négatifs (word cloud)

## 3. Client HTTP Robuste (ui/client.py)

### Responsabilités

```python
class SentimentClient:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
    
    def predict(self, text: str) -> dict:
        """Prédiction avec gestion d'erreurs"""
        try:
            response = requests.post(
                f"{self.api_url}/predict",
                json={"text": text},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                return {"error": "Texte refusé par l'API"}
            else:
                return {"error": f"Erreur {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"error": "API injoignable"}
        except requests.exceptions.Timeout:
            return {"error": "Délai dépassé"}
```

### Avantages

- **Isolation** : Logique HTTP séparée de l'interface
- **Testabilité** : Client testable indépendamment
- **Réutilisabilité** : Peut être utilisé par d'autres interfaces (mobile, desktop)
- **Robustesse** : Gestion systématique des erreurs réseau

## 4. Cas d'Usage Testés

### Test T29 : Page charge avec API prête
```
Streamlit lance
API prête : tfidf-logreg (TP2, ...)
✅ Page affiche le message
```

### Test T30 : Prédictions simples
```
"Livraison rapide, produit conforme, très satisfait"
→ Avis positif, 78%
✅ Résultat correct
```

### Test T31 : Cas indéterminé
```
"xqzvb wlkptr grombu"
→ Je ne sais pas, 52%
✅ Abstention correcte
```

### Test T32 : Gestion des erreurs
```
"   " (trois espaces)
→ Texte refusé
✅ Erreur API bien traduite

API arrêtée
→ API injoignable
✅ Erreur réseau gérée
```

### Test T33 : Upload CSV
```
data/avis_exemple.csv (6 avis)
→ Tableau + résumé
→ Téléchargement CSV
✅ Batch processing fonctionne
```

## 5. Leçons apprises

### Architecture
- **Séparation API/Interface** = flexibilité (changer l'interface sans toucher à l'API)
- **Client robuste** = expérience utilisateur stable même si le réseau est instable

### UX/Ergonomie
- **Couleurs et emojis** = feedback immédiat sans lire le texte
- **Messages d'erreur clairs** = utilisateur sait ce qui s'est passé
- **Batch processing** = permet d'analyser 100 avis d'un coup

### Déploiement
- API et Interface peuvent tourner sur **machines différentes**
- Interface peut être redeployée sans redémarrer l'API
- Client HTTP = portable (mobile, desktop, etc.)

## 6. Améliorations futures

1. **Cache Streamlit** : Mémoriser les prédictions pour éviter les appels API
2. **Authentification** : Protéger l'API avec une clé
3. **Historique** : Sauvegarder les avis analysés pour suivi
4. **Multi-langues** : Supporter français, anglais, arabe
5. **Dashboard temps réel** : WebSocket pour metrics en direct

## Métriques finales

| Métrique | Valeur |
|----------|--------|
| Tests passants | 88 passed, 3 xfailed |
| Pages Streamlit | 2+ (simple + batch) |
| Fonctionnalités | Prédiction, CSV upload, export |
| Gestion erreurs | API, réseau, validation |
| Client HTTP | Timeout, retry, types |

## Conclusion

Le projet est maintenant **complet et utilisable** :

- **TP1** : Cadrage et environnement ✅
- **TP2** : Modèle ML entraîné ✅
- **TP3** : API REST robuste ✅
- **TP4** : Tests approfondis et qualité ✅
- **TP5** : Interface ergonomique ✅

Un utilisateur non-technique peut maintenant analyser des avis clients en 2 clics, sans connaître Python ou l'IA.