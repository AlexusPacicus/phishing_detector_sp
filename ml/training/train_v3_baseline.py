import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from datetime import datetime
import hashlib
import joblib
import json

# 1. Cargar dataset contractual
DATASET_PATH = "data/interim/dataset_v3_features.csv"
df = pd.read_csv(DATASET_PATH)

# 2. Validar vector contractual
FEATURES_V3 = [
    "domain_complexity", "domain_whitelist", "trusted_token_context",
    "host_entropy", "infra_risk", "brand_in_path", "brand_match_flag"
]

if not all(f in df.columns for f in FEATURES_V3):
    raise ValueError("Faltan features contractuales en el dataset v3.")
if "label" not in df.columns:
    raise ValueError("Falta columna 'label' en el dataset v3.")

# 3. Anti-leakage: agrupar exclusivamente por ENTIDAD (contractual)
groups = df["entidad"].astype(str)

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

(train_idx, test_idx) = next(gss.split(df, groups=groups))

X_train = df.iloc[train_idx][FEATURES_V3].values
y_train = df.iloc[train_idx]["label"].values

X_test = df.iloc[test_idx][FEATURES_V3].values
y_test = df.iloc[test_idx]["label"].values

# 4. Entrenamiento LogisticRegression (parámetros contractuales)
clf = LogisticRegression(
    solver="lbfgs",
    C=1.0,
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

clf.fit(X_train, y_train)

# 5. Métricas obligatorias
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

metrics = {
    "precision": float(precision_score(y_test, y_pred)),
    "recall": float(recall_score(y_test, y_pred)),
    "f1": float(f1_score(y_test, y_pred)),
    "roc_auc": float(roc_auc_score(y_test, y_prob))
}

# 6. Guardar modelo contractual
joblib.dump(clf, "models/logreg_phishing_v3.joblib")

# 7. Función hash contractual
def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 8. Metadata contractual
metadata = {
    "version": "3.0",
    "model_type": "LogisticRegression",
    "features": FEATURES_V3,

    "dataset_file": DATASET_PATH,
    "dataset_hash": file_sha256(DATASET_PATH),

    "split": {
        "method": "GroupShuffleSplit",
        "train_size": 0.8,
        "test_size": 0.2,
        "random_state": 42,
        "group_key": "entidad"
    },

    "threshold": 0.5,
    "metrics": metrics,
    "training_date": datetime.now().isoformat(timespec="seconds")
}

with open("models/logreg_phishing_v3_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
