from fastapi import FastAPI
from api.schemas import PredictionRequest, PredictionResponse
from api.model import model, predict

app = FastAPI(title="Sentiment API")

@app.get("/health")
def health():
    return {
        "status": "OK",
        "model": f"tfidf-logreg (TP2, models/sentiment.joblib)"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest):
    result = predict(request.text)
    return {
        "text": request.text,
        "label": result["label"],
        "score": result["score"]
    }