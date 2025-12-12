# Feature Set v3 — Especificación Contractual

**Versión:** 3.0 FINAL  
**Estado:** CERRADO  
**Dependencias:**
- `features/features_constantes.py`
- `docs/whitelist.csv` (dominios oficiales)
- `docs/dominios_espanyoles.csv` (fuente de marcas españolas)

---

## 1. Objetivo

El Feature Set v3 define un vector mínimo de 7 features estructurales para detección de phishing en España. El diseño prioriza:

- Explicabilidad total
- Cero redundancia
- Estabilidad temporal
- Cero falsos positivos en dominios oficiales

---

## 2. Vector contractual (orden fijo)

```python
FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]
```

**Este orden es contractual.** Se utiliza en entrenamiento, scoring, despliegue y documentación.

---

## 3. Fuentes de verdad

### 3.1 Whitelist (`docs/whitelist.csv`)

Dominios oficiales españoles y proveedores globales neutros autorizados.

**Uso:** `domain_whitelist`, `trusted_token_context (+1)`, `domain_complexity (bypass)`

### 3.2 Marcas españolas (`docs/dominios_espanyoles.csv`)

CSV con dominios .es ordenados por ranking Tranco.

**Uso:** Generación de `brands_set` para `brand_in_path`, `brand_match_flag`, `trusted_token_context (0)`

**Construcción:**
```python
brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
```

**Requisito:** Ejecutar `load_brands_from_domains_es(constants)` antes de `extract_features_v3()`.

---

## 4. Definición de features

### 4.1 domain_complexity

| Atributo | Valor |
|----------|-------|
| Tipo | float |
| Rango | 0.0 – 1.0 |

Mide complejidad estructural del dominio mediante entropía + longitud + penalización de dominios cortos. Dominios en whitelist → 0.0.

### 4.2 domain_whitelist

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {0, 1} |

Indica si `registered_domain ∈ WHITELIST`. Señal estructural de legitimidad.

### 4.3 trusted_token_context (TTC v28)

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {-1, 0, +1} |

Contextualiza legitimidad del dominio:

| Valor | Condición |
|-------|-----------|
| +1 | `domain_whitelist == 1` |
| 0 | `domain_whitelist == 0` AND `core ∈ brands_set` |
| -1 | resto |

**Nota:** `brands_set` proviene de `dominios_espanyoles.csv`, NO de whitelist.

### 4.4 host_entropy

| Atributo | Valor |
|----------|-------|
| Tipo | float |
| Rango | 0.0 – 3.0 aprox |

Entropía Shannon del subdominio limpio. Detecta subdominios aleatorios típicos de kits de phishing.

### 4.5 infra_risk

| Atributo | Valor |
|----------|-------|
| Tipo | float |
| Rango | 0 – 5 |

Riesgo agregado de infraestructura:
```
infra_risk = 0.3 × is_http + tld_risk_weight + free_hosting
```

### 4.6 brand_in_path

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {0, 1} |

Detecta marca española en el path cuando el dominio NO es legítimo.

**Fuente de marcas:** `brands_set` derivado de `dominios_espanyoles.csv`

**Activación:** Solo si `domain_whitelist == 0`

### 4.7 brand_match_flag

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {0, 1} |

Indica si el núcleo del dominio coincide con una marca española.

**Fuente de marcas:** `brands_set` derivado de `dominios_espanyoles.csv`

```python
brand_match_flag = int(core in brands_set)
```

---

## 5. Requisitos de inicialización

Antes de invocar `extract_features_v3(url)`:

```python
from features.features_constantes import constants, load_brands_from_domains_es

# Cargar marcas desde CSV
load_brands_from_domains_es(constants)

# Verificar carga
assert "BRANDS_FROM_DOMAINS_ES" in constants
assert len(constants["BRANDS_FROM_DOMAINS_ES"]) > 0
```

---

## 6. Validación empírica

| Feature | Legítimas | Phishing | Observación |
|---------|-----------|----------|-------------|
| domain_complexity | bajo | alto | muy discriminativa |
| domain_whitelist | 1 | 0 | cero FPs |
| TTC_v28 | +1/0 | -1 | separa legitimidad |
| host_entropy | bajo | moderado-alto | detecta kits |
| infra_risk | 0 | alto | separa infraestructura |
| brand_in_path | 0 | ~20% | señal de abuso |
| brand_match_flag | ~0.7 | ~0.03 | sólida |

---

*Documento contractual del Feature Set v3.*
