# ============================================================
# ⚙️ FEATURES_CONSTANTES.PY — Constantes para features_v2
# ============================================================
# Última revisión: 2025-11-18
# Autor: Alexis Zapico Fernández
# Descripción:
#   Constantes oficiales de la versión v2 del sistema de
#   Feature Engineering para detección de phishing español.
#   Archivo limpio, sin duplicados y totalmente alineado con:
#       - features_v2.md (documentación humana)
#       - features_v2_prompt.md (prompt maestro para Aider)
# ============================================================

import pandas as pd
import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_PATH = os.path.join(PROJECT_ROOT, "docs", "global_neutral_domains.csv")


# ============================================================
# 🧠 1. TOKENS SOSPECHOSOS MANUALES — v2
# ============================================================
# Lista reducida, curada y estable. Servirá como base para la Fase 3.

SUSPICIOUS_TOKENS_WEIGHT = {
    "verificar": 1.0,
    "confirmar": 1.5,
    "recibir": 1.0,
    "actualizar": 1.0,
    "sms": 1.0,
    "pago": 1.5,
    "seguridad": 1.0,

    # Logísticos
    "paquete": 1.2,
    "aduanas": 1.2,
    "envio": 1.2,
    "tracking": 1.0,

    # Financieros
    "tarjeta": 1.5,
    "pin": 1.2,
    "token": 1.0,
    "banca": 1.0,

    # 3D Secure
    "verificacion": 2.0,
    "3d": 3.0,
    "3d-secure": 3.0,
    "no-back-button": 3.0,
}

# ============================================================
# TOKENS SOSPECHOSOS BINARIOS (SUSPICIOUS_TOKENS) — v2
# ============================================================
# Solo activan el flag suspicious_path_token = 1
# Deben aparecer casi exclusivamente en phishing moderno.

SUSPICIOUS_TOKENS = [
    "verificar",
    "confirmar",
    "pago",
    "paquete",
    "envio",
    "aduanas",
    "3d",
    "3dsecure",
    "sms",
]


# ============================================================
#  TOKENS LEGÍTIMOS DE CONFIANZA (TRUSTED_TOKENS) — v2
# ============================================================
# Usados en trusted_token_context:
#   +1 si aparecen en dominio whitelisted
#   -1 si aparecen en dominio NO whitelisted
#    0 si no aparecen

TRUSTED_TOKENS = [
    # Tokens típicos de rutas legítimas
    "login",
    "acceso",
    "clientes",
    "cliente",
    "cuenta",
    "area-cliente",
    "identificacion",
    "portal",
    "secure",
    "account",
]
# Ampliación v2.1 (compatibilidad inglés/español)
TRUSTED_TOKENS += [
    "access",
    "client",
    "clients",
    "auth",
    "authentication",
    "signin",
    "user",
]


# ============================================================
#  2. TLDs DE RIESGO — v2
# ============================================================

# TLDs baratos / genéricos usados masivamente en phishing
COMMON_PHISH_TLDS = {
    "app": 2.0,
    "live": 3.0,
    "shop": 2.5,
    "xyz": 2.0,
    "top": 2.0,
    "online": 2.0,
    "site": 2.0,
    "space": 1.5,
    "info": 1.5,
    "icu": 1.5,
    "web.app": 3.0,
    "repl.co": 3.0,
    "tempsite.link": 3.0,
    "rf.gd": 3.0,
}

# TLDs geopolíticos o de riesgo elevado
HIGH_RISK_TLDS = {"ru", "su", "by", "cn", "hk", "kp", "vn"}

# TLDs seguros / legítimos comunes
SAFE_TLDS = {"es", "com", "org", "net", "eu"}
# ============================================================
# 🔥 2.1 FUSIÓN OFICIAL TLD_RISK — v2 (Diccionario final)
# ============================================================
# Este diccionario es el único que debe usar el extractor.
# Combina:
#   - COMMON_PHISH_TLDS  → TLDs baratos/usados en kits
#   - HIGH_RISK_TLDS     → riesgo geopolítico elevado (peso fijo 3.0)
#   - SAFE_TLDS          → TLDs seguros que NO deben penalizarse
#
# Resultado: un único mapa TLD → peso numérico consistente.

TLD_RISK = {}

# 1) TLD comunes de phishing (valores ya ponderados)
for tld, score in COMMON_PHISH_TLDS.items():
    TLD_RISK[tld] = float(score)

# 2) TLD geopolíticos de alto riesgo (peso fijo v2.2 = 3.0)
for tld in HIGH_RISK_TLDS:
    TLD_RISK[tld] = 3.0

# 3) TLD seguros → 0.0
for tld in SAFE_TLDS:
    TLD_RISK[tld] = 0.0


# ============================================================
# ☁️ 3. DOMINIOS GLOBALES NEUTRALES (CSV REAL)
# ============================================================
# Infraestructura global legítima que NO debe penalizarse.
# Este CSV es la fuente oficial (docs/global_neutral_domains.csv)

GLOBAL_NEUTRAL_DOMAINS = [
    d.strip().lower()
    for d in pd.read_csv(DOCS_PATH)["domain"].dropna().tolist()
]



# ============================================================
# 🎭 4. TOKENS DE TLD FALSOS (ENGAÑOS VISUALES)
# ============================================================
# Detectan abuso de TLDs incrustados en subdominios o rutas
# Ej: "bbva.es-login.com", "ing.es-safe.app-net.ru"

FAKE_TLD_TOKENS = [
    # TLDs clásicos
    "es", "com", "net", "org", "eu",

    # TLDs modernos (muy usados en kits)
    "app", "shop", "online", "site", "store",

    # Genéricos engañosos
    "cloud", "tech", "pro", "email", "support", "info",

    # TLDs de riesgo incrustados
    "ru", "cn", "su", "by", "tk", "ml",
]


# ============================================================
# 🧱 5. FREE HOSTING DETECTADO (lista ampliada) — v2
# ============================================================
# Datos extraídos del dataset completo (TweetFeed + PhishTank + OpenPhish).
# Hosting gratuito = infraestructura poco fiable, usada masivamente en phishing.

FREE_HOSTING = [
    "000webhost",
    "blogspot",
    "wixsite",
    "weebly",
    "repl.co",
    "web.app",
    "tempsite.link",
    "rf.gd",
    "myfreesites.net",
    "freenom.com",
    "freenom.net",
    "awardspace",
    "infinityfree",
    "byethost",
    "heliohost",
    "googlesites",
]


# ============================================================
# ⚖️ 6. PARÁMETROS NUMÉRICOS
# ============================================================

# Parámetro de suavizado para token_density_improved()
TOKEN_DENSITY_K = 2.0

# Peso bajo para HTTP dentro de infra_risk()
HTTP_WEIGHT = 0.30


