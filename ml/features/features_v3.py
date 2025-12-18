"""
features_v3.py — Extractor de features v3 para URLs (phishing español)

Output contractual (orden fijo):
FEATURES_V3 = [...nombres en orden...]

Dependencias:
- features_constantes.py
- whitelist (set o frozenset, inyectado desde fuera)
- brands_set (set o frozenset, inyectado desde fuera)
- constants (objeto/dict, inyectado desde fuera)
"""

from __future__ import annotations

from typing import List, Set, FrozenSet
from urllib.parse import urlparse, parse_qs
from math import log2, exp
import math
import re
from collections import Counter

import tldextract


# Lista de nombres de features en orden (pendiente de implementación)
FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag",
]


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


def extract_features_v3(
    url: str,
    whitelist: Set[str] | FrozenSet[str],
    brands_set: Set[str] | FrozenSet[str],
    constants: dict,
) -> List[float]:
    """
    Extrae las features finales de v3 para una URL.
    
    Args:
        url: URL a analizar
        whitelist: Conjunto de dominios en whitelist
        brands_set: Conjunto de marcas conocidas
        constants: Diccionario con constantes necesarias
    
    Returns:
        Lista de features en el orden definido por FEATURES_V3
    """
    try:
        url = (url or "").strip()
        if not url:
            domain_complexity = 0.0
            domain_whitelist = 0
            brand_match_flag = 0
            trusted_token_context = -1
            host_entropy = 0.0
            infra_risk = 0.0
            brand_in_path = 0
        else:
            # 1. Parse the URL with tldextract
            ext = tldextract.extract(url)
            core = (ext.domain or "").lower()
            registered = (ext.registered_domain or "").lower()

            # 2. Base signals
            domain_length = len(registered)
            domain_entropy = _shannon_entropy(core)

            # 3. Normalisations
            norm_len = min(domain_length / 18.0, 1.0)
            norm_ent = min(domain_entropy / 3.8, 1.0)

            # 4. Raw combination
            raw = 0.78 * norm_ent + 0.22 * norm_len

            # 5. Extra penalty
            if domain_length < 10:
                raw *= 0.35

            # 6. Whitelist hard override
            if registered in whitelist:
                raw = 0.0

            # 7. Final score
            score = raw ** 0.55
            domain_complexity = max(0.0, min(score, 1.0))

            # domain_whitelist
            domain_whitelist = 1 if registered in whitelist else 0

            # brand_match_flag
            core = (ext.domain or "").lower()
            brand_match_flag = 1 if core in brands_set else 0

            # trusted_token_context
            if domain_whitelist == 1:
                trusted_token_context = +1
            elif brand_match_flag == 1:
                trusted_token_context = 0
            else:
                trusted_token_context = -1

            # host_entropy
            sub = (ext.subdomain or "").replace(".", "")
            if not sub:
                host_entropy = 0.0
            else:
                host_entropy = _shannon_entropy(sub)

            # infra_risk
            scheme = urlparse(url).scheme.lower()
            host = ext.registered_domain.lower() or ""
            tld = (ext.suffix or "").lower()

            http_weight = constants["HTTP_WEIGHT"] if scheme == "http" else 0.0
            tld_risk_weight = constants["TLD_RISK"].get(tld, 0.0)
            # v3_ok_infra_risk
            free_hosting_weight = 1.0 if host in constants["FREE_HOSTING"] else 0.0

            infra_risk = http_weight + tld_risk_weight + free_hosting_weight

            # brand_in_path
            last_segment = url.split("/", 3)[-1].lower()
            tokens = re.split(r'[/\-_\.=&?%]', last_segment)
            tokens = [t for t in tokens if t]  # Remove empty tokens
            if any(token in brands_set for token in tokens) and domain_whitelist == 0:
                brand_in_path = 1
            else:
                brand_in_path = 0
    except Exception:
        domain_complexity = 0.0
        domain_whitelist = 0
        brand_match_flag = 0
        trusted_token_context = -1
        host_entropy = 0.0
        infra_risk = 0.0
        brand_in_path = 0

    return [
        domain_complexity,
        domain_whitelist,
        trusted_token_context,
        host_entropy,
        infra_risk,
        brand_in_path,
        brand_match_flag,
    ]

