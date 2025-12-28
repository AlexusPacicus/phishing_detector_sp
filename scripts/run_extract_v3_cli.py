"""
Entrypoint CLI contractual v3 (bootstrap único).

Uso:
  python scripts/run_extract_v3_cli.py --input_path <ruta_csv> --output_dir <directorio_salida>

Genera:
  - <output_dir>/dataset_v3_features.csv
  - <output_dir>/dataset_v3_metadata.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import subprocess
from datetime import datetime

import pandas as pd

# Asegura imports desde la raíz del repo cuando se ejecuta como script.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from features.loaders_v3 import initialize_v3  # noqa: E402
from features_v3 import FEATURES_V3, extract_features_v3  # noqa: E402


EXPECTED_BASE_SCHEMA = ["url", "label", "sector", "entidad", "notas", "campaign"]
EXPECTED_SCHEMA = EXPECTED_BASE_SCHEMA + FEATURES_V3


def _fail(msg: str) -> None:
    raise SystemExit(f"[ERROR] {msg}")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], encoding="utf-8").strip()
    except Exception:
        return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extractor contractual v3 (CLI)")
    parser.add_argument("--input_path", required=True, help="Path CSV de entrada (schema base v2)")
    parser.add_argument("--output_dir", required=True, help="Directorio de salida")
    args = parser.parse_args()

    input_path = args.input_path
    if not os.path.isabs(input_path):
        input_path = os.path.join(REPO_ROOT, input_path)

    output_dir = args.output_dir
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(REPO_ROOT, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "dataset_v3_features.csv")
    metadata_path = os.path.join(output_dir, "dataset_v3_metadata.json")

    whitelist_path = os.path.join(REPO_ROOT, "docs", "whitelist.csv")
    brands_path = os.path.join(REPO_ROOT, "docs", "dominios_espanyoles.csv")
    neutral_domains_path = os.path.join(REPO_ROOT, "docs", "global_neutral_domains.csv")

    for p, name in (
        (input_path, "input_path"),
        (whitelist_path, "whitelist_path"),
        (brands_path, "brands_path"),
        (neutral_domains_path, "neutral_domains_path"),
    ):
        if not os.path.isfile(p):
            _fail(f"{name} no encontrado: {p}")

    # Bootstrap único (listas canónicas v3)
    whitelist, constants = initialize_v3(
        whitelist_path=whitelist_path,
        brands_path=brands_path,
    )

    # Carga input (solo schema base)
    df_in = pd.read_csv(input_path)
    if list(df_in.columns) != EXPECTED_BASE_SCHEMA:
        _fail(
            "Schema base incorrecto. "
            f"Esperado: {EXPECTED_BASE_SCHEMA} / Obtenido: {list(df_in.columns)}"
        )

    # Extracción batch v3 (sin re-bootstrap)
    feats = df_in["url"].apply(lambda u: extract_features_v3(u, whitelist, constants))
    feats_df = pd.DataFrame(feats.tolist(), columns=FEATURES_V3)
    df_out = pd.concat([df_in.reset_index(drop=True), feats_df], axis=1)

    # Validaciones contractuales
    if list(df_out.columns) != EXPECTED_SCHEMA:
        _fail(
            "Schema contractual v3 incorrecto. "
            f"Esperado: {EXPECTED_SCHEMA} / Obtenido: {list(df_out.columns)}"
        )
    if df_out[FEATURES_V3].isna().any().any():
        _fail("NaN detectado en FEATURES_V3 (violación contractual)")

    df_out.to_csv(output_path, index=False)

    meta = {
        "version": "3.0",
        "entrypoint": os.path.relpath(__file__, REPO_ROOT),
        "timestamp": datetime.now().isoformat(),
        "commit_hash": _git_commit_hash(),
        "sources": {
            "dataset_base": {
                "path": os.path.relpath(input_path, REPO_ROOT),
                "rows": int(len(df_in)),
                "checksum_sha256": _sha256_file(input_path),
            },
            "whitelist": {
                "path": os.path.relpath(whitelist_path, REPO_ROOT),
                "entries": int(len(whitelist)),
                "checksum_sha256": _sha256_file(whitelist_path),
            },
            "dominios_espanyoles": {
                "path": os.path.relpath(brands_path, REPO_ROOT),
                "checksum_sha256": _sha256_file(brands_path),
            },
            "global_neutral_domains": {
                "path": os.path.relpath(neutral_domains_path, REPO_ROOT),
                "checksum_sha256": _sha256_file(neutral_domains_path),
            },
        },
        "extractor": {
            "module": "features_v3",
            "features": FEATURES_V3,
            "bootstrap": "initialize_v3 (features.loaders_v3)",
        },
        "output": {
            "path": os.path.relpath(output_path, REPO_ROOT),
            "rows": int(len(df_out)),
            "checksum_sha256": _sha256_file(output_path),
            "schema_expected": EXPECTED_SCHEMA,
            "schema_observed": list(df_out.columns),
            "nan_count_features": int(df_out[FEATURES_V3].isna().sum().sum()),
            "whitelist_len": int(len(whitelist)),
            "brands_set_len": int(len(constants["BRANDS_FROM_DOMAINS_ES"])),
        },
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print("✅ Extracción v3 completada (contractual).")
    print("📄 Features:", os.path.relpath(output_path, REPO_ROOT))
    print("🧾 Metadata:", os.path.relpath(metadata_path, REPO_ROOT))


if __name__ == "__main__":
    main()

