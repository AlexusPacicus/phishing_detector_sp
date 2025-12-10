# tests/test_features.py
import pytest
from app.features import extract_features

def test_extract_features_keys():
    url = "https://soporte-netflx.com/"
    feats = extract_features(url)

    # ✅ Debe devolver exactamente 10 features
    expected_keys = {
        "domain_length", "domain_entropy", "num_params",
        "trusted_path_token", "contains_percent", "contains_equal",
        "suspicious_path_token", "free_hosting", "protocol", "tld_group"
    }
    assert set(feats.keys()) == expected_keys

def test_extract_features_values_types():
    url = "https://soporte-netflx.com/"
    feats = extract_features(url)

    # ✅ Tipos correctos: int/float/str
    assert isinstance(feats["domain_length"], int)
    assert isinstance(feats["domain_entropy"], float)
    assert isinstance(feats["protocol"], int)
    assert isinstance(feats["tld_group"], str)
