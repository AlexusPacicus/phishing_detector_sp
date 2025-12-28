# 📑 Contrato de salida – Endpoint `/predict_explain`

Este documento define el **contrato JSON de salida** del nuevo endpoint `/predict_explain`, que integra el modelo de detección de phishing con explicabilidad generada vía Azure OpenAI.

---

## 🔹 Ejemplo de salida

```json
{
  "request_id": "b3e29c92-76f7-44b5-9c78-fbcd2f25b123",
  "timestamp": "2025-09-25T14:00:00Z",
  "url": "https://soporte-netflx.com/",
  "label": 1,
  "probability": 0.7517,
  "threshold": 0.425,
  "features": {
    "domain_length": 14,
    "domain_entropy": 3.37,
    "num_params": 0,
    "trusted_path_token": 0,
    "contains_percent": 0,
    "contains_equal": 0,
    "suspicious_path_token": 0,
    "free_hosting": 0,
    "protocol": 1,
    "tld_group": "com"
  },
  "explanation": "Clasificada como phishing porque usa hosting gratuito, un TLD sospechoso y muestra entropía de dominio elevada.",
  "reasons": [
    {"feature": "free_hosting", "evidence": "dominio en hosting gratuito", "weight": "alta"},
    {"feature": "tld_group", "evidence": "TLD fuera del grupo seguro", "weight": "media"},
    {"feature": "domain_entropy", "evidence": "entropía de dominio elevada", "weight": "baja"}
  ],
  "model_version": "logreg_v1.0",
  "prompt_version": "azure_v1"
}
 
 
 🔹 Campos obligatorios

request_id → UUID único para trazabilidad.
timestamp → Fecha/hora en formato ISO 8601 (UTC).
url → La URL analizada.
label → 0 = legítima, 1 = phishing.
probability → Score de probabilidad del modelo (float).
threshold → Umbral de decisión, fijado en 0.425.
features → Diccionario con las 10 features seleccionadas:
domain_length
domain_entropy
num_params
trusted_path_token
contains_percent
contains_equal
suspicious_path_token
free_hosting
protocol
tld_group
explanation → Explicación generada por Azure OpenAI en castellano (2–4 frases).
reasons → Lista de máx. 3 razones en formato {feature, evidence, weight}.
model_version → "logreg_v1.0".
prompt_version → Versión del prompt usado, ej. "azure_v1".


🔹 Casos especiales

Si la llamada a Azure OpenAI falla (timeout, error de cuota, etc.), la respuesta incluirá:
{
  "explanation": null,
  "reasons": [],
  "explanation_note": "LLM_unavailable"
}


🔹 Notas

El contrato asegura consistencia para testing automático y trazabilidad en auditorías.
Los campos model_version y prompt_version permiten versionar tanto el modelo como el prompt.
Se recomienda almacenar cada respuesta en Azure Blob Storage para auditoría (logs/prediction_{fecha}/{request_id}.json).
