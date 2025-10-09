# scripts/features.py

import tldextract
import math
from collections import Counter
from urllib.parse import urlparse

# --- Funciones auxiliares ---

def domain_entropy(domain: str) -> float:
    """Calcula la entropía de un dominio."""
    if not domain:
        return 0.0
    counter = Counter(domain)
    probs = [freq/len(domain) for freq in counter.values()]
    return -sum(p * math.log2(p) for p in probs)


def count_params(url: str) -> int:
    """Cuenta el número de parámetros en la query."""
    parsed = urlparse(url)
    if not parsed.query:
        return 0
    return len(parsed.query.split("&"))


def tld_group(tld: str) -> str:
    """Agrupa TLDs en es, com, seguros y otros (según prototipo)."""
    if tld == "es":
        return "es"
    elif tld == "com":
        return "com"
    elif tld in ["us", "network"]:
        return "seguros"
    else:
        return "otros"


def has_suspicious_token(url: str) -> int:
    """Detecta tokens sospechosos en la ruta de la URL."""
    path = urlparse(url).path.lower()
    SUSPICIOUS_TOKENS = ["php", "html", "index", "view", "principal"]
    return 1 if any(tok in path for tok in SUSPICIOUS_TOKENS) else 0


def has_trusted_token(url: str) -> int:
    """Detecta tokens de confianza en la ruta de la URL."""
    path = urlparse(url).path.lower()
    TRUSTED_TOKENS = ["clientes", "empresas", "banca", "seguridad", "login"]
    return 1 if any(tok in path for tok in TRUSTED_TOKENS) else 0


def is_free_hosting(url: str) -> int:
    """Detecta si la URL usa dominios de hosting gratuito comunes."""
    domain = tldextract.extract(url).registered_domain.lower()
    FREE_HOSTING_DOMAINS = [
        "blogspot.com", "sites.google.com", "webcindario.com", "000webhostapp.com",
        "github.io", "herokuapp.com", "wixsite.com", "weebly.com", "web.app",
        "wordpress.com"
    ]
    return 1 if any(fh in domain for fh in FREE_HOSTING_DOMAINS) else 0


# --- Función principal ---

def extract_features(url: str) -> dict:
    """Extrae las 10 features seleccionadas en el prototipo."""
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    domain = ext.domain
    tld = ext.suffix

    return {
        # Moderadas
        "domain_length": len(domain),
        "domain_entropy": domain_entropy(domain),
        "suspicious_path_token": has_suspicious_token(url),

        # Fuertes
        "num_params": count_params(url),
        "contains_equal": 1 if "=" in url else 0,
        "protocol": 1 if url.startswith("https") else 0,
        "tld_group": tld_group(tld),
        "trusted_path_token": has_trusted_token(url),

        # Específicas
        "contains_percent": 1 if "%" in url else 0,
        "free_hosting": is_free_hosting(url),
    }
