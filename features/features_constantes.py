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


# ============================================================
# 🧠 1. TOKENS SOSPECHOSOS MANUALES — v2
# ============================================================
# Lista reducida, curada y estable. Servirá como base para la Fase 3.

SUSPICIOUS_TOKENS_WEIGHT = {
    # === Acciones comunes ===
    "verificar": 1.0,
    "confirmar": 1.5,
    "recibir": 1.0,
    "actualizar": 1.0,
    "acceso": 1.0,
    "login": 0.8,
    "clientes": 1.0,
    "sms": 1.0,
    "pago": 1.5,
    "seguridad": 1.0,

    # === Tokens logísticos ===
    "paquete": 1.2,
    "aduanas": 1.2,
    "envio": 1.2,
    "tracking": 1.0,

    # === Tokens financieros ===
    "tarjeta": 1.5,
    "pin": 1.2,
    "token": 1.0,
    "banca": 1.0,

    # === Tokens 3D Secure ===
    "verificacion": 2.0,
    "3d": 3.0,
    "3d-secure": 3.0,
    "no-back-button": 3.0,
}


# ============================================================
# 🌐 2. TLDs DE RIESGO — v2
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
# ☁️ 3. DOMINIOS GLOBALES NEUTRALES (CSV REAL)
# ============================================================
# Infraestructura global legítima que NO debe penalizarse.
# Este CSV es la fuente oficial (docs/global_neutral_domains.csv)

GLOBAL_NEUTRAL_DOMAINS = [
    d.strip().lower()
    for d in pd.read_csv("docs/global_neutral_domains.csv")["domain"].dropna().tolist()
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


