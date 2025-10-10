#!/usr/bin/env python3
"""
scoring_utils.py
Versión: 1.0 (v2.6 interna)
Autor: Alexis Zapico Fernández

Descripción:
Sistema heurístico de scoring para priorizar URLs de phishing orientadas a España (versión v1).
Basado en las reglas documentadas en docs/scoring.md.
"""

# ===============================================================
# 📦 IMPORTS
# ===============================================================
import sys
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from rapidfuzz import fuzz

# ===============================================================
# 🧭 RUTAS Y CONSTANTES (modo mixto: script / notebook)
# ===============================================================
# === RUTAS Y CONSTANTES ===
try:
    # Si se ejecuta como script .py
    REPO_ROOT = Path(__file__).resolve().parents[3]  # sube desde limpieza/phishing/scoring/
except NameError:
    # Si se ejecuta desde notebook
    REPO_ROOT = Path.cwd().parents[2]

DATA_RAW = REPO_ROOT / "data" / "raw" / "phishing"
DATA_INTERIM = REPO_ROOT / "data" / "interim" / "phishing"
DATA_PROCESSED = DATA_INTERIM  # para consistencia
INPUT_FILE = DATA_RAW / "database-phishing.txt"
DEFAULT_WHITELIST = REPO_ROOT / "docs" / "spanish_domains.csv"
# ===============================================================
# 🧩 LOGGING
# ===============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("scoring_utils")

# ===============================================================
# 🔑 FUNCIONES AUXILIARES
# ===============================================================

def load_spanish_whitelist(path: Path) -> list:
    """
    Carga una whitelist de dominios españoles (CSV o TXT).
    Devuelve una lista de strings en minúscula.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"❌ Whitelist no encontrada: {path}")

    try:
        df = pd.read_csv(path)
        col = df.columns[0]
        whitelist = df[col].astype(str).str.lower().str.strip().tolist()
        logger.info("Whitelist cargada (%d dominios) desde %s", len(whitelist), path)
        return whitelist
    except Exception:
        with open(path, "r", encoding="utf-8") as f:
            whitelist = [line.strip().lower() for line in f if line.strip()]
        logger.info("Whitelist cargada (TXT) — %d dominios desde %s", len(whitelist), path)
        return whitelist


# ===============================================================
# ⚖️ FUNCIÓN PRINCIPAL DE SCORING (v1)
# ===============================================================

def score_url_v1(url: str, spanish_whitelist: list):
    """
    Implementación del sistema heurístico de scoring (v1 / v2.6 interna).
    Basado en reglas lingüísticas, geográficas y de marca.
    Devuelve: (score:int, signals:str)
    """
    url_low = str(url).lower()
    parsed = urlparse(url_low)
    netloc = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''
    domain_core = netloc.split('.')[-2] if '.' in netloc else netloc

    score = 0
    signals = []

    # --- Listas base ---
    POSITIVE_KEYWORDS = ['multa', 'pago', 'verificación', 'cliente', 'acceso', 'seguridad', 'confirmación', 'factura', 'tarjeta']
    SPANISH_MARKERS = ['.es', '+34', '€']
    SPANISH_BRANDS = ['santander', 'bbva', 'caixabank', 'ing', 'bankia', 'openbank', 'ionos', 'orange', 'movistar', 'correos', 'dgt']
    SPANISH_HOSTINGS = ['webcindario', 'rf.gd']

    GENERIC_SP_TOKENS = [
        'servicio', 'soporte', 'atencion', 'cliente', 'usuarios', 'ayuda', 'asistencia',
        'cuenta', 'acceso', 'inicio', 'login', 'sesion', 'datos', 'perfil', 'portal',
        'seguridad', 'verificacion', 'confirmacion', 'actualizacion', 'validacion', 'auth', 'clave', 'codigo',
        'envio', 'entrega', 'paquete', 'pedido', 'multa', 'factura', 'notificacion', 'aviso',
        'gob', 'oficial', 'tramite', 'tramites', 'agencia', 'impuestos', 'certificado'
    ]

    BANKING_TOKENS = [
        'banco', 'banca', 'bank', 'banking', 'transferencia', 'tarjeta', 'pin', 'clave', 'codigo', 'validacion',
        'firma', 'token', 'sms', 'autenticacion', 'movimientos', 'saldo', 'oficinavirtual', 'bancamovil',
        'appbanco', 'bancadigital', 'acceso', 'usuarios', 'verificacion', 'serviciocliente', 'soportecliente'
    ]

    INSTITUTIONAL_TOKENS = [
        'ayuntamiento', 'gob', 'gobierno', 'agencia', 'tramite', 'tramites', 'oficial', 'certificado',
        'seg-social', 'catastro', 'impuestos', 'tributos', 'dgt', 'hacienda', 'dni', 'salud', 'sanidad'
    ]

    PROFESSIONAL_TOKENS = [
        'asesoria', 'gestoria', 'abogado', 'despacho', 'consultoria', 'contable', 'laboral', 'fiscal', 'bufete', 'notaria'
    ]

    ECOMMERCE_TOKENS = [
        'pedido', 'pedidos', 'compra', 'compras', 'factura', 'facturas', 'recibo', 'recibos',
        'abonado', 'tarifa', 'tarifas', 'servicios', 'renovar', 'renovacion', 'contrato',
        'suscripcion', 'envio', 'entrega', 'paquete', 'envios', 'devolucion'
    ]

    LATAM_TLDS = ['.co', '.mx', '.cl', '.ar', '.br', '.pe', '.ec', '.uy', '.py', '.bo', '.sv', '.hn', '.cr', '.gt', '.do']
    GLOBAL_TLDS = ['.com', '.app', '.net', '.org', '.io', '.web.app', '.dev']

    # --- Reglas principales ---
    for kw in POSITIVE_KEYWORDS:
        if kw in url_low:
            score += 1
            signals.append(f'has_kw:{kw}')

    for m in SPANISH_MARKERS:
        if m in url_low:
            score += 2 if m == '.es' else 1
            signals.append(f'spanish_marker:{m}')

    for b in SPANISH_BRANDS:
        if b in url_low:
            score += 1
            signals.append(f'spanish_brand:{b}')

    for h in SPANISH_HOSTINGS:
        if h in url_low:
            score += 2
            signals.append(f'spanish_hosting:{h}')

    if '.com.es' in url_low:
        score += 2
        signals.append('tld_combo_com_es')

    # --- Semánticas compuestas ---
    if '.es' in url_low:
        if sum(tok in url_low for tok in GENERIC_SP_TOKENS) >= 2:
            score += 3
            signals.append('generic_service_combo_es')
        if any(tok in url_low for tok in BANKING_TOKENS):
            score += 3
            signals.append('banking_combo_es')
        if any(tok in url_low for tok in INSTITUTIONAL_TOKENS + PROFESSIONAL_TOKENS):
            score += 3
            signals.append('institutional_professional_es')
        if any(tok in url_low for tok in ECOMMERCE_TOKENS):
            score += 2
            signals.append('ecommerce_combo_es')

    # --- Whitelist exacta + fuzzy ---
    for legit in spanish_whitelist:
        if legit in url_low:
            score += 2
            signals.append(f'spanish_whitelist_match:{legit}')
            break
        else:
            legit_base = legit.split('.')[0]
            sim = fuzz.ratio(domain_core, legit_base)
            if sim >= 80:
                score += 2
                signals.append(f'fuzzy_whitelist_match:{legit}:{sim:.0f}')
                break

    # --- Recuperación y casos específicos ---
    spanish_tokens_for_brand = ['ayuda', 'cliente', 'esapp', 'es', 'spain', 'movil', 'ayuntamiento', 'paqueteria', 'paquete', 'envio', 'entrega']
    if any(b in url_low for b in SPANISH_BRANDS) and any(tok in url_low for tok in spanish_tokens_for_brand):
        score += 2
        signals.append('brand_plus_spanish_token')

    # Marca en subdominio
    try:
        parts = netloc.split('.')
        if len(parts) > 2:
            subdomain_str = '.'.join(parts[:-2])
            if any(b in subdomain_str for b in SPANISH_BRANDS):
                score += 2
                signals.append('brand_in_subdomain')
    except Exception:
        pass

    # Acortadores
    shorteners = ['l.ead.me', 'bit.ly', 't.co', 'tinyurl.com', 'ow.ly', 'is.gd']
    if any(s in netloc for s in shorteners):
        short_tokens = ['spain', 'es', 'dgt', 'bbva', 'correos', 'ing', 'santander', 'caixabank']
        if any(tok in path or tok in query for tok in short_tokens):
            score += 2
            signals.append('shortener_spain')

    # Marca española en TLD global
    try:
        has_spanish_brand = any(b in url_low for b in SPANISH_BRANDS)
        host_has_global_tld = any(tld in netloc for tld in GLOBAL_TLDS)
        host_has_es = '.es' in netloc
        if has_spanish_brand and host_has_global_tld and not host_has_es:
            score += 1
            signals.append('brand_global_tld_boost')
    except Exception:
        pass

    # --- Penalizaciones LATAM ---
    for tld in LATAM_TLDS:
        if url_low.endswith(tld) or f"{tld}/" in url_low:
            score -= 2
            signals.append(f'latam_tld:{tld}')

    for pk in ['pagamento', 'fatura', 'acesso', 'faturas']:
        if pk in url_low:
            score -= 2
            signals.append(f'pt_kw:{pk}')

    for lb in ['banrural', 'pichincha', 'itau', 'bradesco', 'yape', 'daviplata']:
        if lb in url_low:
            score -= 1
            signals.append(f'latam_brand:{lb}')

    # --- Fuzzy brand match ---
    for brand in SPANISH_BRANDS:
        sim = fuzz.ratio(domain_core, brand)
        if sim >= 80:
            score += 2
            signals.append(f'fuzzy_brand_match:{brand}:{sim:.0f}')
            break

    return score, ';'.join(signals)


# ===============================================================
# 🚀 APLICACIÓN MASIVA
# ===============================================================
def apply_scoring_v1(df: pd.DataFrame, whitelist_path: Path = DEFAULT_WHITELIST) -> pd.DataFrame:
    whitelist = load_spanish_whitelist(whitelist_path)
    logger.info("Aplicando scoring_v1 a %d URLs", len(df))
    df = df.copy()
    df['score_total'], df['signals_detected'] = zip(*df['url'].apply(lambda x: score_url_v1(x, whitelist)))
    df['timestamp'] = datetime.now().isoformat()
    df['scoring_version'] = 'v1 (v2.6 interna)'
    return df


# ===============================================================
# 🧭 FUNCIONES DE ENTRADA/SALIDA
# ===============================================================
def _read_input_file(input_path: Path) -> pd.DataFrame:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"❌ Archivo de entrada no encontrado: {input_path}")

    try:
        df = pd.read_csv(input_path)
        if 'url' not in df.columns:
            first_col = df.columns[0]
            df = df[[first_col]].rename(columns={first_col: 'url'})
    except Exception:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        df = pd.DataFrame({'url': lines})

    if df.empty:
        raise ValueError(f"⚠️ Archivo de entrada vacío: {input_path}")

    return df[['url']].dropna().reset_index(drop=True)


# ===============================================================
# 🧩 MAIN CLI
# ===============================================================
def main(input_file: Path = INPUT_FILE, whitelist_path: Path = DEFAULT_WHITELIST, out_dir: Path = DATA_PROCESSED):
    input_file = Path(input_file)
    whitelist_path = Path(whitelist_path)
    out_dir = Path(out_dir)

    # --- Validación de rutas ---
    if not input_file.exists():
        raise FileNotFoundError(f"❌ Archivo de entrada no encontrado: {input_file}")
    if not whitelist_path.exists():
        raise FileNotFoundError(f"❌ Whitelist no encontrada: {whitelist_path}")
    if not out_dir.exists():
        raise FileNotFoundError(f"❌ Directorio de salida inexistente: {out_dir}")

    # === LECTURA INICIAL ===
    df_in = _read_input_file(input_file)
    original_count = len(df_in)

    # === DEDUPLICADO ===
    df_in['url_norm'] = df_in['url'].str.strip().str.lower().str.rstrip('/')
    df_in = df_in.drop_duplicates(subset='url_norm').drop(columns='url_norm').reset_index(drop=True)

    logger.info("🧹 Dedupl. URLs: %d → %d (%.2f%% eliminadas)",
                original_count, len(df_in), 100 * (1 - len(df_in)/original_count))

    # === SCORING ===
    df_scored = apply_scoring_v1(df_in, whitelist_path=whitelist_path)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"feed_scored_v1_{ts}.csv"

    # === Guardado del CSV completo ===
    df_scored.to_csv(out_file, index=False)
    logger.info("✅ Scoring completado — %d URLs procesadas", len(df_scored))
    print(f"✅ Output guardado en: {out_file}")

    # === Separación por score ===
    out_base = out_file.stem
    out_dir = out_file.parent

    df_gt7 = df_scored[df_scored['score_total'] >= 7]
    df_4to7 = df_scored[(df_scored['score_total'] > 4) & (df_scored['score_total'] < 7)]
    df_le4 = df_scored[df_scored['score_total'] <= 4]

    df_gt7.to_csv(out_dir / f"{out_base}_score_gt7.csv", index=False)
    df_4to7.to_csv(out_dir / f"{out_base}_score_4to7.csv", index=False)
    df_le4.to_csv(out_dir / f"{out_base}_score_le4.csv", index=False)

    print(f"📂 Subarchivos guardados en {out_dir}:")
    print(f"  🔹 score ≥ 7:     {len(df_gt7)} URLs → {out_base}_score_gt7.csv")
    print(f"  🔸 4 < score < 7: {len(df_4to7)} URLs → {out_base}_score_4to7.csv")
    print(f"  ⚪ score ≤ 4:     {len(df_le4)} URLs → {out_base}_score_le4.csv")


# ===============================================================
# ENTRY POINT
# ===============================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aplica el sistema de scoring_v1 a un fichero de URLs.")
    parser.add_argument("--input", "-i", default=str(INPUT_FILE), help="Fichero de entrada (CSV o TXT).")
    parser.add_argument("--whitelist", "-w", default=str(DEFAULT_WHITELIST), help="Whitelist de dominios españoles.")
    parser.add_argument("--out", "-o", default=str(DATA_PROCESSED), help="Directorio de salida para los resultados.")
    args = parser.parse_args()

    main(Path(args.input), Path(args.whitelist), Path(args.out))

