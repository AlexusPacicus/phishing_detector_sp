# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "threshold" in data

def test_predict_endpoint():
    res = client.post("/predict", json={"url": "https://soporte-netflx.com/"})
    assert res.status_code == 200
    data = res.json()

    # ✅ Claves esperadas en la respuesta
    assert "label" in data
    assert "probability" in data
    assert "threshold" in data
    assert "features" in data

    # ✅ Features contiene las 10 columnas
    assert len(data["features"]) == 10
