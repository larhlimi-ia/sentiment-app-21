import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "models" / "sentiment.joblib"
SEUIL_ABSTENTION = 0.60

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"{MODEL_PATH} non trouvé")
    return joblib.load(MODEL_PATH)

model = load_model()

def predict(text: str) -> dict:
    """Prédiction avec abstention si confiance < seuil"""
    proba = model.predict_proba([text])[0]
    score = max(proba)
    
    if score < SEUIL_ABSTENTION:
        return {"label": "INDETERMINE", "score": float(score)}
    
    label = model.classes_[proba.argmax()].upper()  # ← Ajoute .upper()
    return {"label": label, "score": float(score)}