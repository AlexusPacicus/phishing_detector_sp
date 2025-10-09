# app_fastapi_azure.py
import os
import uuid
import time
import json
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from joblib import load
from azure.storage.blob import BlobServiceClient, ContentSettings

# =========================
# Configuración de entorno
# =========================
AZ_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZ_KEY = os.getenv("AZURE_OPENAI_KEY")
AZ_DEPLOY = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
API_VERSION = "2024-12-01-preview"
MODEL_VERSION = "logreg_v1.0"
PROMPT_VERSION = "azure_v1"
BLOB_CONNSTR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")  # opcional
BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER", "logs")

if not AZ_ENDPOINT or not AZ_KEY:
    raise SystemExit("ERROR: exporta AZURE_OPENAI_ENDPOINT y AZURE_OPENAI_KEY antes de ejecutar.")

llm = AzureOpenAI(api_version=API_VERSION, azure_endpoint=AZ_ENDPOINT, api_key=AZ_KEY)

blob_client = None
if BLOB_CONNSTR:
    blob_client = BlobServiceClient.from_connection_string(BLOB_CONNSTR)
    try:
        blob_client.create_container(BLOB_CONTAINER)
    except Exception:
        pass

MODEL_PATH = os.getenv("MODEL_PATH", "models/logreg_phishing_final.joblib")
try:
    model = load(MODEL_PATH)
except Exception as e:
    model = None
    print("⚠️ WARNING: no se pudo cargar el modelo en", MODEL_PATH, "-", e)

# =========================
# FastAPI
# =========================
app = FastAPI(title="Phishing Detector + Azure Explainability")

class PredictRequest(BaseModel):
    url: str

# =========================
# Features (stub: adáptalo a tu extractor real)
# =========================
def extract_features(url: str) -> Dict[str, Any]:
    return {
        "domain_length": len(url.split("/")[2]) if "://" in url else len(url),
        "domain_entropy": 3.0,  # placeholder
        "num_params": 0,
        "trusted_path_token": 0,
        "contains_percent": 0,
        "contains_equal": 0,
        "suspicious_path_token": 0,
        "free_hosting": 1 if "webcindario" in url or "web.app" in url else 0,
        "protocol": 1 if url.startswith("https://") else 0,
        "tld_group": url.split(".")[-1] if "." in url else "com"
    }

# =========================
# Llamada a Azure LLM
# =========================
def call_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    system = (
        "Eres un analista SOC. Explica la decisión de un modelo de detección de phishing "
        "SOLO usando las features provistas. No inventes pruebas ni nombres de empresa. "
        "Escribe en español, 2–4 frases. Devuelve SIEMPRE un JSON con los campos "
        "`explanation` y `reasons`."
    )
    user_msg = json.dumps(payload, ensure_ascii=False)

    resp = llm.chat.completions.create(
        model=AZ_DEPLOY,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg}
        ],
        max_tokens=300,
        temperature=0.0,
        top_p=1.0,
    )

    text = resp.choices[0].message.content.strip()
    try:
        parsed = json.loads(text)
        explanation = parsed.get("explanation")
        reasons = parsed.get("reasons", [])
    except Exception:
        explanation = text
        reasons = []
    return {"explanation": explanation, "reasons": reasons}

# =========================
# Guardar log en Blob
# =========================
def save_log_to_blob(key: str, data: Dict[str, Any]):
    if not blob_client:
        return
    container = blob_client.get_container_client(BLOB_CONTAINER)
    blob_name = f"prediction_{time.strftime('%Y%m%d')}/{key}.json"
    container.upload_blob(
        name=blob_name,
        data=json.dumps(data, ensure_ascii=False),
        overwrite=True,
        content_settings=ContentSettings(content_type="application/json")
    )

# =========================
# Endpoint principal
# =========================
@app.post("/predict_explain")
def predict_explain(req: PredictRequest):
    request_id = str(uuid.uuid4())
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    url = req.url

    # 1) Features
    features = extract_features(url)

    # 2) Predicción local
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")
    X = [list(features.values())]
    prob = float(model.predict_proba(X)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(X)[0])
    threshold = float(os.getenv("MODEL_THRESHOLD", 0.425))
    label = 1 if prob >= threshold else 0

    payload = {
        "request_id": request_id,
        "timestamp": timestamp,
        "url": url,
        "label": label,
        "probability": prob,
        "threshold": threshold,
        "features": features,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION
    }

    # 3) Llamada a Azure OpenAI (con fallback)
    try:
        llm_result = call_llm(payload)
        payload["explanation"] = llm_result.get("explanation")
        payload["reasons"] = llm_result.get("reasons", [])
    except Exception:
        payload["explanation"] = None
        payload["reasons"] = []
        payload["explanation_note"] = "LLM_unavailable"

    # 4) Guardar log en Blob (si está activado)
    try:
        save_log_to_blob(request_id, payload)
    except Exception as e:
        print("⚠️ Warning: no se pudo guardar en blob:", e)

    return payload
