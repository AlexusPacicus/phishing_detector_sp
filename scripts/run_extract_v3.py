# ===============================================================================
# Este script usa exclusivamente initialize_v3() como bootstrap v3 contractual.
# PROHIBIDO pasar whitelists externas o brands_set externos.
# PROHIBIDO usar loaders v2 en este pipeline.
# ===============================================================================

import json
import pandas as pd
from datetime import datetime
import subprocess
from features.features_v3 import FEATURES_V3
from src.features.extract_features_dataset_v3 import extract_features_dataset_v3
from features.loaders_v3 import initialize_v3
import hashlib

# Rutas y bootstrap central
input_path = "data/clean/dataset_v2.csv"
output_path = "data/interim/dataset_v3_features.csv"
whitelist, constants = initialize_v3()

extract_features_dataset_v3(input_path, output_path)

# Commit hash (con fallback)
try:
    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], encoding="utf-8"
    ).strip()
except Exception:
    commit_hash = "unknown"

# Hash rápido de archivos
def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Metadata contractual y validación
df_in = pd.read_csv(input_path)
df_out = pd.read_csv(output_path)

# Validación contractual schema v3
expected_cols = ["url","label","sector","entidad","notas","campaign"] + FEATURES_V3
if list(df_out.columns) != expected_cols:
    raise ValueError(f"Schema columnas v3 incorrecto:\nEsperado: {expected_cols}\nObtenido: {list(df_out.columns)}")
if df_out[FEATURES_V3].isna().any().any():
    raise ValueError("Hay valores NaN en las features v3; el dataset no es contractual.")

meta = {
    "commit_hash": commit_hash,
    "input_path": input_path,
    "output_path": output_path,
    "whitelist_path": "docs/whitelist.csv",
    "brands_path": "docs/dominios_espanyoles.csv",
    "neutral_domains_path": "docs/global_neutral_domains.csv",
    "features_version": "v3",
    "features_list": FEATURES_V3,
    "row_count_input": len(df_in),
    "row_count_output": len(df_out),
    "null_counts_por_feature": {
        f: int(df_out[f].isna().sum()) for f in FEATURES_V3 if f in df_out.columns
    },
    "timestamp": datetime.now().isoformat(),
    "schema_expected": expected_cols,
    "schema_observed": list(df_out.columns),
    "input_hash": file_hash(input_path),
    "output_hash": file_hash(output_path),
    "whitelist_len": len(whitelist),
    "brands_set_len": len(constants["BRANDS_FROM_DOMAINS_ES"]),
}

with open("data/interim/dataset_v3_metadata.json", "w") as f:
    json.dump(meta, f, indent=2)
