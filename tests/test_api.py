from fastapi.testclient import TestClient
from app.main import app

# test corretta operatività dell'API
client = TestClient(app)


def test_predict_risponde_correttamente():
    response = client.post("/predict", json={"review": "This product is amazing! I love it."})
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"


def test_predict_formato_risposta():
    response = client.post("/predict", json={"review": "Terrible quality, it broke after one day."})
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1


def test_predict_senza_review_da_errore():
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_metrics_disponibile():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predict_request_seconds" in response.text
    assert "predict_errors_total" in response.text