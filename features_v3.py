import tldextract
from urllib.parse import urlparse
from math import log2

FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]

def extract_features_v3(url: str, whitelist: set, constants: dict):
    # Normalización robusta de la URL
    if not isinstance(url, str):
        url = ""
    url = url.strip()
    if not url:
        return [0.0, 0, -1, 0.0, 0.0, 0, 0]
    try:
        parsed = urlparse(url)
        tld = tldextract.extract(parsed.hostname or "")
        registered_domain = tld.registered_domain or ""
        core = tld.domain or ""
        subdomain = tld.subdomain or ""
        subdomain_clean = subdomain.replace(".", "")
        path = parsed.path or ""
        scheme = parsed.scheme.lower() if parsed.scheme else ""
        brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
        domain_whitelisted = int(registered_domain in whitelist)
        brand_match_flag = int(core in brands_set)
        tld_suffix = tld.suffix or ""
        return [
            _domain_complexity(registered_domain, core, subdomain_clean, whitelist),
            _domain_whitelist(registered_domain, whitelist),
            _trusted_token_context(domain_whitelisted, brand_match_flag),
            _host_entropy(subdomain_clean),
            _infra_risk(scheme, tld_suffix, registered_domain, constants),
            _brand_in_path(path, brands_set, domain_whitelisted),
            _brand_match_flag(core, brands_set),
        ]
    except Exception:
        return [0.0, 0, -1, 0.0, 0.0, 0, 0]

def load_brands_from_domains_es(constants: dict, csv_path: str = "docs/dominios_espanyoles.csv"):
    import csv
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        domains_column = [
            row[0] for row in reader 
            if row and "dominio" not in row[0].lower()
        ]
    brands = {domain.split(".")[0].lower() for domain in domains_column if domain}
    constants["BRANDS_FROM_DOMAINS_ES"] = brands

def _domain_complexity(registered_domain, core, subdomain_clean, whitelist):
    if not registered_domain:
        return 0.0
    if registered_domain in whitelist:
        return 0.0
    domain_length = len(registered_domain)
    core_entropy = _shannon_entropy(core)
    norm_len = min(domain_length / 18, 1)
    norm_entropy = min(core_entropy / 3.8, 1)
    raw = 0.78 * norm_entropy + 0.22 * norm_len
    if domain_length < 10:
        raw *= 0.35
    dc = raw ** 0.55
    return min(max(dc, 0.0), 1.0)

def _domain_whitelist(registered_domain, whitelist):
    return int(registered_domain in whitelist)

def _trusted_token_context(domain_whitelisted, brand_match_flag):
    if domain_whitelisted == 1:
        return 1
    elif brand_match_flag == 1:
        return 0
    else:
        return -1

def _host_entropy(subdomain_clean):
    return _shannon_entropy(subdomain_clean) if subdomain_clean else 0.0

def _infra_risk(scheme, tld_suffix, registered_domain, constants):
    http_weight = constants.get("HTTP_WEIGHT", 0.3) if scheme == "http" else 0.0
    tld_risk_weight = constants.get("TLD_RISK", {}).get(tld_suffix.lower(), 0.0)
    if registered_domain in constants.get("GLOBAL_NEUTRAL_DOMAINS", set()):
        tld_risk_weight = 0.0
    free_hosting_weight = 1.0 if registered_domain in constants.get("FREE_HOSTING", set()) else 0.0
    return http_weight + tld_risk_weight + free_hosting_weight

def _brand_in_path(path, brands_set, domain_whitelisted):
    if domain_whitelisted:
        return 0
    last_segment = path.strip("/").split("/")[-1].lower() if path else ""
    import re
    tokens = re.split(r'[/\-_\.=&?%]', last_segment)
    tokens = [t for t in tokens if t]
    return int(any(t in brands_set for t in tokens))

def _brand_match_flag(core, brands_set):
    return int(core in brands_set)

def _shannon_entropy(text: str) -> float:
    text = (text or "").strip()
    if not text:
        return 0.0
    from collections import Counter
    counts = Counter(text)
    length = len(text)
    return -sum((c/length) * log2(c/length) for c in counts.values())
