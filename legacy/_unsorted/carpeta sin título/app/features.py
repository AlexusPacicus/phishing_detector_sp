# app/features.py
from urllib.parse import urlparse
import tldextract
import math
from collections import Counter

# === Listas de tokens / dominios usados en el entrenamiento ===
TRUSTED_TOKENS = ["login", "clientes", "empresas", "banca", "seguridad"]

SUSPICIOUS_TOKENS = ["php", "html", "index", "view", "principal"]

FREE_HOSTINGS = [
    "webcindario.com", "000webhostapp.com", "rf.gd", "hol.es", "biz.nf",
    "blogspot.com", "wordpress.com", "weebly.com", "wix.com",
    "web.app", "firebaseapp.com", "sites.google.com", "godaddysites.com",
    "ead.me", "ucoz.net", "tk", "ml", "ga", "cf", "gq"
]

# === Funciones auxiliares (idénticas al notebook) ===

def domain_entropy(domain: str) -> float:
    """Calcula la entropía de un dominio (idéntico al notebook)."""
    if not domain:
        return 0.0
    counter = Counter(domain)
    probs = [freq / len(domain) for freq in counter.values()]
    return -sum(p * math.log2(p) for p in probs)

def count_params(url: str) -> int:
    """Cuenta el número de parámetros en la query (usando split('&'))."""
    parsed = urlparse(url)
    if parsed.query == "":
        return 0
    return len(parsed.query.split("&"))

def has_trusted_token(url: str) -> int:
    """Devuelve 1 si la ruta contiene un token 'legitimador'."""
    path = urlparse(url).path.lower()
    return 1 if any(tok in path for tok in TRUSTED_TOKENS) else 0

def contains_percent(url: str) -> int:
    """Devuelve 1 si la URL contiene '%', 0 si no."""
    return 1 if "%" in url else 0

def contains_equal(url: str) -> int:
    """Devuelve 1 si la URL contiene '=', 0 si no."""
    return 1 if "=" in url else 0

def get_protocol(url: str) -> int:
    """Devuelve 1 si la URL empieza por https, 0 si no (idéntico al notebook)."""
    return 1 if url.startswith("https") else 0

def get_tld_group(url: str) -> str:
    """Agrupa el TLD en 'es', 'com' o 'otros' (idéntico al notebook)."""
    tld = tldextract.extract(url).suffix.lower()
    if tld == "es":
        return "es"
    elif tld == "com":
        return "com"
    else:
        return "otros"

def has_suspicious_token(url: str) -> int:
    """Devuelve 1 si la ruta contiene un token sospechoso."""
    path = urlparse(url).path.lower()
    return 1 if any(tok in path for tok in SUSPICIOUS_TOKENS) else 0

def is_free_hosting(url: str) -> int:
    """Devuelve 1 si el dominio registrado está en la lista de hostings gratuitos."""
    domain = tldextract.extract(url).registered_domain.lower()
    return 1 if any(host in domain for host in FREE_HOSTINGS) else 0

# === Función principal: extrae todas las features ===

def extract_features(raw_url: str) -> dict:
    """
    Extrae las 10 features finales usadas en el entrenamiento.
    Devuelve un diccionario {feature_name: valor}.
    """
    url = raw_url.strip()
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url  # para parsear correctamente

    tx = tldextract.extract(url)
    domain_raw = tx.domain or ""

    feats = {
        "domain_length": len(domain_raw),
        "domain_entropy": domain_entropy(domain_raw),
        "num_params": count_params(url),
        "trusted_path_token": has_trusted_token(url),
        "contains_percent": contains_percent(url),
        "contains_equal": contains_equal(url),
        "suspicious_path_token": has_suspicious_token(url),
        "free_hosting": is_free_hosting(url),
        "protocol": get_protocol(url),
        "tld_group": get_tld_group(url),
    }
    return feats
