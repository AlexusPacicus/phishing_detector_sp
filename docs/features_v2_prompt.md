# Prompt técnico para generar `features_v2.py` (Versión v2)

Tu tarea es implementar el archivo `features_v2.py` siguiendo estrictamente estas especificaciones.  
No añadas funciones, columnas ni lógica que no esté indicada aquí.  
No utilices features internas como salida final.  
No renombres ni alteres las columnas definidas en el output.

---

## 1. Firma de la función

La función debe tener exactamente esta firma:

```python
def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

### Requisitos de entrada:
- `df` debe contener una columna obligatoria:
  - `url` (string): URL completa a analizar.

### Requisitos de salida:
- Un `DataFrame` con **solo** las 9 features finales.
- Las columnas deben estar en el **orden exacto** definido.
- Sin valores NaN (rellenar con 0).
- Todas las columnas numéricas.

---

## 2. Features finales (únicas válidas)

Estas son **las únicas columnas** que deben exportarse:

```python
OUTPUT_COLUMNS = [
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
```

No se permite exportar ninguna columna fuera de esta lista.

---

## 3. Features internas (prohibidas en el output)

Estas features pueden usarse como pasos intermedios,  
pero **NO deben aparecer en el DataFrame final**:

```python
INTERNAL_FEATURES = [
    "domain_length",
    "domain_entropy",
    "is_http",
    "free_hosting",
    "tld_risk_weight",
    "trusted_path_token",
    "trusted_path_penalty",
]
```

---

## 4. Archivos externos necesarios

### Whitelist de dominios .es:
- Ruta: `docs/dominios_espanyoles.csv`
- Columna: `domain`

Debe cargarse como lista de strings en minúsculas.

### Tokens sectoriales:
- Ruta: `docs/tokens_por_sector.csv`
- Columnas: `sector`, `token`, `peso`
El archivo `docs/tokens_por_sector.csv` ya está normalizado y no debe modificarse.  
Tiene exactamente estas columnas:

- `sector`
- `token`
- `peso`

Todos los tokens están en minúsculas, sin tildes y sin duplicados.  
Los pesos están normalizados al rango 0.5–1.5 para evitar dominancia en la feature `token_density`.

La implementación debe:

- cargar el archivo tal cual  
- aplicar los pesos exactamente como aparecen  
- no modificar los valores  
- no transformar los tokens  

### Dominios neutrales globales
Ruta: `docs/global_neutral_domains.csv`
Columna: `domain`
Todos en minúsculas. No modificar este archivo.

### Hosting gratuito:
La constante FREE_HOSTING define todos los dominios de hosting gratuito, temporal o de baja reputación que deben detectarse.  
La función free_hosting(url) debe devolver 1 si la URL contiene cualquiera de estos valores, 0 en caso contrario.
No modificar esta lógica.

---

## 5. Constantes importadas obligatorias

```python
from features.features_constantes import (
    SUSPICIOUS_TOKENS_WEIGHT,
    GLOBAL_NEUTRAL_DOMAINS,
    SAFE_TLDS,
    COMMON_PHISH_TLDS,
    HIGH_RISK_TLDS,
    TOKEN_DENSITY_K,
    HTTP_WEIGHT,
)
```

No cambies, elimines ni crees constantes nuevas.

---

## 6. Definición exacta de cada feature final

### 6.1 `domain_complexity`
```text
domain_complexity = domain_length * domain_entropy
```

### 6.2 `host_entropy`
- Entropía de Shannon del subdominio extraído con `tldextract`.

### 6.3 `domain_whitelist_score`
- 1 si el dominio registrado coincide o termina en un dominio de la whitelist.
- 0 en caso contrario.

### 6.4 `suspicious_path_token`
- 1 si el path contiene alguno de estos tokens en español:  
  `verificar`, `pago`, `recibir`, `confirmar`, `paquete`, `sms`, `aduanas`, `3dsecure`  
- 0 si no.

### 6.5 `token_density`
Fórmula completa:

```text
token_density = (sum(weights) / total_tokens) * (path_depth / (path_depth + TOKEN_DENSITY_K))
```

### 6.6 `trusted_token_context`
Reglas:

```text
+1 si trusted_path_token == 1 y domain_whitelist_score == 1
-1 si trusted_path_token == 1 y domain_whitelist_score == 0
 0 en otros casos
```

### 6.7 `infra_risk`

```text
infra_risk = HTTP_WEIGHT * is_http + tld_risk_weight + free_hosting
```

### 6.8 fake_tld_in_subdomain_or_path
1 si el subdominio o path contienen cualquiera de los tokens definidos en FAKE_TLD_TOKENS.

### 6.9 `param_count_boost`
Número de símbolos `=` en la URL, como float.

---

## 7. Requisitos del DataFrame final

- Solo `OUTPUT_COLUMNS`
- En el **orden exacto**
- Sin columnas adicionales
- Sin NaN (rellenar con 0)
- Todas numéricas

---

## 8. Reglas estrictas

1. No añadir features nuevas.  
2. No exportar internas.  
3. No cambiar nombres ni orden.  
4. Nada fuera de estas especificaciones.  
5. Usar `tldextract` obligatoriamente.  
6. Si un cálculo falla → devolver 0.

---

## 9. Objetivo

Generar `features_v2.py` alineado con este documento  
y con `features_v2.md`, implementando **exactamente** las 9 features finales.
