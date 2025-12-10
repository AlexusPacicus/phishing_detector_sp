# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import PredictRequest, PredictResponse
from app.features import extract_features
from app.model import wrapper
import pandas as pd

app = FastAPI(
    title="Detector de Phishing (España)",
    version="0.1",
    description="API para detectar URLs de phishing en el contexto español"
)

@app.get("/health", description="Comprueba si la API y el modelo están listos")
def health():
    return {
        "status": "ok",
        "model_loaded": wrapper.model is not None,
        "threshold": wrapper.threshold
    }

@app.post(
    "/predict",
    response_model=PredictResponse,
    description="Predice si una URL es phishing o legítima"
)
def predict(req: PredictRequest):
    url = req.url.strip()
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url  # normalizamos

    try:
        feats = extract_features(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extrayendo features: {e}")

    # Construir DataFrame con nombres de columnas correctos
    X = pd.DataFrame([feats])

    try:
        proba = wrapper.predict_proba(X)
        label = wrapper.predict_label(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en inferencia: {e}")

    return PredictResponse(
        label=label,
        probability=round(proba, 4),
        threshold=wrapper.threshold,
        features=feats
    )
