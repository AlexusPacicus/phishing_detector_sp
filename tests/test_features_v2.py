# ============================================================
# 🧪 TEST_FEATURES_V2_2.PY — Pruebas unitarias básicas
# ============================================================
# Comprueba que el sistema de extracción de features v2.2
# funciona correctamente, genera todas las columnas esperadas
# y mantiene coherencia entre funciones.
# ============================================================

import pytest
import pandas as pd
from features.features_v2 import (
    extract_features,
    domain_whitelist_score,
    token_density_improved,
    tld_risk_weight,
    fake_tld_in_subdomain_or_path,
    load_whitelist,
)


# ============================================================
# 🔧 TESTS DE FUNCIONALIDAD INDIVIDUAL
# ============================================================

def test_domain_whitelist_score_exact_match():
    whitelist = ["bbva.es", "santander.es"]
    assert domain_whitelist_score("https://clientes.bbva.es", whitelist) == 1
    assert domain_whitelist_score("https://bbva.es-login.com", whitelist) == 0


def test_token_density_formula():
    url = "https://phish.live/login/confirmar"
    val = token_density_improved(url)
    assert 0 < val < 3.0


def test_tld_risk_weight_levels():
    whitelist = ["bbva.es"]
    assert tld_risk_weight("https://malware.ru", whitelist) == 3.0
    assert tld_risk_weight("https://bbva.es", whitelist) == 0.0
    assert tld_risk_weight("https://fake.live", whitelist) >= 2.5


def test_fake_tld_detection():
    assert fake_tld_in_subdomain_or_path("https://bbva.es-login.com") == 1
    assert fake_tld_in_subdomain_or_path("https://clientes.bbva.es") == 0


def test_whitelist_loader_exists():
    wl = load_whitelist("docs/dominios_espanyoles.csv")
    assert isinstance(wl, list)
    assert all(isinstance(d, str) for d in wl)
    assert any("es" in d for d in wl)


# ============================================================
# 🧩 TEST INTEGRADO DE EXTRACT_FEATURES
# ============================================================

def test_extract_features_generates_all_columns():
    # URLs de prueba (phishing / legítima / edge cases)
    data = {
        "url": [
            "https://clientes.bbva.es/login",
            "http://bbva.es-login.com/secure/pago.php",
            "https://correos.com/pago-es/confirmar",
            "https://malware.ru/phish/login",
            "https://fake.live/recibir/envio"
        ]
    }
    df = pd.DataFrame(data)
    features = extract_features(df)

    expected_cols = [
        "domain_length", "domain_entropy", "domain_complexity", "host_entropy",
        "free_hosting", "is_http", "tld_risk_weight", "infra_risk",
        "domain_whitelist_score", "token_density", "fake_tld_in_subdomain_or_path",
        "param_count_boost", "trusted_path_token", "suspicious_path_token",
        "trusted_path_penalty"
    ]

    # Validar columnas
    assert all(c in features.columns for c in expected_cols)
    # Validar tipo numérico
    assert features[expected_cols].select_dtypes(include=["number"]).shape[1] == len(expected_cols)
    # Validar que no hay NaN
    assert features.isna().sum().sum() == 0
    # Validar que las features tienen variabilidad (no todo ceros)
    assert features.sum().sum() > 0
