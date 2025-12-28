import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from features.features_base import extract_features


# === CONFIGURACIÓN ===
ROOT = Path(".")
MODEL_PATH = ROOT / "models" / "logreg_phishing_final.joblib"
DATA_PATH = ROOT / "dataset" / "eval_set_inclusion_v2.csv"
OUT_DIR = ROOT / "outputs" / "inclusion_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)
THRESHOLD = 0.425
# =====================

print(f"📥 Cargando dataset: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"✅ {len(df)} filas cargadas.")

# ===== Función auxiliar para dominio base =====
def base_domain(url):
    try:
        netloc = urlparse(str(url)).netloc.lower()
        parts = netloc.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return netloc
    except Exception:
        return ""

df["base_domain"] = df["url"].apply(base_domain)

# ===== Check de solapamiento (legit vs phish) =====
common_domains = df.groupby("base_domain")["label"].nunique()
overlap = common_domains[common_domains > 1]
if not overlap.empty:
    print("⚠️  Dominios en común detectados (posible leakage):")
    print(overlap)
    overlap.to_csv(OUT_DIR / "overlap_domains.csv")
else:
    print("✅ No se detectan dominios solapados entre clases.")

# ===== Extracción de features =====
print("🔍 Extrayendo features con extract_features() ...")
X = df["url"].apply(lambda u: pd.Series(extract_features(u)))

# 💡 Añadir las features al dataframe principal
df = pd.concat([df, X], axis=1)

# ===== Cargar modelo =====
print(f"📦 Cargando modelo desde: {MODEL_PATH}")
bundle = joblib.load(MODEL_PATH)

# Si el modelo está guardado como diccionario (modelo + scaler + encoder)
if isinstance(bundle, dict) and "model" in bundle:
    model = bundle["model"]
else:
    model = bundle

# ===== Predicciones =====
probs = model.predict_proba(X.fillna(0))[:, 1]
df["prob_phish"] = probs
df["pred_label"] = (probs >= THRESHOLD).astype(int)

# ===== Métricas =====
y_true = df["label"].values
y_pred = df["pred_label"].values

metrics = {
    "accuracy": accuracy_score(y_true, y_pred),
    "precision": precision_score(y_true, y_pred),
    "recall": recall_score(y_true, y_pred),
    "f1": f1_score(y_true, y_pred),
    "roc_auc": roc_auc_score(y_true, probs)
}

print("\n📊 Métricas globales:")
for k, v in metrics.items():
    print(f"  {k}: {v:.4f}")

print("\n📋 Informe detallado:")
print(classification_report(y_true, y_pred))

# ===== Guardar predicciones =====
pred_file = OUT_DIR / "predicciones_inclusion_v2.csv"
df.to_csv(pred_file, index=False)
print(f"💾 Predicciones guardadas en: {pred_file}")

# ===== Falsos negativos =====
fns = df[(df["label"] == 1) & (df["pred_label"] == 0)].copy()
fns = fns.sort_values(by="prob_phish", ascending=False)
fns_file = OUT_DIR / "falsos_negativos_priorizados.csv"
fns.to_csv(fns_file, index=False)
print(f"💾 Falsos negativos guardados en: {fns_file}")

# ===== Guardar informe markdown =====
report_md = OUT_DIR / "evaluacion_inclusion_v2.md"
with open(report_md, "w", encoding="utf-8") as fh:
    fh.write("# 🧠 Evaluación inclusión v2\n\n")
    fh.write(f"Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}\n\n")
    fh.write("## 📊 Métricas globales\n")
    for k, v in metrics.items():
        fh.write(f"- **{k}**: {v:.4f}\n")
    fh.write("\n## 🧩 Observaciones\n")
    fh.write(f"- Umbral usado: {THRESHOLD}\n")
    fh.write(f"- Falsos negativos detectados: {len(fns)}\n")
    fh.write(f"- Dataset evaluado: {DATA_PATH.name}\n")
    fh.write(f"- Modelo: {MODEL_PATH.name}\n")
print(f"🧾 Informe guardado en: {report_md}")

print("\n✅ Evaluación completada correctamente.")
