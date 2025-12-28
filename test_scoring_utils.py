# tests/test_scoring_utils.py
from scripts.scoring_utils import norm_text, parse_url

def test_norm_text_basic():
    assert norm_text("  ÁÉÍÓÚ España  ") == "aeiou espana"
    assert norm_text(None) == ""
    assert norm_text(123) == ""

def test_parse_url_adds_scheme():
    info = parse_url("example.com/login")
    assert info["domain"] == "example.com"
    assert info["protocol"] == "http"
    assert info["path"] == "/login"
    assert info["tld"] == ".com"

def test_parse_url_handles_encoded_and_https():
    info = parse_url("https://mi-dominio.es/p%c3%a1gina?x=1")
    assert info["domain"] == "mi-dominio.es"
    assert info["protocol"] == "https"
    assert info["path"] == "/página"      # unquote correcto
    assert info["tld"] == ".es"
    assert "x=1" in info["query"]
