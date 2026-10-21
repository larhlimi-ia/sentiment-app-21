import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestHealth:
    """Tests du endpoint /health"""
    
    def test_health_status_code(self):
        """GET /health retourne 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_response_structure(self):
        """GET /health retourne status et model"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "model" in data
        assert data["status"] == "OK"


class TestPredictValidInput:
    """Tests du endpoint /predict avec entrées valides"""
    
    def test_predict_positive(self):
        """POST /predict avec avis positif"""
        response = client.post("/predict", json={"text": "Livraison rapide, produit conforme, très satisfait"})
        assert response.status_code == 200
        data = response.json()
        assert "label" in data
        assert "score" in data
        assert "text" in data
        assert data["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]
        assert 0 <= data["score"] <= 1
    
    def test_predict_negative(self):
        """POST /predict avec avis négatif"""
        response = client.post("/predict", json={"text": "Produit cassé et service injoignable, à fuir"})
        assert response.status_code == 200
        data = response.json()
        assert data["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]
    
    def test_predict_indeterminate(self):
        """POST /predict avec avis incompréhensible"""
        response = client.post("/predict", json={"text": "xqzvb wlkptr grombu"})
        assert response.status_code == 200
        data = response.json()
        assert data["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]


class TestPredictInvalidInput:
    """Tests du endpoint /predict avec entrées invalides"""
    
    def test_predict_empty_string(self):
        """POST /predict avec texte vide"""
        response = client.post("/predict", json={"text": ""})
        assert response.status_code == 422
    
    def test_predict_whitespace_only(self):
        """POST /predict avec espaces seulement"""
        response = client.post("/predict", json={"text": "   "})
        assert response.status_code == 422
    
    def test_predict_missing_field(self):
        """POST /predict sans champ text"""
        response = client.post("/predict", json={})
        assert response.status_code == 422
    
    def test_predict_wrong_type(self):
        """POST /predict avec type incorrect"""
        response = client.post("/predict", json={"text": 42})
        assert response.status_code == 422


class TestPredictResponseSchema:
    """Tests de la structure de réponse"""
    
    def test_response_includes_text(self):
        """Réponse inclut le texte d'entrée"""
        text = "Très bon produit"
        response = client.post("/predict", json={"text": text})
        data = response.json()
        assert data["text"] == text
    
    def test_response_label_valid(self):
        """Label est POSITIVE, NEGATIVE ou INDETERMINE"""
        response = client.post("/predict", json={"text": "Bon produit"})
        data = response.json()
        assert data["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]
    
    def test_response_score_range(self):
        """Score est entre 0 et 1"""
        response = client.post("/predict", json={"text": "Test"})
        data = response.json()
        assert isinstance(data["score"], float)
        assert 0 <= data["score"] <= 1