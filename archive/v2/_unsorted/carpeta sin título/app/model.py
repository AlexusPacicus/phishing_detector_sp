# app/model.py
import joblib
from pathlib import Path

MODEL_PATH = Path("models/logreg_phishing_final.joblib")

class ModelWrapper:
    def __init__(self, path=MODEL_PATH):
        if not Path(path).exists():
            raise FileNotFoundError(f"⚠️ Modelo no encontrado en {path}")
        
        artifact = joblib.load(path)
        
        # Soportamos dos formatos: dict {model, threshold} o solo el modelo
        if isinstance(artifact, dict):
            self.model = artifact.get("model")
            self.threshold = artifact.get("threshold", 0.5)
        else:
            self.model = artifact
            self.threshold = 0.5

    def predict_proba(self, X) -> float:
        """Devuelve la probabilidad de phishing (clase 1)."""
        if not hasattr(self.model, "predict_proba"):
            raise RuntimeError("❌ El modelo no soporta predict_proba()")
        return float(self.model.predict_proba(X)[0][1])

    def predict_label(self, X) -> int:
        """Aplica el threshold y devuelve la etiqueta 0/1."""
        p = self.predict_proba(X)
        return 1 if p >= self.threshold else 0

# Instancia global al importar el módulo
wrapper = ModelWrapper()
