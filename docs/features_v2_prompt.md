# FEATURES V2 — PROMPT PARA AIDER (VERSIÓN REFORZADA)

## 🎯 Objetivo
Generar el archivo `features_v2.py` siguiendo estrictamente estas reglas y la documentación de `features_v2.md`.  
El archivo debe ser determinista, reproducible y sin invenciones.  
No añadir features, no modificar constantes externas, no cambiar nombres, no alterar el orden de salida.

---

## 1. Firma obligatoria de la función principal

Debes exportar una única función pública:

```python
def extract_features(url: str, domain_whitelist: list, tokens_por_sector: dict) -> dict:
Parámetros:

url: URL completa a analizar.

domain_whitelist: lista de dominios españoles legítimos.

tokens_por_sector: diccionario sectorial ya cargado desde CSV.

2. Salida obligatoria (OUTPUT_COLUMNS)
El diccionario devuelto debe contener exactamente estas columnas, en este orden:

arduino
Copiar código
[
    "domain_entropy",
    "path_length",
    "param_count",
    "digit_ratio",
    "fake_tld_in_subdomain_or_path",
    "token_density",
    "brand_in_path",
    "tld_risk_weight",
    "trusted_token_context"
]
No exportar ninguna otra feature.

3. Features internas prohibidas en la salida
Estas features pueden existir como variables internas pero nunca deben aparecer en la salida:

nginx
Copiar código
free_hosting_boost
http_penalty
trusted_path_token
trusted_path_penalty
4. Constantes externas obligatorias
Debes importarlas exactamente así:

python
Copiar código
from features_constantes import (
    FAKE_TLD_TOKENS,
    SUSPICIOUS_TOKENS_WEIGHT,
    FREE_HOSTING,
    BRAND_KEYWORDS,
    TLD_RISK,
    TRUSTED_TOKENS
)
No modificar listas ni pesos.

5. Reglas de cálculo (versión reforzada)
5.1 domain_entropy
Extraer dominio con tldextract.extract(url).domain

Calcular entropía Shannon.

Si error → devolver 0.

5.2 path_length
Usar urllib.parse.

Contar longitud del path sin parámetros.

Si no hay path → 0.

5.3 param_count
Obtener query con urllib.parse.urlparse(url).query.

Contar parámetros con parse_qs.

Error → 0.

5.4 digit_ratio
Contar dígitos presentes en toda la URL.

Dividir entre longitud total.

Si longitud = 0 → 0.

5.5 fake_tld_in_subdomain_or_path (REGLA REFORZADA)
FAKE_TLD_TOKENS se importa desde features_constantes.py.

Comprobar presencia de cualquiera de esos tokens en:

subdominio (extract.subdomain)

path (urlparse(url).path)

Detección por substring.

Si aparece al menos uno → 1, si no → 0.

5.6 token_density (REGLAS REFORZADAS)
Debe respetar exactamente esta fórmula:

ini
Copiar código
token_density = ( Σ(weights) / total_tokens ) * ( path_depth / (path_depth + k) )
Donde:

Σ(weights) incluye:

pesos de SUSPICIOUS_TOKENS_WEIGHT (substring search)

pesos específicos de sector si existen en tokens_por_sector

total_tokens = número total de tokens del path (split por /, _, -)

path_depth = número de segmentos del path

k = 2 (constante fija)

Error → 0

Reglas estrictas:

No inventar tokens.

No generar nuevos pesos.

No mezclar con features internas.

No usar TF-IDF ni heurísticas adicionales.

5.7 brand_in_path
Detectar si en el path aparece alguna palabra clave de BRAND_KEYWORDS.

Comparación por substring.

Si aparece alguna → 1, si no → 0.

5.8 tld_risk_weight
Extraer TLD con tldextract.extract(url).suffix.

Buscar en diccionario TLD_RISK.

Si no existe → 0.

Devolver peso tal cual.

6. Sistema "trusted_token_context" (REGLAS REFORZADAS)
Debes construir exactamente esta feature:

ini
Copiar código
trusted_token_context = trusted_path_token - trusted_path_penalty
Definiciones obligatorias:
trusted_path_token

1 si el path contiene cualquier token de TRUSTED_TOKENS.

0 en caso contrario.

trusted_path_penalty

1 si:

aparece un token de confianza en el path

Y el dominio no está en domain_whitelist

0 en caso contrario.

Reglas:

No inventar condiciones extra.

No añadir pesos.

No aplicar scoring.

7. free_hosting_boost (uso interno)
ini
Copiar código
free_hosting_boost = 1 si url contiene cualquier cadena de FREE_HOSTING, si no 0
Reglas:

Búsqueda por substring.

No normalizar.

No modificar FREE_HOSTING.

Variable interna, NO exportar.

8. http_penalty (uso interno)
ini
Copiar código
http_penalty = 1 si url empieza por "http://" y no por "https://"
Variable interna, NO exportar.

9. Obligaciones generales
Código robusto: cualquier excepción → fallback a 0.

No añadir logging ni prints.

No usar pandas.

Solo usar: urllib, tldextract, re, math.

No modificar archivos externos.

No cambiar nombres de columnas.

10. Entrega final
El archivo features_v2.py debe contener:

Imports

Funciones auxiliares

La función principal extract_features

Nada más

No incluir test ni ejecución directa.