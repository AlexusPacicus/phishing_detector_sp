#!/usr/bin/env python3
"""
scoring_v2.py
Versión: 2.0 (v1.7)

Este módulo contiene una implementación actualizada del sistema heurístico de
scoring para priorizar URLs sospechosas de phishing orientadas a usuarios en
España.  La versión 2 incorpora las lecciones aprendidas durante el análisis
del conjunto de datos con puntuaciones intermedias (score 4–7) y amplía las
reglas de la versión 1 con señales adicionales relativas al contexto,
infraestructura y patrones lingüísticos.  Las reglas están documentadas en
los comentarios y deben mantenerse sincronizadas con el documento
``docs/scoring.md``.

Principales novedades respecto a la v1:

* Refuerzo de la combinación ``marca + tokens en español``, que puntúa
  significativamente cuando una marca española coincide con algún término
  castellano en el dominio, subdominio o ruta.
* Detección de marcas dentro de la ruta (``brand_in_path``) además de en el
  dominio o subdominio.
* Identificación de tokens de verificación en la ruta (``sms``, ``codigo``,
  ``pin``, ``verificacion``, ``clave``, ``recibir``, ``particulares``,
  ``espera``) mediante la regla ``path_verification_tokens``.
* Reconocimiento de infraestructuras de alojamiento sospechosas y TLDs de
  alto riesgo, otorgando puntos cuando coexisten con contexto español y
  penalizando en ausencia de señales en castellano.
* Penalización de términos ingleses en la ruta o dominio cuando aparecen
  junto a marcas españolas (``english_term_in_path``), para filtrar ruido de
  campañas globales.
* Gestión de falsos positivos en torno a la cadena ``ing`` (``ing_false_positive``
  e ``ing_path_exception``), inspirada en la función ``detect_ing_brand``
  desarrollada durante el análisis.
* Extensión de la lista de hostings gratuitos y proveedores de subdominios
  explotados por phishers.
* Identificación de dominios ``.es`` comprometidos mediante la detección de
  rutas técnicas típicas de WordPress (``wp-``, ``plugins``, ``includes``, etc.),
  etiquetándolos como ``compromised_host_es``.

Estas reglas buscan mejorar la sensibilidad frente a campañas reales sin
incrementar excesivamente los falsos positivos.  La puntuación resultante se
utiliza para filtrar y priorizar URLs en el pipeline de limpieza.
"""

import sys
import logging
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from rapidfuzz import fuzz

logger = logging.getLogger("scoring_v2")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
#  Carga de whitelist
# ---------------------------------------------------------------------------
def load_spanish_whitelist(path: Path) -> list:
    """
    Carga un fichero de dominios españoles de referencia (CSV o TXT) y
    devuelve una lista de cadenas en minúsculas.  Se utiliza tanto para
    coincidencias exactas como para coincidencias difusas (fuzzy matching) en
    la función de scoring.

    :param path: Ruta del fichero de whitelist.
    :return: Lista de dominios en minúsculas.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"❌ Whitelist no encontrada: {path}")
    try:
        df = pd.read_csv(path)
        col = df.columns[0]
        return df[col].astype(str).str.lower().str.strip().tolist()
    except Exception:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]


# ---------------------------------------------------------------------------
#  Reglas y listas de señales
# ---------------------------------------------------------------------------

# Marcas españolas conocidas (banca, logística, administración, telecomunicaciones)
SPANISH_BRANDS = [
    'santander', 'bbva', 'caixabank', 'bankinter', 'ing', 'unicaja',
    'correos', 'aeat', 'dgt', 'ionos', 'orange', 'movistar', 'mapfre',
    'seg-social', 'gobierno', 'dhl', 'seur', 'bbvaabank'
]

# Tokens genéricos en castellano (clientes, transacciones, envíos, administración)
SPANISH_TOKENS = [
    'cliente', 'clientes', 'tarjeta', 'pago', 'pagos', 'factura', 'facturas',
    'multa', 'acceso', 'login', 'entrada', 'inicio', 'sesion', 'seguridad',
    'confirmacion', 'verificacion', 'envio', 'entrega', 'paquete', 'paquetes',
    'pedido', 'pedidos', 'datos', 'perfil', 'cuenta', 'cuentas', 'portal',
    'notificacion', 'notificaciones', 'aviso', 'mensajeria', 'mensaje', 'mensajes',
    'actualizacion', 'renovar', 'renovacion', 'certificado', 'usuario', 'usuarios',
    'banco', 'banca', 'oficina', 'oficinavirtual', 'movil', 'bancamovil',
    'suscripcion', 'compra', 'compras', 'recibo', 'recibos', 'gob', 'oficial',
    'tramite', 'tramites', 'agencia', 'impuestos', 'dni', 'salud', 'sanidad',
    'seg-social', 'particulares', 'forma', 'espera', 'recibir', 'codigo', 'clave',
    'sms', 'pin', 'verificacion', 'token', 'firma', 'validacion'
]

# Detectores de tokens de verificación presentes en rutas de phishing bancario
VERIFICATION_TOKENS = [
    'sms', 'codigo', 'pin', 'verificacion', 'clave', 'token', 'pin', 'dni',
    'recibir', 'espera', 'forma', 'codigo_incorrecta', 'codigo_incorrecto'
]

# Marcadores geográficos o monetarios españoles
SPANISH_MARKERS = ['.es', '+34', '€']

# Hostings españoles gratuitos o ampliamente utilizados por campañas en castellano
SPANISH_HOSTINGS = [
    'webcindario', 'rf.gd', 'tempurl.host', '10web.site', 'freewebhostmost.com',
    'preview-domain.com', 'codeanyapp.com', 'fsthosting.com', 'cprapid.com',
    'suportededicado.net', 'page.link', 'firebaseapp.com', 'web.app', 'appspot.com',
    'pages.dev', 'weebly.com'
]

# TLDs de alto riesgo frecuentemente abusados en phishing (gTLDs baratos)
RISKY_TLDS = [
    '.xyz', '.top', '.shop', '.bond', '.info', '.vip', '.cc', '.online',
    '.lol', '.site', '.casa', '.cloud', '.live', '.host', '.support',
    '.review', '.link', '.app', '.dev', '.ml', '.tk', '.ga', '.cf'
]

# TLDs latinoamericanos que suelen usarse en campañas fuera de España
LATAM_TLDS = [
    '.co', '.mx', '.cl', '.ar', '.br', '.pe', '.ec', '.uy', '.py', '.bo',
    '.sv', '.hn', '.cr', '.gt', '.do'
]

# Tokens portugueses que indican contenido no español
PORTUGUESE_TOKENS = ['pagamento', 'fatura', 'faturas', 'acesso', 'conta', 'cliente-pt']

# Marcas latinoamericanas o bancos regionales para descartar
LATAM_BRANDS = ['banrural', 'pichincha', 'itau', 'bradesco', 'yape', 'daviplata']

# Palabras inglesas frecuentes en campañas globales que se penalizan cuando
# aparecen en URLs con marcas españolas
ENGLISH_TOKENS = [
    'reset', 'secure', 'security', 'details', 'update', 'validation', 'validate',
    'online', 'account', 'user', 'users', 'customer', 'customers', 'payees',
    'authorize', 'authorization', 'login', 'access', 'confirm', 'payment',
    'invoice', 'billing', 'statement', 'service', 'services', 'support',
    'details', 'sessions', 'portal'
]

# Patrones de hostings efímeros basados en "ingress" y dominios .ewp.live
INGRESS_REGEX = re.compile(r"ingress-[a-z0-9]+\.ewp\.live")


def _extract_core_domain(netloc: str) -> str:
    """Extrae el segundo nivel de dominio para fuzzy matching."""
    parts = netloc.split('.')
    return parts[-2] if len(parts) >= 2 else netloc


def score_url_v2(url: str, spanish_whitelist: list):
    """
    Calcula la puntuación heurística de una URL según la versión 2 del modelo.
    Devuelve una tupla (score:int, signals:str).
    """
    url_low = str(url).lower()
    parsed = urlparse(url_low)
    netloc = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''

    # El core del dominio (sin TLD) para fuzzy matching de marcas y whitelist
    core = _extract_core_domain(netloc)

    score = 0
    signals = []

    # ------------------------------------------------------------------
    # 1. Detectar marcas españolas y tokens castellanos
    # ------------------------------------------------------------------
    has_spanish_brand = False
    for b in SPANISH_BRANDS:
        if b in url_low:
            score += 1
            signals.append(f'spanish_brand:{b}')
            has_spanish_brand = True

    # Tokens en español (palabras clave)
    spanish_token_count = 0
    for tok in SPANISH_TOKENS:
        if tok in url_low:
            score += 1
            signals.append(f'spanish_token:{tok}')
            spanish_token_count += 1

    # Marcadores .es, +34, €
    for marker in SPANISH_MARKERS:
        if marker in url_low:
            # Bonus mayor para .es; euro y +34 suman 1
            if marker == '.es':
                score += 2
            else:
                score += 1
            signals.append(f'spanish_marker:{marker}')

    # Hostings españoles o comunes en phishing hispano
    for host in SPANISH_HOSTINGS:
        if host in netloc:
            score += 2
            signals.append(f'spanish_hosting:{host}')

    # --------------------------------------------------------------
    # 2. Combos y contextos
    # --------------------------------------------------------------
    # Marca + token español: señal fuertemente indicativa
    if has_spanish_brand and spanish_token_count >= 1:
        score += 3
        signals.append('brand_and_spanish_token_boost')

    # Marca en el path (no solo en host)
    # Excluimos la coincidencia en netloc para evitar duplicados
    path_lower = path.lower()
    for b in SPANISH_BRANDS:
        if b in path_lower and b not in netloc:
            score += 2
            signals.append(f'brand_in_path:{b}')
            break

    # Tokens de verificación en path
    for vt in VERIFICATION_TOKENS:
        if vt in path_lower:
            score += 2
            signals.append(f'path_verification_tokens:{vt}')
            break

    # Marca en subdominio (por ejemplo, bbva-login.com)
    try:
        subdomain = '.'.join(netloc.split('.')[:-2])
        if subdomain:
            for b in SPANISH_BRANDS:
                if b in subdomain:
                    score += 2
                    signals.append('brand_in_subdomain')
                    break
    except Exception:
        pass

    # Marca española en TLD global (com, net, org, app, etc.)
    has_es_in_netloc = '.es' in netloc
    if has_spanish_brand and any(netloc.endswith(tld) for tld in ['.com', '.net', '.org', '.app', '.dev']) and not has_es_in_netloc:
        score += 2
        signals.append('brand_global_tld_boost')

    # Dominio con TLD de alto riesgo y contexto español → boost moderado
    if any(netloc.endswith(tld) for tld in RISKY_TLDS):
        score += 1
        signals.append('tld_riesgo_alto')
        # Si además hay marca y tokens, reforzar el contexto español
        if has_spanish_brand and spanish_token_count >= 1:
            score += 2
            signals.append('foreign_tld_but_es_context')

    # Hostings de riesgo/ingress
    if any(h in netloc for h in ['fsthosting', 'codeanyapp', 'preview-domain', 'cprapid', 'suportededicado']):
        score += 1
        signals.append('suspicious_host')

    # Patrón ingress de ewp.live (campañas automáticas)
    if INGRESS_REGEX.search(netloc):
        score += 2
        signals.append('host_ingress_pattern')

    # Shorteners con tokens españoles
    shorteners = ['l.ead.me', 'bit.ly', 't.co', 'tinyurl.com', 'ow.ly', 'is.gd', 'page.link']
    if any(s in netloc for s in shorteners):
        short_tokens = ['es', 'spain', 'bbva', 'correos', 'ing', 'santander', 'caixabank']
        if any(tok in path_lower or tok in query for tok in short_tokens):
            score += 2
            signals.append('shortener_spain')

    # --------------------------------------------------------------
    # 3. Penalizaciones
    # --------------------------------------------------------------
    # TLD latinoamericano
    for tld in LATAM_TLDS:
        if netloc.endswith(tld):
            score -= 2
            signals.append(f'latam_tld:{tld}')
            break

    # Tokens en portugués
    for pt in PORTUGUESE_TOKENS:
        if pt in url_low:
            score -= 2
            signals.append(f'pt_kw:{pt}')
            break

    # Marcas latinoamericanas
    for lb in LATAM_BRANDS:
        if lb in url_low:
            score -= 1
            signals.append(f'latam_brand:{lb}')
            break

    # Tokens ingleses en el path o host cuando hay marca española y pocos tokens en español
    if has_spanish_brand:
        english_hits = [tok for tok in ENGLISH_TOKENS if tok in url_low]
        # Sólo penaliza si la presencia de tokens españoles es baja (0 o 1)
        if english_hits and spanish_token_count <= 1:
            score -= 1
            signals.append('english_term_in_path')

    # Falso positivo de "ing": detectamos si "ing" aparece embebido en palabras
    # más largas (p. ej., hiringindia) sin ser la marca del banco ING.
    ing_false_positive = False
    if 'ing' in url_low:
        # Si la palabra exacta "ing" está en algún label del host, es marca real
        labels = netloc.split('.')
        brand_real = any(label == 'ing' for label in labels)
        # Whitelist de ing legítimo
        if not brand_real and not re.search(r"\bing(\.|-|bank|direct|es|\.es)\b", url_low):
            # Buscar tokens que contienen "ing" dentro de palabras más largas
            for token in re.split(r'[\-/._]', netloc + path):
                if re.search(r'[a-z]+ing[a-z]+', token):
                    ing_false_positive = True
                    break
    if ing_false_positive:
        score -= 2
        signals.append('ing_false_positive')
        # Excepción: si además hay tokens españoles → compensar
        if spanish_token_count >= 1:
            score += 2
            signals.append('ing_path_exception')

    # Detectar dominios .es comprometidos (WP hack)
    compromised = False
    if '.es' in netloc:
        # Rutas técnicas que indican hackeo de webs legítimas
        if re.search(r'(wp-|plugins|themes|includes|vendor/phpunit|css/|js/|webmail)', path_lower):
            compromised = True
    if compromised:
        score -= 5
        signals.append('compromised_host_es')

    # Fuzzy match con whitelist de dominios legítimos
    for legit in spanish_whitelist:
        if legit in url_low:
            score += 2
            signals.append(f'spanish_whitelist_match:{legit}')
            break
        else:
            sim = fuzz.ratio(core, legit.split('.')[0])
            if sim >= 80:
                score += 2
                signals.append(f'fuzzy_whitelist_match:{legit}:{sim:.0f}')
                break

    return score, ';'.join(signals)


def apply_scoring_v2(df: pd.DataFrame, whitelist_path: Path) -> pd.DataFrame:
    """
    Aplica la función ``score_url_v2`` a un DataFrame con una columna ``url``
    y devuelve un nuevo DataFrame con las columnas añadidas: ``score_total``,
    ``signals_detected``, ``timestamp`` y ``scoring_version``.

    :param df: DataFrame con una columna ``url``.
    :param whitelist_path: Ruta al fichero de dominios legítimos.
    :return: DataFrame anotado con el scoring v2.
    """
    whitelist = load_spanish_whitelist(whitelist_path)
    df = df.copy()
    logger.info("Aplicando scoring_v2 a %d URLs", len(df))
    df['score_total'], df['signals_detected'] = zip(*df['url'].apply(lambda x: score_url_v2(x, whitelist)))
    df['timestamp'] = datetime.now().isoformat()
    df['scoring_version'] = 'v2 (v1.7)'
    return df


def _read_input_file(input_path: Path) -> pd.DataFrame:
    """Lee un CSV o TXT y devuelve un DataFrame con una columna ``url``."""
    if not input_path.exists():
        raise FileNotFoundError(f"❌ Archivo de entrada no encontrado: {input_path}")
    try:
        df = pd.read_csv(input_path)
        if 'url' not in df.columns:
            first_col = df.columns[0]
            df = df[[first_col]].rename(columns={first_col: 'url'})
    except Exception:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]
        df = pd.DataFrame({'url': lines})
    if df.empty:
        raise ValueError(f"⚠️ Archivo de entrada vacío: {input_path}")
    return df[['url']].dropna().reset_index(drop=True)


def main(input_file: Path, whitelist_path: Path, out_dir: Path):
    """
    Lector de fichero, deduplicador y aplicador del scoring.  Se encarga de
    separar las URLs según umbrales de puntuación (≥7, 4–6, ≤4) y guardar
    los resultados en CSVs independientes en ``out_dir``.

    :param input_file: Ruta del fichero de entrada (CSV o TXT).
    :param whitelist_path: Ruta del fichero de whitelist de dominios españoles.
    :param out_dir: Directorio de salida para guardar los resultados.
    """
    if not out_dir.exists():
        raise FileNotFoundError(f"❌ Directorio de salida inexistente: {out_dir}")
    df_in = _read_input_file(input_file)
    original_count = len(df_in)

    # Deduplicado básico por URL normalizada
    df_in['url_norm'] = df_in['url'].str.strip().str.lower().str.rstrip('/')
    df_in = df_in.drop_duplicates(subset='url_norm').drop(columns='url_norm').reset_index(drop=True)
    logger.info("🧹 Dedupl. URLs: %d → %d (%.2f%% eliminadas)",
                original_count, len(df_in), 100 * (1 - len(df_in)/original_count))

    # Scoring
    df_scored = apply_scoring_v2(df_in, whitelist_path=whitelist_path)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"feed_scored_v2_{ts}.csv"
    df_scored.to_csv(out_file, index=False)
    logger.info("✅ Scoring v2 completado — %d URLs procesadas", len(df_scored))
    print(f"✅ Output guardado en: {out_file}")

    # Separación por score
    base = out_file.stem
    df_gt7 = df_scored[df_scored['score_total'] >= 7]
    df_4to7 = df_scored[(df_scored['score_total'] > 4) & (df_scored['score_total'] < 7)]
    df_le4 = df_scored[df_scored['score_total'] <= 4]
    df_gt7.to_csv(out_dir / f"{base}_score_gt7.csv", index=False)
    df_4to7.to_csv(out_dir / f"{base}_score_4to7.csv", index=False)
    df_le4.to_csv(out_dir / f"{base}_score_le4.csv", index=False)

    print(f"📂 Subarchivos guardados en {out_dir}:")
    print(f"  🔹 score ≥ 7:     {len(df_gt7)} URLs → {base}_score_gt7.csv")
    print(f"  🔸 4 < score < 7: {len(df_4to7)} URLs → {base}_score_4to7.csv")
    print(f"  ⚪ score ≤ 4:     {len(df_le4)} URLs → {base}_score_le4.csv")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Aplica scoring_v2 a un fichero de URLs")
    parser.add_argument('--input', '-i', required=True, help='Fichero de entrada (CSV o TXT)')
    parser.add_argument('--whitelist', '-w', required=True, help='Whitelist de dominios españoles')
    parser.add_argument('--out', '-o', required=True, help='Directorio de salida para los resultados')
    args = parser.parse_args()
    main(Path(args.input), Path(args.whitelist), Path(args.out))