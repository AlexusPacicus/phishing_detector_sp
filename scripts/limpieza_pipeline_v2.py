#!/usr/bin/env python3
"""
limpieza_pipeline_v2.py
Autor: Alexis Zapico Fernández

Pipeline para:
- Cargar dataset de URLs crudas.
- Aplicar scoring v2.
- Detectar y excluir infraestructura comprometida.
- Deduplicar por dominio y por plantilla de ruta.
- Exportar CSV final para curación manual.

Versión: 2.1
"""

# === 📦 IMPORTS ===
import pandas as pd
import re
import sys
from urllib.parse import urlparse
from pathlib import Path
from rapidfuzz import fuzz
import matplotlib.pyplot as plt

# === ⚙️ CONFIGURACIÓN ===
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data/raw/phishing/database-phishing.txt"
WHITELIST_PATH = BASE_DIR / "docs/spanish_domains.csv"
OUTPUT_DIR = BASE_DIR / "outputs/phishing_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === 🧠 FUNCIONES AUXILIARES ===
def load_urls(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        sys.exit(f"❌ ERROR: No se encontró el archivo {path}")

def extract_domain(url):
    return urlparse(url).netloc.lower()

def extract_path(url):
    return urlparse(url).path.lower()

def normalize_path(path):
    path = re.sub(r"[0-9a-f]{6,}", "", path)
    path = re.sub(r"[_\-]?[0-9]+", "", path)
    return path

def is_host_compromised(url):
    pattern = (
        r"(wp-|plugins|themes|includes|vendor/|phpunit|webmail|wp-admin|"
        r"wp-content|/css|/js|phpmyadmin|/admin|cgi-bin)"
    )
    return bool(re.search(pattern, url, re.IGNORECASE))

def load_whitelist(path):
    if not path.exists():
        sys.exit(f"❌ ERROR: No se encontró el archivo de whitelist en {path}")
    return pd.read_csv(path)["domain"].str.lower().tolist()

# === 🚀 PIPELINE PRINCIPAL ===
if __name__ == "__main__":
    from scoring_v2 import score_url_v2

    print("🚀 Iniciando pipeline de limpieza v2...\n")

    # 1️⃣ Cargar URLs
    urls = load_urls(INPUT_PATH)
    df = pd.DataFrame({"url": urls})
    print(f"✅ Cargadas {len(df):,} URLs")

    # 2️⃣ Cargar whitelist y aplicar scoring
    spanish_whitelist = load_whitelist(WHITELIST_PATH)
    df["score_total_v2"], df["signals_v2"] = zip(*df["url"].map(lambda u: score_url_v2(u, spanish_whitelist)))

    # 3️⃣ Filtrar por score ≥12
    df_high = df[df["score_total_v2"] >= 12].copy()
    df_high["domain"] = df_high["url"].map(extract_domain)
    df_high["path"] = df_high["url"].map(extract_path)
    df_high["path_base"] = df_high["path"].map(normalize_path)
    df_high["host_compromised"] = df_high["url"].map(is_host_compromised)
    print(f"🔍 URLs con score ≥12: {len(df_high):,}")
    print(f"⛔️ Infraestructura comprometida detectada: {df_high['host_compromised'].sum():,}")

    # 4️⃣ Eliminar comprometidos
    df_clean = df_high[~df_high["host_compromised"]].copy()

    # 5️⃣ Deduplicar por dominio y por plantilla de ruta
    df_clean = df_clean.drop_duplicates(subset=["domain"])
    df_clean = df_clean.drop_duplicates(subset=["path_base"])

    # 6️⃣ Preparar columnas para curación manual
    for col in ["sector", "entidad", "inclusion", "notas"]:
        df_clean[col] = ""

    df_final = df_clean[["url", "domain", "score_total_v2", "signals_v2", "sector", "entidad", "inclusion", "notas"]]

    # 7️⃣ Exportar CSV limpio
    out_csv = OUTPUT_DIR / "phishing_v2_limpieza_manual.csv"
    df_final.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"\n✅ Exportado archivo limpio con {len(df_final):,} URLs → {out_csv}")

    # 8️⃣ Graficar distribución de score
    plt.figure(figsize=(10, 5))
    df["score_total_v2"].hist(bins=range(df["score_total_v2"].min(), df["score_total_v2"].max()+1), edgecolor="black")
    plt.title("Distribución de scores (v2)")
    plt.xlabel("score_total_v2")
    plt.ylabel("Número de URLs")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "distribucion_scores.png")
    plt.close()
    print(f"📊 Gráfico de distribución guardado en {OUTPUT_DIR / 'distribucion_scores.png'}")

    print("\n🏁 Pipeline de limpieza completado.")
