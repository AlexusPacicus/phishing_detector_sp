
"""
features_v2_final_autowhitelist.py
==================================
Versión final v2.2 con carga automática de whitelist desde `docs/dominios_espanyoles.csv`.
- Si no se pasa `whitelist_csv` ni `whitelist_cache`, se carga automáticamente desde esa ruta.
- Lanza FileNotFoundError si el archivo no existe.
- Incluye bloque de test en `__main__`.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse, parse_qs

import pandas as pd

try:
    import tldextract  # type: ignore
except Exception:  # pragma: no cover
    tldextract = None

# Ruta por defecto para la whitelist
DEFAULT_WHITELIST_PATH = "docs/dominios_espanyoles.csv"


# -------------------------------
# Listas base
# -------------------------------

ACTION_TOKENS: set[str] = {
    "verificar","verify","sms","codigo","clave","paquete","envio","aduanas","pago",
    "login","clientes","portal","seguridad","actualizar","confirmar","acceso"
}

SUSPICIOUS_TOKENS: set[str] = {
    "php","html","index","view","principal","confirmacion","3d","no-back-button","asset","secure"
}

TRUSTED_TOKENS: set[str] = {
    "clientes","empresas","banca","seguridad","login","soporte","help","status","docs","faq",
    "particulares","personas","area-cliente","portal"
}

FREE_HOSTING_SUFFIXES: tuple[str, ...] = (
    "webcindario.com","rf.gd","000webhostapp.com","blogspot.com","sites.google.com","web.app",
    "godaddysites.com","replit.app","tempsite.link","github.io","wixsite.com","pages.dev"
)

OAUTH_HOSTS_SUFFIX: tuple[str, ...] = (
    "login.microsoftonline.com","accounts.google.com","auth0.com","okta.com","id.atlassian.com","appleid.apple.com"
)

OAUTH_TOKENS_IN_PATH: set[str] = {"authorize","oauth","callback","redirect_uri","signin","sso","login"}

TLD_HIGH_RISK: set[str] = {".live",".xyz",".top",".monster",".cyou",".tk",".gq",".ml",".shop"}
TLD_MID_RISK: set[str]  = {".app",".online",".site",".click",".link",".icu",".me",".info"}


# -------------------------------
# Utilidades
# -------------------------------

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    n = len(text)
    return -sum((c/n) * math.log2(c/n) for c in Counter(text).values())

def _safe_tldextract(host: str):
    if not host:
        return "", "", ""
    if tldextract:
        ex = tldextract.extract(host)
        return ex.subdomain, ex.domain, ex.suffix
    parts = host.split(".")
    if len(parts) < 2:
        return "", host, ""
    sub = ".".join(parts[:-2]) if len(parts) > 2 else ""
    dom = parts[-2]
    suf = parts[-1]
    return sub, dom, suf

def _tokenize_path(path: str) -> list[str]:
    return [p for p in re.split(r"[-_/\.?=&]+", path.lower()) if p]

def _is_free_hosting(host: str) -> int:
    h = host.lower()
    return int(any(h == sfx or h.endswith("." + sfx) for sfx in FREE_HOSTING_SUFFIXES))

def _tld_risk_weight(suffix: str) -> float:
    tld = ("." + suffix.lower()) if suffix else ""
    if tld in TLD_HIGH_RISK:
        return 1.0
    if tld in TLD_MID_RISK:
        return 0.6
    return 0.0

def _load_whitelist(csv_path: Optional[str]) -> set[str]:
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(
            "No se encontró la whitelist en 'docs/dominios_espanyoles.csv'. "
            "Ejecuta el script de generación o especifica un whitelist_csv manual."
        )
    wl: set[str] = set()
    df = pd.read_csv(csv_path)
    for col in ("domain","dominio","url","host"):
        if col in df.columns:
            wl = set(df[col].dropna().astype(str).str.lower().str.strip().tolist())
            break
    if not wl and len(df.columns) > 0:
        wl = set(df.iloc[:,0].dropna().astype(str).str.lower().str.strip().tolist())
    return wl

def _whitelist_strength(host: str, wl: set[str]) -> float:
    h = host.lower()
    if h in wl:
        return 1.0
    if any(h.endswith("." + w) for w in wl):
        return 0.6
    return 0.0


# -------------------------------
# Features
# -------------------------------

def extract_features_v2(
    url: str,
    whitelist_csv: Optional[str] = None,
    whitelist_cache: Optional[set[str]] = None,
) -> Dict[str, Any]:
    parsed = urlparse(url if isinstance(url, str) else "")
    scheme = (parsed.scheme or "").lower()
    host = (parsed.netloc or parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""

    sub, dom, suf = _safe_tldextract(host)
    domain_length = len(dom) if dom else len(host)
    domain_entropy = shannon_entropy(dom if dom else host)
    domain_complexity = domain_length * domain_entropy
    tld_risk_weight = _tld_risk_weight(suf)

    wl = whitelist_cache or _load_whitelist(whitelist_csv or DEFAULT_WHITELIST_PATH)
    whitelist_strength = _whitelist_strength(host, wl)

    is_http = 1.0 if scheme == "http" else 0.0
    protocol_context_penalty = is_http * (1.0 - whitelist_strength)

    sub_clean = (sub or "").replace(".", "")
    host_entropy = 0.0 if len(sub_clean) < 3 else shannon_entropy(sub_clean)

    free_hosting_score = _is_free_hosting(host)
    domain_entropy_norm = min(max(domain_entropy / 4.5, 0.0), 1.0)
    free_hosting_weighted = float(free_hosting_score) * domain_entropy_norm * (1.0 - whitelist_strength)

    parts = _tokenize_path(path)
    total_tokens = max(1, len(parts))
    token_density = sum(1 for p in parts if p in ACTION_TOKENS) / float(total_tokens)
    suspicious_path_token = 1 if any(p in SUSPICIOUS_TOKENS for p in parts) else 0
    trusted_path_token = 1 if any(p in TRUSTED_TOKENS for p in parts) else 0

    trusted_path_penalty = 0.0 if whitelist_strength >= 0.6 else float(trusted_path_token)

    num_params = len(parse_qs(query))
    num_segments = len([p for p in path.split("/") if p])
    param_count_boost = num_params / float(max(1, num_segments))

    is_oauth_host = any(host == sfx or host.endswith("." + sfx) for sfx in OAUTH_HOSTS_SUFFIX)
    has_oauth_path = any(tok in path.lower() for tok in OAUTH_TOKENS_IN_PATH)
    oauth_like_relief = 1 if (is_oauth_host and has_oauth_path) else 0

    return {
        "domain_length": float(domain_length),
        "domain_entropy": float(domain_entropy),
        "domain_complexity": float(domain_complexity),
        "tld_risk_weight": float(tld_risk_weight),
        "host_entropy": float(host_entropy),
        "param_count_boost": float(param_count_boost),
        "token_density": float(token_density),
        "trusted_path_token": int(trusted_path_token),
        "trusted_path_penalty": float(trusted_path_penalty),
        "suspicious_path_token": int(suspicious_path_token),
        "whitelist_strength": float(whitelist_strength),
        "protocol_context_penalty": float(protocol_context_penalty),
        "free_hosting_score": float(free_hosting_score),
        "free_hosting_weighted": float(free_hosting_weighted),
        "oauth_like_relief": int(oauth_like_relief),
    }


def batch_extract_features_v2(
    urls: Iterable[str],
    whitelist_csv: Optional[str] = None,
    whitelist_cache: Optional[set[str]] = None,
) -> "pd.DataFrame":
    wl = whitelist_cache or _load_whitelist(whitelist_csv or DEFAULT_WHITELIST_PATH)
    rows = []
    for u in urls:
        try:
            rows.append(extract_features_v2(u, whitelist_cache=wl))
        except Exception as e:
            raise e
    return pd.DataFrame(rows)


# -------------------------------
# Bloque de test
# -------------------------------

if __name__ == "__main__":
    tests = [
        "http://secure-login.bbva.es/verificar?step=1",
        "https://www.caixabank.es/particulares/banca-digital.html",
        "https://login.microsoftonline.com/oauth2/v2.0/authorize?client_id=...",
        "https://recibir-paquete-correos.live/recibir_paquete.php",
        "https://usuarios.portal.gob.es/portal/particulares?ref=abc&lang=es",
        "http://clientes.seguridad.online/confirmar"
    ]

    df = batch_extract_features_v2(tests)
    pd.set_option("display.max_columns", None)
    print(df)
