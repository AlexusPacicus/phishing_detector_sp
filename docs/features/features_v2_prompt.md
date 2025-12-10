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
```

Parámetros:

- `url`: URL completa a analizar.  
- `domain_whitelist`: lista de dominios españoles legítimos.  
- `tokens_por_sector`: diccionario sectorial ya cargado desde CSV.

---

## 2. Salida obligatoria (OUTPUT_COLUMNS)

El diccionario devuelto debe contener exactamente estas columnas, en este orden:

```python
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
```

No exportar ninguna otra feature.

---

## 3. Features internas prohibidas en la salida

Estas features pueden existir como variables internas, pero NUNCA deben aparecer en el diccionario final:

```
free_hosting_boost
http_penalty
trusted_path_token
trusted_path_penalty
```

---

## 4. Constantes externas obligatorias

Debes importarlas exactamente así:

```python
from features_constantes import (
    FAKE_TLD_TOKENS,
    SUSPICIOUS_TOKENS_WEIGHT,
    FREE_HOSTING,
    BRAND_KEYWORDS,
    TLD_RISK,
    TRUSTED_TOKENS
)
```

No modificar listas ni pesos.

---

## 5. Reglas de cálculo (versión reforzada)

### 5.1 domain_entropy
- Extraer dominio con `tldextract.extract(url).domain`.  
- Calcular entropía de Shannon.  
- Si error → 0.

---

### 5.2 path_length
- Usar `urllib.parse.urlparse(url).path`.  
- Contar los caracteres del path sin parámetros.  
- Si no hay path → 0.

---

### 5.3 param_count
- Obtener query con `urlparse(url).query`.  
- Contar parámetros con `parse_qs`.  
- Si error → 0.

---

### 5.4 digit_ratio
- Contar dígitos en toda la URL.  
- Dividir entre longitud total.  
- Si longitud = 0 → 0.

---

### 5.5 fake_tld_in_subdomain_or_path
- FAKE_TLD_TOKENS viene de `features_constantes.py`.  
- Buscar cualquiera en subdominio (`extract.subdomain`) o path.  
- Por substring.  
- Si aparece uno → 1, si no → 0.

---

### 5.6 token_density

Fórmula OBLIGATORIA:

```
token_density = ( Σ(weights) / total_tokens ) * ( path_depth / (path_depth + k) )
```

Σ(weights) =  
- pesos de `SUSPICIOUS_TOKENS_WEIGHT`  
- + pesos específicos según el sector (`tokens_por_sector`)

Reglas fijas:
- total_tokens = tokens del path (split / _ -)
- path_depth = nº de segmentos del path  
- k = 2  
- error → 0  
- no inventar tokens  
- no añadir lógica nueva

---

### 5.7 brand_in_path
- Detectar si el path contiene un substring de `BRAND_KEYWORDS`.  
- Si sí → 1, si no → 0.

---

### 5.8 tld_risk_weight
- Extraer TLD con `tldextract.extract(url).suffix`.  
- Buscar en `TLD_RISK`.  
- Si no existe → 0.

---

## 6. trusted_token_context

Construir EXACTAMENTE:

```
trusted_token_context = trusted_path_token - trusted_path_penalty
```

### trusted_path_token
1 si el path contiene tokens de `TRUSTED_TOKENS`, si no 0.

### trusted_path_penalty
1 si:
- el path contiene tokens de confianza
- Y el dominio NO está en `domain_whitelist`

Si no → 0.

NO añadir pesos ni condiciones.

---

## 7. free_hosting_boost (interno)
```
free_hosting_boost = 1 si url contiene cualquier substring de FREE_HOSTING, si no 0
```
Reglas:
- búsqueda literal  
- no modificar FREE_HOSTING  
- no exportarlo  

---

## 8. http_penalty (interno)

```
http_penalty = 1 si la url empieza por "http://" y no por "https://"
```



## 9. Restricciones generales
- Cualquier excepción → 0.  
- No usar pandas.  
- Solo usar urllib, tldextract, re, math.  
- No modificar archivos externos.  
- No añadir columnas nuevas.  
- No cambiar el orden de OUTPUT_COLUMNS.


## 10. Entrega final

El archivo `features_v2.py` debe incluir:
1. Imports  
2. Funciones auxiliares  
3. La función principal `extract_features`  
4. Nada más  
(no tests, no ejecución directa)


