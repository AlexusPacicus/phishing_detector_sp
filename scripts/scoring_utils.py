# scripts/scoring_utils.py
from urllib.parse import urlparse, unquote
import unicodedata
from typing import Dict

def norm_text(s: str) -> str:
    """Minúsculas + sin acentos. No asume que s sea str."""
    if not isinstance(s, str):
        return ""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def parse_url(url: str) -> Dict[str, str]:
    """
    Devuelve piezas clave de la URL de forma tolerante a errores.
    Campos: domain, tld, path, query, protocol, url_norm
    """
    if not isinstance(url, str) or not url.strip():
        return dict(domain="", tld="", path="", query="", protocol="", url_norm="")
    u = url.strip()
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    try:
        p = urlparse(u)
    except Exception:
        return dict(domain="", tld="", path="", query="", protocol="", url_norm=norm_text(url))
    domain = p.netloc.lower()
    path = unquote(p.path or "")
    query = p.query or ""
    protocol = (p.scheme or "").lower()

    # tld ingenuo: última parte tras el punto. lo refinaremos si hace falta.
    tld = ""
    if domain and "." in domain:
        tld = "." + domain.split(".")[-1]

    return {
        "domain": domain,
        "tld": tld,
        "path": path,
        "query": query,
        "protocol": protocol,
        "url_norm": norm_text(url),
    }
