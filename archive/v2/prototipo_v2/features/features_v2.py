"""
features_v2.py — Extractor de features v2 para URLs (phishing español)

Output contractual (orden fijo):
[
    "domain_complexity",
    "host_entropy",
    "domain_whitelist_score",
    "suspicious_path_token",
    "token_density",
    "trusted_token_context",
    "infra_risk",
    "fake_tld_in_subdomain_or_path",
    "param_count_boost",
]

Dependencias:
- features_constantes.py
- spanish_whitelist (set o frozenset, inyectado desde fuera)
"""

from __future__ import annotations

from typing import List, Set, FrozenSet
from urllib.parse import urlparse, parse_qs
from collections import Counter
from math import log2, exp

import tldextract

from .features_constantes import (
    SUSPICIOUS_TOKENS_WEIGHT,
    SUSPICIOUS_TOKENS,
    FREE_HOSTING,
    FAKE_TLD_TOKENS,
    TOKEN_DENSITY_K,
    TLD_RISK,
    TRUSTED_TOKENS,
)


INFRA_COMPROMISE_PATTERNS = [
    "/wp-", "/plugins", "/themes", "/includes", "/css/", "/js/", "/vendor/phpunit"
]


# -------------------------------------------------------------------
# 1. Helpers básicos: entropía y tokenización de path
# -------------------------------------------------------------------

def _shannon_entropy(text: str) -> float:
    """
    Entropía de Shannon sobre caracteres de `text`.
    Si text está vacío o hay error → 0.0
    """
    try:
        text = (text or "").strip()
        if not text:
            return 0.0
        counts = Counter(text)
        length = len(text)
        return -sum((c/length) * log2(c/length) for c in counts.values())
    except Exception:
        return 0.0


def _normalize_path_and_tokens(path: str) -> tuple[List[str], int]:
    """
    Devuelve:
    - tokens (normalizados reemplazando "-", "_", "%20", ".")
    - path_depth (solo cuenta "/" reales)
    """
    path = (path or "").lower()

    # Path depth estructural → solo "/"
    path_depth = len([s for s in path.split("/") if s])

    # Normalización para tokens
    norm = path
    for sep in ["-", "_", "%20", "."]:
        norm = norm.replace(sep, "/")

    tokens = [t for t in norm.split("/") if t]

    return tokens, path_depth


# -------------------------------------------------------------------
# 2. token_density
# -------------------------------------------------------------------

def _compute_token_weight_sum(path: str) -> float:
    """
    Suma de pesos W según el README v2:
    - Se basa en el PATH completo (lowercase).
    - Usa SUBSTRING sobre SUSPICIOUS_TOKENS_WEIGHT.
    """
    try:
        lower = (path or "").lower()
        if not lower:
            return 0.0

        total = 0.0
        for s_tok, weight in SUSPICIOUS_TOKENS_WEIGHT.items():
            if s_tok in lower:
                total += weight
        return total
    except Exception:
        return 0.0


def _token_density_improved(tokens: List[str], path_depth: int, path: str) -> float:
    """
    token_density = (W / total_tokens) * (path_depth / (path_depth + K))
    W se calcula sobre el PATH completo (SUBSTRING), como en el README.
    """
    try:
        total_tokens = len(tokens)
        if total_tokens == 0:
            return 0.0


        weight_sum = _compute_token_weight_sum(path)
        if weight_sum <= 0.0:
            return 0.0

        base = weight_sum / float(total_tokens)
        depth_factor = path_depth / float(path_depth + TOKEN_DENSITY_K)
        return base * depth_factor

    except Exception:
        return 0.0


# -------------------------------------------------------------------
# 3. Internal domain and infra signals
# -------------------------------------------------------------------

def _compute_domain_features(extract: tldextract.ExtractResult) -> tuple[float, float]:
    try:
        registered = (extract.registered_domain or "").lower()
        core = (extract.domain or "").lower()

        domain_length = len(registered) if registered else 0
        domain_entropy = _shannon_entropy(core)

        return float(domain_length), domain_entropy
    except Exception:
        return 0.0, 0.0


def _compute_host_entropy(extract: tldextract.ExtractResult) -> float:
    try:
        sub = (extract.subdomain or "").lower().replace(".", "")
        if not sub:
            return 0.0
        
        len_sub = len(sub)
        if len_sub < 4:
            return 0.0
        
        old_entropy = _shannon_entropy(sub)
        
        raw_entropy = old_entropy
        entropy_norm = min(raw_entropy / 4.0, 1.0)
        
        if 4 <= len_sub < 12:
            len_factor = len_sub / 12.0
        elif len_sub >= 12:
            len_factor = 1.0
        else:
            len_factor = 0.0
        
        new_entropy = max(0.0, min(entropy_norm * len_factor, 1.0))
        
        DEBUG_HOST_ENTROPY = False
        if DEBUG_HOST_ENTROPY:
            abs_diff = abs(new_entropy - old_entropy)
            rel_diff = abs_diff / max(old_entropy, 1e-6)
            print(f"[DEBUG host_entropy] old={old_entropy:.4f} new={new_entropy:.4f} abs={abs_diff:.4f} rel={rel_diff:.4f}")
        
        return new_entropy
    except Exception:
        return 0.0


def _compute_infra_signals(url: str, extract: tldextract.ExtractResult) -> tuple[int, float, int]:
    try:
        is_http = 1 if url.lower().startswith("http://") else 0
        tld = (extract.suffix or "").lower()
        tld_risk_weight = float(TLD_RISK.get(tld, 0.0))

        host = urlparse(url).netloc.lower()
        free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0

        return is_http, tld_risk_weight, free_hosting
    except Exception:
        return 0, 0.0, 0


def _compute_domain_whitelist_score(
    registered_domain: str,
    spanish_whitelist: Set[str] | FrozenSet[str],
) -> int:
    try:
        if not registered_domain:
            return 0
        
        # Construir whitelist extendida
        whitelist_extended = set()
        whitelist_extended.update(spanish_whitelist)
        
        # Añadir whitelists globales si existen
        g = globals()
        if 'WHITELIST_ES' in g:
            whitelist_extended.update(g['WHITELIST_ES'])
        if 'WHITELIST_GLOBAL' in g:
            whitelist_extended.update(g['WHITELIST_GLOBAL'])
        if 'WHITELIST_NEUTRAL' in g:
            whitelist_extended.update(g['WHITELIST_NEUTRAL'])
        
        registered_domain_lower = registered_domain.lower()
        
        # Verificar si registered_domain está en whitelist_extended
        if registered_domain_lower in whitelist_extended:
            return 1
        
        # Obtener host si está disponible globalmente
        host = None
        if 'CURRENT_HOST' in g:
            host = g['CURRENT_HOST']
        elif 'host' in g:
            host = g['host']
        
        if host:
            host_lower = str(host).lower()
            # Verificar si host termina exactamente en algún dominio de whitelist_extended
            for domain in whitelist_extended:
                domain_lower = str(domain).lower()
                if host_lower == domain_lower or host_lower.endswith('.' + domain_lower):
                    return 1
        
        return 0
    except Exception:
        return 0


# -------------------------------------------------------------------
# 4. Path signals
# -------------------------------------------------------------------

def _compute_suspicious_path_token(path: str) -> int:
    try:
        lower = (path or "").lower()
        return 1 if any(tok in lower for tok in SUSPICIOUS_TOKENS) else 0
    except Exception:
        return 0


def _compute_trusted_token_context(
    path: str,
    registered_domain: str,
    domain_whitelist_score: int,
) -> int:
    """
    trusted_token_context ∈ {-1, 0, +1}
    """
    try:
        lower = path.lower()
        has_trusted = any(t in lower for t in TRUSTED_TOKENS)

        if not has_trusted:
            return 0

        if domain_whitelist_score == 1:
            return 1
        else:
            return -1

    except Exception:
        return 0


def _compute_fake_tld_signal(host: str, path: str, extract: tldextract.ExtractResult) -> int:
    """
    Devuelve 1 si un token de FAKE_TLD_TOKENS aparece en el subdominio, en el path, o como token estructural en el dominio,
    siempre que ese fake NO forme parte del suffix real de la URL.
    """
    try:
        lower_host = (host or "").lower()
        lower_path = (path or "").lower()
        suffix = (extract.suffix or "").lower()
        domain = (extract.domain or "").lower()
        # Construir prefix_before_suffix
        prefix_before_suffix = lower_host
        suffix_full = f".{domain}.{suffix}" if domain and lower_host.endswith(f".{domain}.{suffix}") else None
        if suffix_full and lower_host.endswith(suffix_full):
            prefix_before_suffix = lower_host[: -len(suffix_full)]
        else:
            suffix_dot = f".{suffix}"
            if suffix and lower_host.endswith(suffix_dot):
                prefix_before_suffix = lower_host[: -len(suffix_dot)]
        for fake in FAKE_TLD_TOKENS:
            if fake == suffix:
                continue
            # Solo activar si el fake aparece como token estructural en el dominio
            domain_tokens = [t for t in domain.replace('-', '.').split('.') if t]
            if fake in domain_tokens:
                return 1
            if fake in prefix_before_suffix.split('.') or fake in prefix_before_suffix.split('-'):
                return 1
            if fake in lower_path.split('/') or fake in lower_path.split('-'):
                return 1
        return 0
    except Exception:
        return 0


def _compute_param_count_boost(query: str) -> float:
    try:
        if not query:
            return 0.0

        params = parse_qs(query, keep_blank_values=True)
        P = len(params)
        return P / float(P + 1) if P > 0 else 0.0
    except Exception:
        return 0.0


# -------------------------------------------------------------------
# 5. API principal
# -------------------------------------------------------------------

def extract_features_v2(
    url: str,
    spanish_whitelist: Set[str] | FrozenSet[str],
) -> List[float]:
    """
    Extrae las 9 features finales de v2 para una URL.
    """
    try:
        url = (url or "").strip()
        if not url:
            return [0.0] * 9

        parsed = urlparse(url)
        extract_res = tldextract.extract(url)

        registered = (extract_res.registered_domain or "").lower()
        host = parsed.netloc or ""
        path = parsed.path or ""
        query = parsed.query or ""
        # Dominio .es comprometido: override total
        if registered.endswith(".es") and any(p in path.lower() for p in INFRA_COMPROMISE_PATTERNS):
            return [
                0.0,  # domain_complexity
                0.0,  # host_entropy
                1.0,  # domain_whitelist_score (es dominio real)
                0.0,  # suspicious_path_token
                0.0,  # token_density
                0.0,  # trusted_token_context
                0.0,  # infra_risk
                0.0,  # fake_tld_in_subdomain_or_path
                0.0,  # param_count_boost
            ]


        # --- Internas básicas ---
        domain_length, domain_entropy = _compute_domain_features(extract_res)
        domain_whitelist_score = _compute_domain_whitelist_score(registered, spanish_whitelist)
        host_entropy = _compute_host_entropy(extract_res)
        is_http, tld_risk_weight, free_hosting = _compute_infra_signals(url, extract_res)

        normalized_length = max(0.0, min(domain_length / 20.0, 1.0))
        normalized_entropy = max(0.0, min(domain_entropy / 4.0, 1.0))

        raw = 0.65 * normalized_entropy + 0.35 * normalized_length

        if domain_length < 10:
            raw *= 0.55

        if domain_whitelist_score == 1:
            raw = 0.0

        domain_complexity = float(max(0.0, min(raw, 1.0)))

        tokens, path_depth = _normalize_path_and_tokens(path)

        suspicious_path_token = _compute_suspicious_path_token(path)
        token_density = _token_density_improved(tokens, path_depth, path)

        trusted_token_context = _compute_trusted_token_context(
            path, registered, domain_whitelist_score
        )
        infra_risk = 0.3 * is_http + tld_risk_weight + free_hosting

        fake_tld_in_subdomain_or_path = _compute_fake_tld_signal(
            host, path, extract_res
        )

        param_count_boost = _compute_param_count_boost(query)

        return [
            float(domain_complexity),
            float(host_entropy),
            float(domain_whitelist_score),
            float(suspicious_path_token),
            float(token_density),
            float(trusted_token_context),
            float(infra_risk),
            float(fake_tld_in_subdomain_or_path),
            float(param_count_boost),
        ]

    except Exception:
        return [0.0] * 9


def pretty_print_features(feature_vector):
    feature_names = [
        "domain_complexity",
        "host_entropy",
        "domain_whitelist_score",
        "suspicious_path_token",
        "token_density",
        "trusted_token_context",
        "infra_risk",
        "fake_tld_in_subdomain_or_path",
        "param_count_boost",
    ]
    for name, value in zip(feature_names, feature_vector):
        print(f"{name}: {value}")
