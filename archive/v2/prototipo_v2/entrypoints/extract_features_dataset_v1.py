import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd

from features.features_v2 import extract_features_v2
# Cargar dataset v1
df = pd.read_csv("data/clean/dataset_v1.csv", usecols=["url", "label"])

# Cargar whitelist española
wl = pd.read_csv("docs/dominios_espanyoles.csv", usecols=["domain"])
spanish_whitelist = frozenset(
    d.strip().lower()
    for d in wl["domain"].dropna()
)
def safe_extract(url: str):
    """
    Aplica extract_features_v2 a una URL con manejo de errores.
    Siempre devuelve una lista de 9 floats en orden contractual.
    """
    try:
        feats = extract_features_v2(url, spanish_whitelist)

        # Validación de estructura
        if not (isinstance(feats, (list, tuple)) and len(feats) == 9):
            return [0.0] * 9

        # Normalizamos salida a floats
        return [
            float(x) if x not in (None, "", "nan") else 0.0
            for x in feats
        ]

    except Exception:
        # Fallo en parsing, TLD inválido, bug interno, etc.
        return [0.0] * 9

features = df["url"].apply(safe_extract)
features_df = pd.DataFrame(features.tolist(), columns=[
    "domain_complexity",
    "host_entropy",
    "domain_whitelist_score",
    "suspicious_path_token",
    "token_density",
    "trusted_token_context",
    "infra_risk",
    "fake_tld_in_subdomain_or_path",
    "param_count_boost"
])
final_df = pd.concat([df[["url", "label"]].reset_index(drop=True), features_df], axis=1)
final_df.to_csv("data/clean/dataset_v1_features.csv", index=False)
print("Features guardadas en data/clean/dataset_v1_features.csv")
